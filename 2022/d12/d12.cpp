#include <iostream>
#include <vector>
#include <chrono>
#include <set>
#include <array>
#include <queue>
#include <map>
#include <climits>
#include <string>
#include "../include/utils.h"
using namespace std;


int findShortestPath(vector<string> heightmap, bool part2 = false) {

    // Find start and ending positions
    array<int,2> startPos, endPos;
    for (int i = 0; i < heightmap.size(); i++)
    {
        if (heightmap[i].find('S') != string::npos) {
            int pos = heightmap[i].find('S');
            heightmap[i][pos] = 'a';
            startPos = array<int,2> {i, pos};
        }
        if (heightmap[i].find('E') != string::npos) {
            int pos = heightmap[i].find('E');
            heightmap[i][pos] = 'z'; 
            endPos = array<int,2> {i, pos};
        }
    }
    if (part2) {startPos = endPos;}
    char endChar = (part2) ? 'a' : 'E';

    int shortestDistance; 
    const int H = heightmap.size(), W = heightmap[0].length(); // Get map dimensions
    set<array<int,2>> visited; // Set to store visited nodes
    map<array<int,2>,int> distances; // Map to store minimum distance to start

    // Construct priority queue to store positions as graph nodes
    struct customLess {
        bool operator() (array<int,4> l, array<int,4> r) { return l[1] > r[1]; } // Will store distance at [1] position
    };
    priority_queue<array<int,4>, vector<array<int,4>>, customLess> nodeQueue;

    // Now, implement modified Dijkstra algorithm to find shortest path 

    array<int,4> startNode {heightmap[startPos[0]][startPos[1]], 0, startPos[0], startPos[1]}, currentNode; // [value, steps, y, x]
    nodeQueue.push(startNode); // Priority queue to store nodes to visit
    distances[startPos] = 0;

    // Vector of possible moves from current position
    vector<array<int,2>> directions {{1, 0}, {-1, 0}, {0, 1}, {0, -1} }; // Up, down, right, left

    bool finished = false;
    while (!finished) 
    {
        // Select new position from the queue
        currentNode = nodeQueue.top();
        nodeQueue.pop();
        array<int,2> currentPos {currentNode[2], currentNode[3]};

        // Since we're not updating the queue, but rather adding redundant moves, 
        // skip candidate move is distance is lower than recorded
        // Not necessary since we have a destination node, but yes for full graph exploration
        if (currentNode[1] > distances[currentPos]) { continue; }

        // Find neighbors
        for (auto d : directions) {
            array<int,2> newPos {currentPos[0]+d[0], currentPos[1]+d[1]};
            int newY = newPos[0], newX = newPos[1];

            // Find "neighbors" of current node
            if (   !visited.contains(newPos) // Skip visited positions
                && newY >= 0 && newY < H // avoid falling off the grid
                && newX >= 0 && newX < W ) {
                    
                // Move only up to 1 higher or lower
                if (  (!part2 && heightmap[newY][newX] - currentNode[0] > 1)
                    ||( part2 && heightmap[newY][newX] - currentNode[0] < -1) ) {continue;}
                
                if (heightmap[newY][newX] == endChar || newPos == endPos) {
                    // If we reach the end position, we're done
                    shortestDistance = currentNode[1]+1;
                    finished = true;
                    break;
                }

                int newDist = currentNode[1] + 1;
                int oldDist = (distances.contains(newPos)) ? distances[newPos] : INT_MAX;
                // If new distance to neighbor is less than recorded
                if (newDist < oldDist) {
                    // update distance and update priority by pushing new element to queue
                    distances[newPos] = newDist;
                    array<int, 4> newNeighbor {heightmap[newY][newX], newDist, newY, newX};
                    nodeQueue.push(newNeighbor);
                }
            }
        }
        visited.insert(currentPos);
    }
    return shortestDistance;
}

int main (int argc, char **argv) 
{
    auto execStart1 = chrono::steady_clock::now();

    vector<string> inputLines = utils::readFileLines(argv[1]);

    int result1 = findShortestPath(inputLines);
    auto execTime1 = chrono::steady_clock::now() - execStart1;

    auto execStart2 = chrono::steady_clock::now();
    int result2 = findShortestPath(inputLines, true);
    auto execTime2 = chrono::steady_clock::now() - execStart2;

    cout << "Solution to Part 1: " << result1 << " . Execution time: " << execTime1 << endl
         << "Solution to Part 2: " << result2 << " . Execution time: " << execTime2;
}
