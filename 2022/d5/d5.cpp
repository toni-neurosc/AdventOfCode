#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <regex>
#include "../include/utils.h"
using namespace std;

string moveCrates(vector<string> stacks, vector<int> instructions, int part) 
{
    string result = "";

    for (int i=0; i != instructions.size() ; i+=3) 
    {
        int amount = instructions[i];
        int origin = instructions[i+1]-1;
        int dest   = instructions[i+2]-1;

        string movedCrates = stacks[origin].substr(0, amount);
        if (part == 1) {
            reverse(movedCrates.begin(), movedCrates.end());
        }
        stacks[origin] = stacks[origin].substr(amount);
        stacks[dest]   = movedCrates + stacks[dest];
    }

    for (auto s : stacks) {
        result.push_back(s[0]);
    }

    return result;
}

int main (int argc, char **argv) 
{
    bool isDrawing = true;
    regex pattern("\\d+");
    vector<int> instructions {};
    vector<string> inputLines = utils::readFileLines(argv[1]);
    int numStacks = (inputLines[0].length()+1)/4;
    vector<string> stacks(numStacks);

    for (auto line : inputLines) 
    {
        if (line.empty()) {
            isDrawing = false;
            continue;
        }

        if (isDrawing) {
            for (int i = 0; i < line.length(); i++) {
                char ch = line[i];
                if (ch >= 64 && ch <= 90) {
                    int pos = i/4;
                    stacks[pos].push_back(ch);
                }
            }
        } else {
            for (auto i = sregex_iterator(line.begin(), line.end(), pattern); i != sregex_iterator(); i++) {
                smatch match = *i;
                instructions.push_back(stoi(match.str()));
            }
        }
    }

    string result1 = moveCrates(stacks, instructions, 1);
    string result2 = moveCrates(stacks, instructions, 2);

    cout << "Solution to Part 1: " << result1 << endl
         << "Solution to Part 2: " << result2;

}