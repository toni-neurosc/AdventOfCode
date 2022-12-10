#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <regex>
#include <array>
#include <unordered_map>

#include "../include/utils.h"
using namespace std;

int getSize(array<string,2> item, auto& fileTreeMap, auto& dirSizeMap) {
    // Recursive function to get the size of a directory 
    
    string itemType = item[0];
    string itemName = item[1];
    if (itemType == "dir") {
        if (dirSizeMap.contains(itemName)) {
            return dirSizeMap[itemName];
        } 

        int totalSize = 0;

        for (array<string,2> content : fileTreeMap[itemName]) {
            if (content[0] == "dir") {
                content[1] = itemName + content[1] + "/";
            }
            totalSize += getSize(content, fileTreeMap, dirSizeMap);
        }
        
        return totalSize;
    } else {
        return stoi(itemType);
    }
}

int main (int argc, char **argv) 
{
    auto execStart = chrono::steady_clock::now();

    unordered_map<string, vector<array<string,2>>> fileTreeMap;
    unordered_map<string, int> dirSizeMap;
    
    vector<string> inputLines = utils::readFileLines(argv[1]);
    
    string currentDir {};

    for (auto line : inputLines) {
        
        if (line[0]=='$') {
            string command = line.substr(2,2);
            if (command == "cd") {
                string arg = line.substr(5);
                if (arg == "..") {
                    currentDir = currentDir.substr(0,currentDir.find_last_of('/', currentDir.size()-2)+1);
                } else if (arg == "/") {
                    currentDir = "/";
                } else {
                    currentDir += arg + "/";
                }
            }
        } else {
            int delimPos = line.find_first_of(" ");
            string size = line.substr(0, delimPos);
            string content = line.substr(delimPos+1);
            array<string,2> entry {size,content};
            if (fileTreeMap.contains(currentDir)) {
                fileTreeMap[currentDir].push_back(entry);
            } else {
                fileTreeMap[currentDir] = vector<array<string,2>> {entry};
            }
        }
    }

    // for (auto [dir, contents] : fileTreeMap) {
    //     cout << "Folder: " << dir << ". " << "Contents: " << endl;
    //     for (auto e : contents) {
    //         cout << e[0] << " : " << e[1] << endl;
    //     }
    //     cout<<endl;
    // }
    
    for (auto& [dir, contents]: fileTreeMap) {
        if (!dirSizeMap.contains(dir)) {
            dirSizeMap[dir] = getSize(array<string,2> {"dir", dir}, fileTreeMap, dirSizeMap);
        }
        
    }

    int result1 = 0;
    int minSize = 30000000 - (70000000 - dirSizeMap["/"]);
    cout << "Need to delete " << minSize << endl;
    int result2 = 70000001;
    for (auto const& [dir, dirSize]: dirSizeMap) {
        if (dirSize <= 100000) {
            result1 += dirSize;
        }
        if (dirSize >= minSize && dirSize < result2) {
            result2 = dirSize;
        }
        cout << "Folder: " << dir << ". Size: " << dirSize << endl;
    }

    auto execTime = chrono::steady_clock::now() - execStart;

    cout << "Solution to Part 1: " << result1 << endl
         << "Solution to Part 2: " << result2 << endl
         << "Execution time: " << execTime;

}