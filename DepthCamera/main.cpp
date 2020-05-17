#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include <iostream>
#include <string>
#include <sstream>
#include "ObjLoader.h"
#include "Shader.h"
#include "Camera.h"
#include <fstream>
#include "UdpClient.h"
#include <thread>
#include <chrono>
#include <vector>
#include <fstream>

#define ADDR "127.0.0.1"
#define PORT 5005
#define SERVER_LIMIT 1024

#define IMG_SIZE 512

static void framebuffer_size_callback(GLFWwindow* window, int width, int height);
static void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods);
static void mouse_button_callback(GLFWwindow* window, int button, int action, int mods);

glm::vec3 cameraPos = glm::vec3(0.0f, 1.3f, 0.0f);

void SendImage(BYTE* img, unsigned int w, unsigned int h, UdpClient& client)
{
    //size_t max_data = (SERVER_LIMIT / sizeof(float));
    /*unsigned int pos = 0;
    unsigned int max_pos = w * h * 3 * sizeof(float);

    char* data = new char[SERVER_LIMIT];
    FloatToChar converter;
    converter.f = img[0];

    unsigned int sent_packages = 0;
    unsigned int float_stepper = 0;
    unsigned int float_counter = 0;

    std::cout << img[0] << std::endl;

    while (pos < max_pos)
    {
        for (unsigned int i = 0; i < SERVER_LIMIT; i++)
        {
            if (!i)
                data[i] = 'c';
            else
            {
                data[i] = converter.c[float_stepper];
                std::cout << +data[i] << std::endl;
                float_stepper++;
                if (float_stepper == 4)
                {
                    float_stepper = 0;
                    float_counter++;
                    if (float_counter >= w * h * 3)
                        break;
                    converter.f = img[float_counter];
                    std::cout << img[float_counter] << std::endl;
                }
            }

            pos++;
            if (pos >= max_pos)
                break;

        }
        client.send(data, SERVER_LIMIT);
        sent_packages++;
        //
    }
    std::cout << "Packages sent: " << sent_packages << std::endl;
    delete [] data;*/

    unsigned int pos = 0;
    unsigned int max_pos = w * h * 3;
    unsigned int sent_packages = 0;

    char* data = new char[SERVER_LIMIT];
    while (pos < max_pos)
    {
        for (unsigned int i = 0; i < SERVER_LIMIT; i++)
        {
            if (pos < max_pos)
                data[i] = img[pos];
            else
                data[i] = 0;
            pos++;
        }

        client.send(data, SERVER_LIMIT);
        sent_packages++;
        std::this_thread::sleep_for(std::chrono::milliseconds(5));
    }


    std::cout << "Packages sent: " << sent_packages << std::endl;
    delete [] data;
}

