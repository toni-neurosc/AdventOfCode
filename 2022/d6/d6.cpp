#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <chrono>
#include "../include/utils.h"
using namespace std;

int findMarker_slow(string message, int len, int* iterCount)
/* 
    Quick and dirty solution, sliding window along input,
    counting for each position the frequency of that char in
    the window. Sum of frequencies should be length of window for
    substring of unique characters. 

    Complexity is O(N*M^2), N length of input, M length of window.
    For my input, takes 672476 iterations. Awful.

    Using sets, worst case complexity would be O(N*M). 
    For my input, takes 48034 iterations
*/
{
    int position = 0;
    for (int i = 0; i < message.length() - len; i++)
    {
        string ss = message.substr(i, len);
        int freqSum = 0;
        for (char ch : ss)
        {
            *iterCount += len; // To include comparisons made by std::count
            // (*iterCount)++; // Iteration count if using sets
            freqSum += count(ss.begin(), ss.end(), ch);
        }
        if (freqSum == len) {
            position = i + len;
            break;
        }
    }
    return position;

}

int findMarker(string message, int len, int* iterCount)
/*
    I tried to use the position of the repeated character to my advantage,
    but only got to the correct solution after stealing the idea of using
    a dynamic window size and extending it until reachinig the desired length,
    rather than using a fixed size of window like I was trying to do.

    This solution starts with a window of 1 length and extends it as long as the
    new character is not already in the string. If it's already in it, the start of 
    the window jumps to right after the repeated character, discarding all 
    preceding characters and saving a lot of processing. 
    Stops when desired length is reached. Could also use std::find
    for code simplicity, but this is probably more efficient

    Worst case complexity O(N*M) if I'm not mistaken, but average case much better.
    For my input, takes 11623 iterations.
*/
{
    int start = 0;
    int end   = 0; 
    while (end-start<len-1 && end < message.length())
    {
        // Check that all chars are different than next
        for (int i = start; i <= end; i++) 
        {
        (*iterCount)++;
            // If a char in window appears again, advance past it
            if (message[i] == message[end+1]) 
            {
                start = i+1; // Start after repeated char
                break; // Start for loop again with new start
            }
        }
        end++; // If next char is not present, extend window by 1    
    }
    return end+1; // Fix 0-index
}

int main (int argc, char **argv) 
{
    vector<string> inputLines = utils::readFileLines(argv[1]);
    string input = inputLines[0];

    int iterCount1 = 0;
    auto execStart1 = chrono::steady_clock::now();
    int result1 = findMarker(input, 4, &iterCount1);
    auto execTime1 = chrono::steady_clock::now() - execStart1;

    int iterCount2 = 0;
    auto execStart2 = chrono::steady_clock::now();
    int result2 = findMarker(input, 14, &iterCount2);
    auto execTime2 = chrono::steady_clock::now() - execStart2;

    cout << "Solution to Part 1: " << result1 << ". Execution time: " << execTime1 
         << ". Iterations: " << iterCount1 << endl
         << "Solution to Part 2: " << result2 << ". Execution time: " << execTime2
         << ". Iterations: " << iterCount2;

}