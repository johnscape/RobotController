#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include <iostream>
#include <string>
#include <sstream>
#include "ObjLoader.h"
#include "Shader.h"
#include "Camera.h"
#include <fstream>

static void framebuffer_size_callback(GLFWwindow* window, int width, int height);
static void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods);
static void mouse_button_callback(GLFWwindow* window, int button, int action, int mods);

glm::vec3 cameraPos = glm::vec3(0.0f, 1.3f, 0.0f);

int main(int argc, char** argv)
{
    unsigned int SCR_WIDTH = 512;
    unsigned int SCR_HEIGHT = 512;
    std::string fileName = "mesh.obj";
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


    ObjLoader loader;
    loader.LoadObjFrom(fileName);
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


    float* depth = new float[SCR_WIDTH * SCR_HEIGHT];
    bool changed = true;
    while (!glfwWindowShouldClose(window)) {

        if (!changed)
            continue;
        else
        {
            //changed = false;
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
            glfwSwapBuffers(window);

            //glReadPixels(0, 0, SCR_WIDTH, SCR_HEIGHT, GL_DEPTH_COMPONENT, GL_FLOAT, depth);
            /*std::ofstream imgWriter("img.data");
            imgWriter << SCR_WIDTH << " " << SCR_HEIGHT << " ";
            for (unsigned int x = 0; x < SCR_WIDTH; x++)
            {
                for (unsigned int y = 0; y < SCR_HEIGHT; y++)
                    imgWriter << depth[y * SCR_WIDTH + x] << " ";
            }
            imgWriter.close();
            std::cout << "Finished writing!" << std::endl;*/
        }

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
