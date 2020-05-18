#ifndef ARGPARSER_HPP_INCLUDED
#define ARGPARSER_HPP_INCLUDED

#include <string>
#include <sstream>

class ArgParser
{
public:
    ArgParser(int argc, char** argv) : windowSize(512), fileName("mesh.obj")
    {
        for (int i = 0; i < argc; i++)
        {
            if (!i)
                continue;
            if (argv[i] == "-size" || argv[i] == "--S")
            {
                std::stringstream ss;
                ss.str(argv[i + 1]);
                ss >> windowSize;
                i++;
            }
            else if (argv[i] == "-file" || argv[i] == "--F")
            {
                fileName = argv[i + 1];
                i++;
            }
        }
    }
    ~ArgParser(){}

    unsigned int GetSize() {return windowSize;}
    std::string GetFileName() {return fileName;}

private:
    unsigned windowSize;
    std::string fileName;
};

#endif // ARGPARSER_HPP_INCLUDED
