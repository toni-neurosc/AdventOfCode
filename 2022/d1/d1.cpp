#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <numeric>
using namespace std;

int main (int argc, char **argv) 
{
    ifstream inFile(argv[1]);
    string line;
    vector<int> allCalories {0};
    int currentCalories;
    int maxCalories = 0;
    int topThreeCalories = 0;
    
    if ( inFile.is_open() ) 
    {
        while ( getline(inFile,line) ) 
        {
            if ( !line.empty() ) {
                allCalories.back() += stoi(line);

                currentCalories = allCalories.back();
                if ( currentCalories > maxCalories ) {
                    maxCalories = currentCalories;
                }
            } else {
                allCalories.push_back(0);
            }
        }

        nth_element(allCalories.begin(), allCalories.begin() + 2, allCalories.end(), std::greater<int>());
        // for (int i = 0; i < allCalories.size(); i++) { cout << allCalories[i] << endl;}

        topThreeCalories = accumulate(allCalories.begin(), allCalories.begin()+3, 0);

        cout << "Solution to Part 1: " << maxCalories
            << "\nSolution to Part 2: " << topThreeCalories;
    }
}