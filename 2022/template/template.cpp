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

    int result1 = 0;

    for (auto line : inputLines)
    {

    }

    auto execTime1 = chrono::steady_clock::now() - execStart1;

    auto execStart2 = chrono::steady_clock::now();
    int result2 = 0;
    auto execTime2 = chrono::steady_clock::now() - execStart2;

    cout << "Solution to Part 1: " << "TODO" << " . Execution time: " << execTime1 << endl
         << "Solution to Part 2: " << "TODO" << " . Execution time: " << execTime2;

}
