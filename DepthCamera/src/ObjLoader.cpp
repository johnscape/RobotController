#include "ObjLoader.h"
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <iostream>
#include <fstream>
#include <sstream>

ObjLoader::ObjLoader()
{

}

ObjLoader::~ObjLoader()
{
    //dtor
}

void ObjLoader::LoadObjFrom(std::string file)
{
    std::cout << "Loading " << file << std::endl;
    std::ifstream reader;
    reader.open(file);
    if (!reader.is_open())
    {
        std::cout << "Cannot open file " << file << "!" << std::endl;
        return;
    }

    std::vector<glm::vec3> temp_vertex;
    std::vector<glm::vec3> temp_normal;

    std::vector<FaceData> faceData;

    while (reader.good())
    {
        std::string line, first;
        std::stringstream ss;
        std::getline(reader, line);
        ss.str(line);
        ss >> first;
        if (first[0] == '#' || first == "usemtl" || first == "mtllib")
            continue;

        if (first == "v")
        {
            //itt egy vertex van
            glm::vec3 vertex;
            ss >> vertex.x >> vertex.y >> vertex.z;
            temp_vertex.push_back(vertex);
            temp_normal.push_back(glm::vec3(0.0f));
        }
        else if (first == "f")
        {
            std::string v1, v2, v3, segment;
            ss >> v1 >> v2 >> v3;
            FaceData d;
            //std::stringstream textToInt1, textToInt2, textToInt3;

            //std::vector<std::string> parts;
            /*std::vector<std::string> splitted = Split(v1, '/');
            textToInt1.str(splitted[0]);
            textToInt1 >> d.VertexA;

            splitted = Split(v2, '/');
            textToInt2.str(splitted[0]);
            textToInt2 >> d.VertexB;

            splitted = Split(v3, '/');
            textToInt3.str(splitted[0]);
            textToInt3 >> d.VertexC;*/
            d.VertexA = std::stoi(Split(v1, '/')[0]);
            d.VertexB = std::stoi(Split(v2, '/')[0]);
            d.VertexC = std::stoi(Split(v3, '/')[0]);



            d.VertexA--;
            d.VertexB--;
            d.VertexC--;
            //generate normal
            glm::vec3 normal, u, v;
            u = temp_vertex[d.VertexB] - temp_vertex[d.VertexA];
            v = temp_vertex[d.VertexC] - temp_vertex[d.VertexA];

            normal.x = (u.y * v.z) - (u.z * v.y);
            normal.y = (u.z * v.x) - (u.x * v.z);
            normal.z = (u.x * v.y) - (u.y * v.x);

            temp_normal.push_back(normal);
            d.FaceNormal = temp_normal.size() - 1;
            faceData.push_back(d);
        }
    }

    vertices.clear();
    indices.clear();
    for (FaceData f : faceData)
    {
        vertices.push_back(temp_vertex[f.VertexA].x);
        vertices.push_back(temp_vertex[f.VertexA].y);
        vertices.push_back(temp_vertex[f.VertexA].z);

        vertices.push_back(temp_normal[f.FaceNormal].x);
        vertices.push_back(temp_normal[f.FaceNormal].y);
        vertices.push_back(temp_normal[f.FaceNormal].z);

        vertices.push_back(temp_vertex[f.VertexB].x);
        vertices.push_back(temp_vertex[f.VertexB].y);
        vertices.push_back(temp_vertex[f.VertexB].z);

        vertices.push_back(temp_normal[f.FaceNormal].x);
        vertices.push_back(temp_normal[f.FaceNormal].y);
        vertices.push_back(temp_normal[f.FaceNormal].z);

        vertices.push_back(temp_vertex[f.VertexC].x);
        vertices.push_back(temp_vertex[f.VertexC].y);
        vertices.push_back(temp_vertex[f.VertexC].z);

        vertices.push_back(temp_normal[f.FaceNormal].x);
        vertices.push_back(temp_normal[f.FaceNormal].y);
        vertices.push_back(temp_normal[f.FaceNormal].z);

        indices.push_back(f.VertexA);
        indices.push_back(f.VertexB);
        indices.push_back(f.VertexC);
    }

    FaceCount = faceData.size();

    std::cout << "Finished loading!" << std::endl;
}

std::vector<float>& ObjLoader::GetVertices()
{
    return vertices;
}

std::vector<unsigned int>& ObjLoader::GetIndicies()
{
    return indices;
}

std::vector<std::string> ObjLoader::Split(std::string text, char delimeter)
{
    std::stringstream ss(text);
    std::string item;
    std::vector<std::string> splittedStrings;
    while (std::getline(ss, item, delimeter))
        splittedStrings.push_back(item);
    return splittedStrings;
}

unsigned int ObjLoader::GetFaceVertexCount()
{
    return FaceCount * 3;
}

