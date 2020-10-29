#include "ModelLoader.h"
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <iostream>
#include <fstream>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"


ModelLoader::ModelLoader()
{
    VerticleArray = nullptr;
    IndiciesArray = nullptr;
}

ModelLoader::~ModelLoader()
{
    if (VerticleArray)
        delete[] VerticleArray;
    if (IndiciesArray)
        delete[] IndiciesArray;
}

bool ModelLoader::StartLoading(std::string file, unsigned int& texture, unsigned int& VAO, unsigned int& VBO, unsigned int& EBO, std::string folder)
{
    startingFolder = folder;
    if (!LoadModel(file))
    {
        std::cout << "Error while loading model!" << std::endl;
        return false;
    }
    if (!CreateBuffers(VBO, VAO, EBO))
    {
        std::cout << "Error while creating buffers!" << std::endl;
        return false;
    }
    if (!LoadTextures(texture))
    {
        std::cout << "Error while loading texture!" << std::endl;
        return false;
    }
    
    std::cout << "Model successfuly loaded!" << std::endl;
    return false;
}

bool ModelLoader::LoadModel(std::string file)
{
    std::cout << "Loading model " << file << "..." << std::endl;
    std::ifstream reader(startingFolder + file);
    if (!reader.good())
    {
        std::cout << "Model file does not exists: " << file << std::endl;
        return false;
    }

    std::string line;
    unsigned char phase = 0;
    while (std::getline(reader, line))
    {
        if (line[0] == '#')
            continue;
        std::vector<std::string> lineParts = Split(line);
        if (lineParts[0] == "mtllib")
            texturePath = lineParts[1];
        else if (lineParts[0] == "v")
        {
            Verticle v;
            v.x = std::stof(lineParts[1]);
            v.y = std::stof(lineParts[2]);
            v.z = std::stof(lineParts[3]);
            verticles.push_back(v);
        }
        else if (lineParts[0] == "vt")
        {
            if (phase == 0)
            {
                std::cout << "Reading texture coords..." << std::endl;
                phase++;
            }
            Verticle v;
            v.x = std::stof(lineParts[1]);
            v.y = std::stof(lineParts[2]);
            textureVerticles.push_back(v);
        }
        else if (lineParts[0] == "vn")
        {
            if (phase == 1)
            {
                std::cout << "Reading normals..." << std::endl;
                phase++;
            }
            Verticle v;
            v.x = std::stof(lineParts[1]);
            v.y = std::stof(lineParts[2]);
            v.z = std::stof(lineParts[2]);
            normalVerticles.push_back(v);
        }
        else if (lineParts[0] == "f")
        {
            if (phase == 2)
            {
                std::cout << "Reading faces..." << std::endl;
                phase++;
            }
            Face f;

            std::vector<std::string> targets = Split(lineParts[1], '/');
            f.av = std::stoi(targets[0]);
            f.at = std::stoi(targets[1]);
            f.an = std::stoi(targets[2]);

            targets = Split(lineParts[2], '/');
            f.bv = std::stoi(targets[0]);
            f.bt = std::stoi(targets[1]);
            f.bn = std::stoi(targets[2]);

            targets = Split(lineParts[3], '/');
            f.cv = std::stoi(targets[0]);
            f.ct = std::stoi(targets[1]);
            f.cn = std::stoi(targets[2]);

            faces.push_back(f);
        }
    }

    reader.close();

    std::cout << "Model loaded!" << std::endl;
	return true;
}

