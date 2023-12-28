#include <iostream>
#include <vector>
#include <chrono>
#include <array>
#include <set>
#include <regex>
#include <string>
#include "../include/utils.h"
using namespace std;


void addPoints (array<int,2> origin, array<int,2> dest, set<array<int, 2>> &pointSet) {
    int dim = (origin[0] == dest[0]) ? 1 : 0 ; // Variable dimension

    // cout << "Origin: [" << origin[0] << "," << origin[1] << "]. Destination: [" 
    //                     << dest[0]   << "," << dest[1]   << "]." << endl;

    int start = min(origin[dim], dest[dim]);
    int end = max(origin[dim], dest[dim]);
    // std::cout << "Generating points from " 
    //           << start << " to " << end << endl;        for(auto i = sregex_iterator(line.begin(), line.end(), num);


    for (int i = 0; i < end-start+1 ; i++){
        array<int, 2> point;
        point[dim] = start+i;
        point[1-dim] = origin[1-dim];
        pointSet.insert(point);
        // std::cout << point[0] << ", " << point[1] << endl;
    }
}

int main (int argc, char **argv) 
{
    auto execStart = chrono::steady_clock::now();

    vector<string> inputLines = utils::readFileLines(argv[1]);
    vector<vector<int>> rockPaths;
    regex num("[0-9]+");

    for (auto line : inputLines)
    {
        vector<int> path;
                 i != std::sregex_iterator(); i++) 
        {
            smatch m = *i;
            path.push_back(stoi(m.str()));
        }  
        rockPaths.push_back(path);         
    }

    set<array<int, 2>> blockedPoints;

    for (auto path : rockPaths) {
        for (size_t i = 0; i < path.size() - 3; i+=2)
        {
            array<int,2> origin = {path[i], path[i+1]};
            array<int,2> dest = {path[i+2], path[i+3]};
            addPoints(origin, dest, blockedPoints);
        }
    }

    int maxY = 0;
    for (auto p: blockedPoints) {
        if (p[1] > maxY) {maxY = p[1];}
        // cout << "[" << p[0] << "," << p[1] << "], ";
    }
    array<int,2> startPos {500,0}, sandPos = startPos, nextPos;

    int sandCount = 0;
    int result1 = 0, result2;
    while (true) {
        
        if (sandPos[1] > maxY && result1 == 0) {
            // If sand goes past last horizontal line, part 1 finished
            result1 = sandCount;
        }

        nextPos = sandPos;
        nextPos[1] += 1 ; // Try one down

        if (nextPos[1] == maxY + 2) {
            // If you reached the floor, let sand stay there
            blockedPoints.insert(sandPos); // Occupy point
            sandPos = startPos; // Reset position
            sandCount++; // Incrase sand count
            continue;
        }
        if (blockedPoints.contains(nextPos)) {
            // If one down is not possible
            nextPos[0] -= 1; // Try down left
        } 
        if (blockedPoints.contains(nextPos)) {
            // If down and left is not possible
            nextPos[0] += 2; // Try down right
        }
        if (blockedPoints.contains(nextPos)) {
            // If no moves are possible or floor has been reached
            if (sandPos == startPos) {
                // If the sand has stopped at start, part 2 finished
                result2 = ++sandCount;
                break;
            }
            blockedPoints.insert(sandPos); // Occupy point
            sandPos = startPos; // Reset position
            sandCount++; // Incrase sand count
            continue;
        }
        sandPos = nextPos;
    }
    
    auto execTime = chrono::steady_clock::now() - execStart;

    std::cout << "Solution to Part 1: " << result1 << endl
         << "Solution to Part 2: " << result2 << endl
         << "Execution time: " << execTime;

}
