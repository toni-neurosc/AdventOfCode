#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <functional>
#include <algorithm>
#include <numeric>
#include "../include/utils.h"
using namespace std;

int main (int argc, char **argv) 
{
    auto execStart1 = chrono::steady_clock::now();

    vector<string> inputLines = utils::readFileLines(argv[1]);
    
    vector<function<unsigned long(unsigned long)>> inspectFunctions;
    vector<vector<unsigned long>> currentItems;
    vector<int> divisors, targetsTrue, targetsFalse;
    const int ROUNDS = 20;
    // const int ROUNDS = 10;


    size_t i = 0;
    while (i < inputLines.size())
    {
        // Read starting items
        string itemString = inputLines[i+1].substr(18);
        vector<unsigned long> thisItems;
        size_t last = 0, next;
        while ((next = itemString.find(',', last)) != string::npos) {
                thisItems.push_back(stoi(itemString.substr(last, next-last)));
            last = next + 1;    
        }
        thisItems.push_back(stoi(itemString.substr(last)));
        currentItems.push_back(thisItems);

        // Read inspect operation
        char op = inputLines[i+2][23];
        string secondTerm = inputLines[i+2].substr(25);
        function<unsigned long(unsigned long)> fun;
        if (secondTerm == "old") {
            fun = [](int a) {return a*a;};
        } else if (op == '*') {
            fun = [secondTerm](int a) {return a * stoi(secondTerm);};
        } else if (op == '+') {
            fun = [secondTerm](int a) {return a + stoi(secondTerm);};
        }
        inspectFunctions.push_back(fun);

        // Read worry level test
        divisors.push_back(stoi(inputLines[i+3].substr(21)));
        targetsTrue.push_back(stoi(inputLines[i+4].substr(29)));
        targetsFalse.push_back(stoi(inputLines[i+5].substr(30)));

        i += 7;
    }

    const int DIV = accumulate(divisors.begin(), divisors.end(), 1, multiplies<int>{});
    cout << "DIV=" <<DIV;

    const int MONKEYS = currentItems.size();
    vector<int> activity(MONKEYS, 0);
    for (size_t r = 0; r < ROUNDS; r++)
    { // Run for each monkey
        for (size_t m = 0; m < MONKEYS; m++)
        { // Then for each item it's holding
            for (size_t i = 0; i < currentItems[m].size(); i++) {
                // Inspect item
                // unsigned long thisItem = inspectFunctions[m](currentItems[m][i]) / 3;
                
                unsigned long thisItem = inspectFunctions[m](currentItems[m][i]);
                // thisItem = (thisItem % DIV + DIV) % DIV;
                activity[m]++;          
                // Test worry level and throw item
                int targetMonkey = (thisItem % divisors[m] == 0) ? targetsTrue[m] : targetsFalse[m];
                unsigned long newItem = (thisItem % DIV + DIV) % DIV;

                if ((currentItems[m][i] % divisors[m]) != (newItem % divisors[m])) {
                    cout << "Modulo changed: " << endl;
                    cout << currentItems[m][i] << "%" << divisors[m] << "=" << currentItems[m][i] % divisors[m] << endl;
                    cout << thisItem << "%" << divisors[m] << "=" << thisItem % divisors[m] << endl;

                    cout << newItem << "%" << divisors[m] << "=" << newItem % divisors[m] << endl;

                }
                
                currentItems[targetMonkey].push_back(newItem);
            }
            currentItems[m].clear(); // Empty current monkey item list
        }
    }

    cout << "After round " << ROUNDS << " the monkeys are holding items with these worry levels:" << endl;
    for (size_t i = 0; i < MONKEYS; i++)
    {
        cout << "Monkey " << i << ":";
        for (unsigned long item : currentItems[i]) {
            cout << item << ", ";
        }
        cout << endl << "Monkey " << i << " inspected items " << activity[i] << " times." << endl;
    }

    sort(activity.begin(), activity.end(), greater());
    int result1 = activity[0] * activity[1];

    auto execTime1 = chrono::steady_clock::now() - execStart1;

    auto execStart2 = chrono::steady_clock::now();
    int result2 = 0;
    auto execTime2 = chrono::steady_clock::now() - execStart2;

    cout << "Solution to Part 1: " << result1 << " . Execution time: " << execTime1 << endl
         << "Solution to Part 2: " << "TODO" << " . Execution time: " << execTime2;

}
