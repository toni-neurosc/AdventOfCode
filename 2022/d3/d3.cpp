#include <iostream>
#include <string>
#include <vector>
#include <numeric>
#include <algorithm>
#include <iterator>
#include "../include/utils.h"

using namespace std;


int main (int argc, char **argv) 
{
    // Create a string that has all the item types (alpahbet letters) in order of priority
    // To do so, take the ASCII values of the lower and uppercase letters, and add them to string
    int lower_begin = 97;
    int lower_end = 122;
    int upper_begin = 65;
    int upper_end = 90;
    string letters;

    for (int i = lower_begin; i < lower_end + 1; i++) 
    {
        letters.push_back(i);
    }
    for (int i = upper_begin; i < upper_end + 1; i++) 
    {
        letters.push_back(i);
    }

    // Initialize variables to keep track of priority sums
    int prioritiesPart1 = 0;
    int prioritiesPart2 = 0;
    const int N = letters.length(); // Number of item types
    int itemTypeFreq[N] {0}; // How many times a type appears in each elf group
    int elfCount = 0; // Keep track of elf rucksacks analyzed

    // Process input
    vector<string> inputLines = utils::readFileLines(argv[1]);
    for (auto line : inputLines) 
    {
        elfCount++;

        // Part 1
        // Loop through items until we find the type that is in both halves of the string
        // Note: this is complexity O((N^2) with N half-length of string, while doing it 
        // with sets instead is O(N), but I'm new at C++ and I don't know the set syntax 
        for (char& c : line)
        {
            if (line.find(c, line.size()/2) != string::npos) 
            {
                prioritiesPart1 += letters.find(c) + 1; // Find priority of item type and add to total
                break; // Once we found the missplaced type, we're done with this rucksack for Part 1
            }
        }

        // Part 2
        // Get a list of the unique item types carried by this elf
        sort(line.begin(), line.end());
        string itemTypes = string(line.begin(), unique(line.begin(), line.end()));
        // And keep count of the number of elves in this group that carry each type
        for (auto c : itemTypes) {
            itemTypeFreq[letters.find(c)]++;
        }

        // When we reach the third elf of each group, we find the common item type, and reset the count
        if (elfCount % 3 == 0) 
        {
            // Find priority of the item that the common to the 3 elves in the group
            prioritiesPart2 += 1 + distance(itemTypeFreq, find(itemTypeFreq, itemTypeFreq+N, 3));
            fill(itemTypeFreq, itemTypeFreq+N, 0); // Reset item type frequency for next group
        }

    }

    cout << "Solution to Part 1: " << prioritiesPart1 << endl
        << "Solution to Part 2: " << prioritiesPart2;

}