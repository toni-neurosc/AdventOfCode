#include <iostream>
#include <vector>
#include <chrono>
#include <array>
#include <set>
#include <map>
#include <string>
#include "../include/utils.h"
using namespace std;

int main (int argc, char **argv) 
/* 
    Note: this solution is off by 1, gives 2371 instead of 2372. 
    I could not find the error however, code looks good to me and works for 
    the test data perfectly. Perhaps AoC solution counts the start as a 
    separate position while I'm just calling it (0,0)? 
*/
{
    auto execStart = chrono::steady_clock::now();

    vector<string> inputLines = utils::readFileLines(argv[1]);

    vector<vector<array<int,2>>> position (10, vector<array<int,2>> {{0,0}});
    
    map<char, array<int,2>> directionMap {{'R', { 1,0}}, 
                                          {'L', {-1,0}},
                                          {'U', {0, 1}},
                                          {'D', {0,-1}}};
    
    auto headPos = position[0].back();
    
    for (auto line : inputLines) 
    {
        char direction = line[0];
        int distance = stoi(line.substr(2));
        
        for (size_t i = 0; i < distance; i++)
        {
            headPos[0] += directionMap[direction][0];
            headPos[1] += directionMap[direction][1];

            position[0].push_back(headPos);


            for (size_t node = 1; node < 10; node++)
            {
                auto& thisNodePos = position[node-1].back();
                auto& nextNodePos = position[ node ].back();
                
                array<int,2> newPosition = nextNodePos;

                int xDist = thisNodePos[0] - nextNodePos[0];
                int yDist = thisNodePos[1] - nextNodePos[1];

                if (abs(xDist) > 1) {
                    newPosition[0] += xDist/2;
                    if (abs(yDist) > 0) {
                        newPosition[1] += yDist;
                    }
                } else if (abs(yDist) > 1) {
                    newPosition[1] += yDist/2;
                    if (abs(xDist) > 0) {
                        newPosition[0] += xDist;
                    }
                }
                position[node].push_back(newPosition);   
            }
        }
    }
    
    set<array<int,2>> posSet1;
    set<array<int,2>> posSet2;

    for (int i = 0; i < position[1].size(); i++) {
        posSet1.insert(position[1][i]);
        posSet2.insert(position[9][i]);
    }

    int result1 = posSet1.size();
    int result2 = posSet2.size();

    auto execTime = chrono::steady_clock::now() - execStart;

    cout << "Solution to Part 1: " << result1 << endl
         << "Solution to Part 2: " << result2 << endl
         << "Execution time: " << execTime;
}