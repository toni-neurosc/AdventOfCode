#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <chrono>
#include <unordered_map>
#include <climits>
#include <queue>
#include "../include/utils.h"
using namespace std;

template <typename T>
int findInVector(const vector<T> &vec, const T &element) {
    auto it = find(vec.begin(), vec.end(), element);
    if (it != vec.end()) {
        return distance(vec.begin(), it);
    } else {
        return -1;
    }
}

int main (int argc, char **argv) 
{
    auto execStart1 = chrono::steady_clock::now();

    vector<string> inputLines = utils::readFileLines(argv[1]);

    const int N = inputLines.size();

    int result1 = 0;

    vector<string> rooms {};
    vector<int> flowrates {};          
    unordered_map<string, vector<string>> neighbors;
    vector<vector<int>> distMatrix (N, vector<int>(N, 0));


    regex r("Valve ([A-J]{2}) has flow rate=(\\d+); tunnels? leads? to valves? (.+)");

    for (auto line : inputLines)
    {
        smatch matches;
        regex_search(line, matches, r);
        string thisRoom = matches[1].str();
        rooms.push_back(thisRoom);
        string thisTunnels = matches[3].str();
        flowrates.push_back(stoi(matches[2].str()));
        neighbors[thisRoom] = vector<string> {};
        for (size_t i = 0; i < thisTunnels.length(); i+=4)
        {
            neighbors[thisRoom].push_back(thisTunnels.substr(i, 2));
        }
    }
    
    // Build min distance matrix by running BFS for all nodes
    for (size_t i = 0; i < rooms.size(); i++)
    {   
        string startingRoom = rooms[i];
        distMatrix[i][i] = 0;

        vector<string> visited {};
        queue<string> nextRooms {};
        nextRooms.push(startingRoom);
        
        while (!nextRooms.empty()) {
            string currentRoom = nextRooms.front();
            nextRooms.pop();
            int currentIndex = findInVector(rooms, currentRoom);
            vector<string> adjRooms = neighbors[currentRoom];
            for (auto room : adjRooms) {
                if (findInVector(visited, room) == -1) {
                    int adjIndex = findInVector(rooms, room);
                    nextRooms.push(room);
                    distMatrix[i][adjIndex]  = distMatrix[i][currentIndex] + 1;
                }
            }
            visited.push_back(currentRoom);
        }
    }

    for (auto r:rooms) {cout << r << " ";}
    cout<<endl;
    utils::print2D(distMatrix);
 
    int clock = 30;
    string currentRoom = "AA";
    int currentIndex = findInVector(rooms, currentRoom);
    vector<int> open;
    int totalYield = 0;
    while (clock > 4) {
        int maxYield = 0, maxRoom, maxTime;
        for (int i = 0; i < rooms.size(); i++) {
            if (findInVector(open, i) != -1) {
                continue;
            }
            int openTime = clock - (distMatrix[currentIndex][i] + 1);
            if (openTime > clock) {
                continue;
            }
            int yield = flowrates[i] * openTime;
            if (yield > maxYield) {
                maxYield = yield;
                maxRoom = i;
                maxTime = openTime;
            }
        }
        open.push_back(maxRoom);
        currentIndex = maxRoom;
        totalYield += maxYield;
        clock = maxTime;
        cout << clock << endl;
    }

    for (auto r:open) {cout << r << " ";}


    auto execTime1 = chrono::steady_clock::now() - execStart1;

    auto execStart2 = chrono::steady_clock::now();
    int result2 = 0;
    auto execTime2 = chrono::steady_clock::now() - execStart2;

    cout << "Solution to Part 1: " << totalYield << " . Execution time: " << execTime1 << endl
         << "Solution to Part 2: " << "TODO" << " . Execution time: " << execTime2;

}