int main(int argc, char** argv)
{
    UdpClient client(ADDR, PORT);
    client.send("camera", 5);
    std::string data = client.receive();
    std::cout << data << std::endl;

    ObjLoader loader;
    std::string fileName = "mesh.obj";
    loader.LoadObjFrom(fileName);

    unsigned int SCR_WIDTH = IMG_SIZE;
    unsigned int SCR_HEIGHT = IMG_SIZE;

    bool noWindow = false;
    for (int i = 0; i < argc; i++)
    {
        if (i == 0)
            continue;
        if (argv[i] == "--width" || argv[i] == "-W")
        {
            std::stringstream ss;
            ss.str(argv[i + 1]);
            ss >> SCR_WIDTH;
            i++;
        }
        else if (argv[i] == "--height" || argv[i] == "-H")
        {
            std::stringstream ss;
            ss.str(argv[i + 1]);
            ss >> SCR_HEIGHT;
            i++;
        }
        else if (argv[i] == "--file" || argv[i] == "-F")
        {
            fileName = argv[i + 1];
            i++;
        }
        else if (argv[i] == "--no_window" || argv[i] == "--no-window" || argv[i] == "-N")
            noWindow = true;
    }

    // glfw: initialize and configure
    // ------------------------------
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "LearnOpenGL", nullptr, nullptr);
    if (window == nullptr) {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
    glfwSetKeyCallback(window, key_callback);
    glfwSetMouseButtonCallback(window, mouse_button_callback);

    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    glEnable(GL_DEPTH_TEST);

    Shader shader("shader.vs", "shader.fs");

    float* vertices = new float[loader.GetVertices().size()];
    unsigned int* indices = new unsigned int[loader.GetIndicies().size()];

    for (unsigned int i = 0; i < loader.GetVertices().size(); i++)
        vertices[i] = loader.GetVertices()[i];
    for (unsigned int i = 0; i < loader.GetIndicies().size(); i++)
        indices[i] = loader.GetIndicies()[i];

    unsigned int VBO, VAO;

    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);

    glBindVertexArray(VAO);

    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(float) * loader.GetVertices().size(), vertices, GL_STATIC_DRAW);

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);

    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);

    shader.use();


    BYTE* pixels = new BYTE[SCR_WIDTH * SCR_HEIGHT * 3];
    bool changed = true;
    bool exit = false;
    while (!glfwWindowShouldClose(window) && !exit) {

        client.send("get", 3);
        std::string ans = client.receive();
        if (ans[0] != '\0')
        {
            std::cout << "Message received: ";
            for (unsigned int i = 0; i < ans.size(); i++)
                std::cout << +ans[i];
            std::cout << std::endl;
            float dist = ans[1] * 0.01f;
            switch (ans[0])
            {
            case 1:
                cameraPos += glm::vec3(0.0f, dist, 0.0f);
                std::cout << "Moving up!" << std::endl;
                break;
            case 2:
                cameraPos += glm::vec3(0.0f, -dist, 0.0f);
                break;
            case 3:
                cameraPos += glm::vec3(-dist, 0.0f, 0.0f);
                break;
            case 4:
                cameraPos += glm::vec3(dist, 0.0f, 0.0f);
                break;
            case 5:
                cameraPos += glm::vec3(0.0f, 0.0f, -dist);
                break;
            case 6:
                cameraPos += glm::vec3(0.0f, 0.0f, dist);
                break;
            }

            changed = true;
        }
        glClearColor(0.0, 0.0, 0.0, 1.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

        shader.use();
        glm::mat4 projection = glm::perspective(glm::radians(90.0f), (float)SCR_WIDTH / (float)SCR_HEIGHT, 0.01f, 100.0f);
        shader.setMat4("projection", projection);

        glm::mat4 view = glm::lookAt(cameraPos, cameraPos + glm::vec3(0.0f, 0.0f, -1.0f), glm::vec3(0.0f, 1.0f, 0.0f));
        shader.setMat4("view", view);


        glBindVertexArray(VAO);

        glm::mat4 model = glm::mat4(1.0f);
        shader.setMat4("model", model);

        glDrawArrays(GL_TRIANGLES, 0, loader.GetFaceVertexCount());

        if (changed)
        {
            glReadPixels(0, 0, SCR_WIDTH, SCR_HEIGHT, GL_RGB, GL_UNSIGNED_BYTE, pixels); //GL_DEPTH_COMPONENT
            SendImage(pixels, SCR_WIDTH, SCR_HEIGHT, client);
            changed = false;
        }
        else
            std::this_thread::sleep_for(std::chrono::milliseconds(500));

        glfwSwapBuffers(window);
        glfwPollEvents();



    }

    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);

    glfwTerminate();
    return 0;
}

static void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods) {
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);
    if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
        cameraPos += glm::vec3(0.0f, 0.01f, 0.0f);
    if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
        cameraPos += glm::vec3(0.0f, -0.01f, 0.0f);
    if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
        cameraPos += glm::vec3(0.01f, 0.0f, 0.0f);
    if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
        cameraPos += glm::vec3(-0.01f, 0.0f, 0.0f);
    if (glfwGetKey(window, GLFW_KEY_UP) == GLFW_PRESS)
        cameraPos += glm::vec3(0.0f, 0.0f, 0.01f);
    if (glfwGetKey(window, GLFW_KEY_DOWN) == GLFW_PRESS)
        cameraPos += glm::vec3(0.0f, 0.0f, -0.01f);
}

static void mouse_button_callback(GLFWwindow* window, int button, int action, int mods) {
    if(button == GLFW_MOUSE_BUTTON_LEFT && action == GLFW_PRESS) {
        double xpos, ypos;
        //getting cursor position
        glfwGetCursorPos(window, &xpos, &ypos);
        std::cout << "Cursor Position at (" << xpos << " : " << ypos << "\n";
    }
}

// glfw: whenever the window size changed (by OS or user resize) this callback function executes
// ---------------------------------------------------------------------------------------------
static void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
    // make sure the viewport matches the new window dimensions; note that width and
    // height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height);
}