bool ModelLoader::LoadTextures(unsigned int& texture)
{
    texturePath = startingFolder + texturePath;
    std::cout << "Loading texture from " << texturePath << std::endl;
    std::ifstream reader(texturePath);
    if (!reader.good())
    {
        std::cout << "File not found: " << texturePath << std::endl;
        return false;
    }
    std::string line;
    std::string imageFile;
    while (std::getline(reader, line))
    {
        std::vector<std::string> parse = Split(line);
        if (parse.size() < 2)
            continue;
        if (parse[0] != "map_Kd")
            continue;
        imageFile = parse[1];
        break;
    }
    reader.close();
    reader.open(imageFile);
    if (!reader.good())
    {
        std::cout << "Image not found: " << imageFile << std::endl;
        return false;
    }
    reader.close();
    glGenTextures(1, &texture);
    glBindTexture(GL_TEXTURE_2D, texture);

    int width, height, nrChannels;
    stbi_set_flip_vertically_on_load(true);
    unsigned char* data = stbi_load(imageFile.c_str(), &width, &height, &nrChannels, 0);
    std::cout << "Image read." << std::endl;

    if (data)
    {
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
        glGenerateMipmap(GL_TEXTURE_2D);
    }
    else
    {
        std::cout << "Failed to load texture!" << std::endl;
        return false;
    }

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

    stbi_image_free(data);
    std::cout << "Image loading finished!" << std::endl;
    return true;
}

bool ModelLoader::CreateBuffers(unsigned int& VBO, unsigned int& VAO, unsigned int& EBO)
{
    std::cout << "Creating buffers..." << std::endl;

    VerticleArray = new float[faces.size() * 3 * (3 + 2)];
    IndiciesArray = new unsigned int[faces.size() * 3]; //TODO: use EBO

    for (unsigned int i = 0; i < faces.size(); i++)
    {
        unsigned int pos = i * 15;
        for (unsigned char t = 0; t < 3; t++)
        {
            if (t == 0)
            {
                VerticleArray[pos] = verticles[faces[i].av - 1].x;
                VerticleArray[pos + 1] = verticles[faces[i].av - 1].y;
                VerticleArray[pos + 2] = verticles[faces[i].av - 1].z;

                VerticleArray[pos + 3] = textureVerticles[faces[i].at - 1].x;
                VerticleArray[pos + 4] = textureVerticles[faces[i].at - 1].y;
            }
            else if (t == 1)
            {
                VerticleArray[pos + 5] = verticles[faces[i].bv - 1].x;
                VerticleArray[pos + 6] = verticles[faces[i].bv - 1].y;
                VerticleArray[pos + 7] = verticles[faces[i].bv - 1].z;

                VerticleArray[pos + 8] = textureVerticles[faces[i].bt - 1].x;
                VerticleArray[pos + 9] = textureVerticles[faces[i].bt - 1].y;
            }
            else if (t == 2)
            {
                VerticleArray[pos + 10] = verticles[faces[i].cv - 1].x;
                VerticleArray[pos + 11] = verticles[faces[i].cv - 1].y;
                VerticleArray[pos + 12] = verticles[faces[i].cv - 1].z;

                VerticleArray[pos + 13] = textureVerticles[faces[i].ct - 1].x;
                VerticleArray[pos + 14] = textureVerticles[faces[i].ct - 1].y;
            }

            /*for (size_t z = 0; z < 5; z++)
            {
                std::cout << VerticleArray[pos + t * 5 + z] << " ";
            }
            
            std::cout << std::endl;*/
        }

    }

    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glGenBuffers(1, &EBO);

    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(float) * (3 + 2) * 3 * faces.size(), VerticleArray, GL_STATIC_DRAW);

    //glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    //glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(unsigned int) * 3 * faceCount, IndiciesArray, GL_STATIC_DRAW);

    //pos
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    //tex
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(sizeof(float) * 3));
    glEnableVertexAttribArray(1);

    std::cout << "Buffers created!" << std::endl;
	return true;
}

unsigned int ModelLoader::VertexCount()
{
    return faces.size() * 3;
}

std::vector<std::string> ModelLoader::Split(std::string text, char delimiter)
{
    std::vector<std::string> parts;
    parts.push_back("");
    for (unsigned int i = 0; i < text.size(); i++)
    {
        if (text[i] == delimiter)
            parts.push_back("");
        else
            parts[parts.size() - 1] += text[i];
    }

    parts.erase(std::remove(parts.begin(), parts.end(), ""), parts.end());

    return parts;
}
