#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include "../include/utils.h"
using namespace std;

int main (int argc, char **argv) 
{
    auto execStart1 = chrono::steady_clock::now();

    vector<string> inputLines = utils::readFileLines(argv[1]);

    int cycle = 0;
    int line = 0;
    int X = 1;
    int result1 = 0;
    bool wait = true;
    while (line < inputLines.size()) 
    {
        cycle += 1;
        
        // Calculate signal strength
        if ((cycle + 20) % 40 == 0) {
            // cout << "Cycle: " << cycle << ". X: " << X << ". Signal strength: " << X * cycle << endl;
            result1 += X * cycle;
        }

        // Draw pixel 
        int pixel = cycle % 40 - 1;
        string output = (pixel < X + 2 && pixel > X - 2) ? "██" : "░░" ;
        cout << output;
        if (cycle % 40 == 0) {cout<<"\n";}

        // Execute instruction
        if (wait) {
            wait = false;
            continue;
        }

        string instruction = inputLines[line].substr(0,4);

        if (instruction == "addx") {
            X += stoi(inputLines[line].substr(5));
            wait = true;
        }
        
        line += 1;
    }

    auto execTime1 = chrono::steady_clock::now() - execStart1;

    cout << endl;
    cout << "Solution to Part 1: " << result1 << endl << "Execution time: " << execTime1 << endl;
}