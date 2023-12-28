#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <regex>
#include <array>
#include "../include/utils.h"
using namespace std;

int manhattan(int x1, int y1, int x2, int y2) {
    return (abs(x1-x2)+abs(y1-y2));
}

vector<array<int,2>> getCoverage(vector<array<int,2>> &sensors,
                                 vector<int> &radius,
                                 int targetY)
{
    vector<array<int,2>> ranges, merged_ranges;

    for (size_t i = 0; i < sensors.size(); i++)
    {
            int& Sx = sensors[i][0];
            int& Sy = sensors[i][1];

        // Get interval of target Y line that is covered by sensor
        int distY = abs(Sy - targetY);

        if  (radius[i] - distY >= 0) {
            int half = radius[i] - distY;
            ranges.push_back({Sx-half, Sx+half});
        } 
    }

    // Sort ranges by start
    sort(ranges.begin(), ranges.end());

    // Merge overlapping intervals
    merged_ranges.push_back(ranges[0]);
    for (size_t i = 1; i < ranges.size(); i++) 
    {
        if (ranges[i][0] <= merged_ranges.back()[1]) {
            merged_ranges.back()[1] = max(ranges[i][1], merged_ranges.back()[1]);
        } else {
            merged_ranges.push_back(ranges[i]);
        }
    }

    return merged_ranges;

}

int main (int argc, char **argv) 
{
    vector<string> inputLines = utils::readFileLines(argv[1]);
    
    auto execStart1 = chrono::steady_clock::now();
    // Read sensor and beacon positions as coordiante pairs
    vector<array<int,2>> sensors, beacons;
    vector<int> radius;

    string coord = "(-?[0-9]+)";
    regex rgx (  "Sensor at x="              + coord 
               + ", y="                      + coord 
               + ": closest beacon is at x=" + coord 
               + ", y="                      + coord);

    for (auto line : inputLines)
    {
        smatch matches;
        regex_search(line, matches, rgx);

        sensors.push_back({stoi(matches[1].str()), stoi(matches[2].str())});
        beacons.push_back({stoi(matches[3].str()), stoi(matches[4].str())});
    }
    // For each sensor and beacon pair, get coverage radius
    for (size_t i = 0; i < sensors.size(); i++)
    {
        // Get manhattan distance between them
        radius.push_back(manhattan(sensors[i][0], sensors[i][1], beacons[i][0],  beacons[i][1]));
    }

    // Part 1

    // int targetY = 10; // Test input
    int targetY = 2000000; // Real input

    // Sum length of all covered intervals
    auto merged_ranges = getCoverage(sensors, radius, targetY);
    int result1 = 0;
    for (auto r: merged_ranges) 
    {
        result1 += r[1] - r[0];
        cout << r[0] << "," << r[1] << endl;
    }

    auto execTime1 = chrono::steady_clock::now() - execStart1;

    // Part 2
    // Can't think of anything faster than  just iterating over all possible lines, and 
    // checking if there is a line that is covered by 2 intervals, in which case
    // the uncovered spot is where the distress beacon must be.
    auto execStart2 = chrono::steady_clock::now();

    unsigned long result2;
    for (int y = 0; y < 4000001; y++) {
        if (y % 100000 == 0) {
            cout << "Looking at y = " << y << "\r" << flush;
        }
        
        auto merged_ranges = getCoverage(sensors, radius, y);
        if (merged_ranges.size() > 1) {
            int x = merged_ranges[0][1]+1;
            cout << "Found distress beacon at location: "
                 << "y = " << y << ", " 
                 << "x = " << x << endl;
            result2 = (unsigned long) x * 4000000 + y;
        }


    }
    auto execTime2 = chrono::steady_clock::now() - execStart2;

    cout << "Solution to Part 1: " << result1 << " . Execution time: " << execTime1 << endl
         << "Solution to Part 2: " << result2 << " . Execution time: " << execTime2;

}
