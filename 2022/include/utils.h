#include <vector> 
#include <fstream>

namespace utils 
{
    std::vector<std::string> readFileLines(std::string path, char delim = '\n', bool skipEmpty = false) 
    { 
        std::vector<std::string> lines;
        std::ifstream inFile(path);
        std::string line;

        while (std::getline(inFile, line, delim)) { 
            if (line.empty() && skipEmpty) continue;
            lines.push_back(line); 
        }
        return lines;
    }

    template <typename T> void print2D(T v) 
    {
        for (auto i : v) {
            for (auto ii : i) { std::cout << ii;}
            std::cout << std::endl;
        }
    }
}
