#pragma once

#include <string>
#include <vector>

struct Verticle
{
	float x;
	float y;
	float z;
};

struct Face
{
	unsigned int av;
	unsigned int at;
	unsigned int an;

	unsigned int bv;
	unsigned int bt;
	unsigned int bn;

	unsigned int cv;
	unsigned int ct;
	unsigned int cn;
};

class ModelLoader
{
public:
	ModelLoader();
	~ModelLoader();

	bool StartLoading(std::string file, unsigned int& texture, unsigned int& VAO, unsigned int& VBO, unsigned int& EBO);

	bool LoadModel(std::string file);
	bool LoadTextures(unsigned int& texture);
	bool CreateBuffers(unsigned int& VBO, unsigned int& VAO, unsigned int& EBO);

	unsigned int VertexCount();

private:
	float* VerticleArray;
	unsigned int* IndiciesArray;
	std::string texturePath;

	std::vector<Verticle> verticles;
	std::vector<Verticle> normalVerticles;
	std::vector<Verticle> textureVerticles;
	std::vector<Face> faces;

	std::vector<std::string> Split(std::string text, char delimiter = ' ');

};

