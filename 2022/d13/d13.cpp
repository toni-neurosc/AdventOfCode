#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include "../include/utils.h"
using namespace std;

vector<string> getListElements(string list) {
    vector<string> elements;
    list = list.substr(1, list.length() - 2);
    size_t start = 0, pos = list.find(',');
    while (pos != string::npos) {
        elements.push_back(list.substr(start, pos-start));
        start = pos + 1;
        pos = list.find(',', start);
    }
    elements.push_back(list.substr(start));
    return elements;
}

int main (int argc, char **argv) 
{
    auto execStart1 = chrono::steady_clock::now();

    vector<string> inputLines = utils::readFileLines(argv[1]);

    int result1 = 0;

    for (auto line : inputLines)
    {
        if (!line.empty()) {
            vector<string> subelements = getListElements(line);
            for (auto el : subelements) { cout<<el<<" | ";}
        }
        cout<< endl;
    }

    auto execTime1 = chrono::steady_clock::now() - execStart1;

    auto execStart2 = chrono::steady_clock::now();
    int result2 = 0;
    auto execTime2 = chrono::steady_clock::now() - execStart2;

    cout << "Solution to Part 1: " << "TODO" << " . Execution time: " << execTime1 << endl
         << "Solution to Part 2: " << "TODO" << " . Execution time: " << execTime2;

}
