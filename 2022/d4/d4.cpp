#include <iostream>
#include <string>
#include <vector>
#include "../include/utils.h"

using namespace std;


int main (int argc, char **argv) 
{
    int result1 = 0;
    int result2 = 0;
    string delim = "-,";

    vector<string> inputLines = utils::readFileLines(argv[1]);
    for (auto line : inputLines) 
    {
        vector<int> sections;
        int start = 0;
        while (start < line.length()) 
        {
            int end = line.find_first_of(delim, start);
            sections.push_back(stoi(line.substr(start, end - start)));
            if (end != line.npos) {start = end + 1 ;} else {break;}
        }

        // Part 1: check if distance between left edges of both ranges 
        // is opposite sign of distance between right edges, or if either is 0
        int loffset = sections[0] - sections [2];
        int roffset = sections[1] - sections [3];
        if   ((loffset <= 0 && roffset >= 0)||(roffset <= 0 && loffset >= 0)) 
        {
            result1++;
        } 
        // Alternative solution, may lead to too big integers
        // if (loffset * roffset <= 0) {result1++;} 
        
        // Part 2: check if left edge of one range is rigth of right edge of the other
        if (!( (sections[1] - sections [2] < 0)||(sections[3] - sections [0] < 0)))
        {
            result2++;
        }
    }
    cout << "Solution to Part 1: " << result1 << endl
         << "Solution to Part 2: " << result2;

}