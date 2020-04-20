#ifndef OBJLOADER_H
#define OBJLOADER_H

#include <string>
#include <vector>

struct FaceData
{
    unsigned int VertexA;
    unsigned int VertexB;
    unsigned int VertexC;

    unsigned int FaceNormal;
};

class ObjLoader
{
    public:
        ObjLoader();
        virtual ~ObjLoader();

        void LoadObjFrom(std::string file);

        std::vector<float>& GetVertices();
        std::vector<unsigned int>& GetIndicies();

        unsigned int GetFaceVertexCount();

    protected:

    private:
        std::vector<float> vertices;
        std::vector<unsigned int> indices;

        std::vector<std::string> Split(std::string text, char delimeter);

        unsigned int FaceCount;
};

#endif // OBJLOADER_H
