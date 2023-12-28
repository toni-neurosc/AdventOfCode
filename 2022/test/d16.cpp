#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <chrono>
#include <unordered_map>
#include "../include/utils.h"
using namespace std;

int main (int argc, char **argv) 
{
    auto execStart1 = chrono::steady_clock::now();

    vector<string> inputLines = utils::readFileLines(argv[1]);

    int result1 = 0;

    unordered_map<string, int> flowrates;
    unordered_map<string, vector<string>> neighbors;


    regex r("Valve ([A-J]{2}) has flow rate=(\\d+); tunnels? leads? to valves? (.+)");

    for (auto line : inputLines)
    {
        smatch matches;
        regex_search(line, matches, r);
        string thisRoom = matches[1].str();
        string thisTunnels = matches[3].str();
        flowrates[thisRoom] = stoi(matches[2].str());
        neighbors[thisRoom] = vector<string> {};
        for (size_t i = 0; i < thisTunnels.length(); i+=4)
        {
            neighbors[thisRoom].push_back(thisTunnels.substr(i, 2));
        }
        
    }

    for (auto &[k,v] : neighbors) {
        cout << k << ": ";
        for (auto s:v) {
            cout << s << ", ";
        }
        cout << endl;
    }

    auto execTime1 = chrono::steady_clock::now() - execStart1;

    auto execStart2 = chrono::steady_clock::now();
    int result2 = 0;
    auto execTime2 = chrono::steady_clock::now() - execStart2;

    cout << "Solution to Part 1: " << "TODO" << " . Execution time: " << execTime1 << endl
         << "Solution to Part 2: " << "TODO" << " . Execution time: " << execTime2;

}
