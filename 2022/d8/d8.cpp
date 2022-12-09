#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include "../include/utils.h"
using namespace std;

int main (int argc, char **argv) 
{    
    vector<string> inputLines = utils::readFileLines(argv[1]);

    // Store input as 2D vector of integers
    int N = inputLines[0].length();
    vector<vector<int>> treeGrid;
    for (auto line : inputLines) {
        vector<int> row;
        for (char ch : line) {row.push_back(ch - '0');}
        treeGrid.push_back(row);
    }

    // Part 1
    auto execStart1 = chrono::steady_clock::now();

    vector<vector<int>> visibleGrid(N, vector<int>(N, 0));

    // Instead of rotating the array, I have a coordinate variable for each dimension
    // and swap and reverse them to re-use them for all 4 directions
    for (int i = 0; i < N; i++) {
        // I keep track of tallest tree seen so far in the line, for each direction
        vector<int> maxHeight(4, -1);
        for (int j = 0; j < N; j++) {
            vector<int> x {i, i, j, N-j-1};
            vector<int> y {j, N-j-1, i, i};
            // For each directionk, check if this tree is the highest so far, if so,
            // it's visible from this direction. Then, update greatest height.
            for (int d = 0; d < 4; d++) {
                if (treeGrid[x[d]][y[d]] > maxHeight[d] ) {
                visibleGrid[x[d]][y[d]] = 1;
                maxHeight[d] = treeGrid[x[d]][y[d]];
                } 
            }
        }
    }

    int visible = 0;
    for (auto row : visibleGrid) {
        for (auto col : row) {
            visible += col;
        }
    }

    auto execTime1 = chrono::steady_clock::now() - execStart1;

    // Part 2
    // Note: no trees visible from all sides in full input
    auto execStart2 = chrono::steady_clock::now();

    // I keep the viewing distances for each direction in an NxNx4 array
    vector<vector<vector<int>>> distanceGrid(N, vector<vector<int>>(N, vector<int>(4)));

    for (int i = 0; i < N; i++){
        // I progress in each direction keeping track of how many trees since 
        // last one of equal or greater height, for each possible height
        vector<vector<int>> viewDistance(10, vector<int>(4, 0));
        for (int j = 0; j < N; j++) {
            vector<int> x {i, i, j, N-j-1};
            vector<int> y {j, N-j-1, i, i};
            for (int d = 0; d < 4; d++) {
                int treeHeight = treeGrid[x[d]][y[d]];
                // I assign the viewing distance for this tree
                distanceGrid[x[d]][y[d]][d] = viewDistance[treeHeight][d];
                // Then reset the distance counter for this and lower heigths
                for (int h = 0; h <= treeHeight; h++) {
                    viewDistance[h][d] = 0;
                }
                // Then add 1 to each distance counter before moving to next position
                for (int h = 0; h < 10; h++) {
                    viewDistance[h][d]++;
                }
            }
        }
    }

    // Multiply scores from each direction
    vector<vector<int>> scenicScore(N, vector<int>(N, 1));
    for (int d = 0; d < 4; d++) {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                scenicScore[i][j] *= distanceGrid[i][j][d];
            }
        }
    }

    // Find max score
    int maxScore = -1;
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
               if (scenicScore[i][j] > maxScore) {
                    maxScore = scenicScore[i][j];
            }
        }
    }

    auto execTime2 = chrono::steady_clock::now() - execStart2;

    cout << "Solution to Part 1: " << visible << " . Execution time: " << execTime1 << endl
         << "Solution to Part 2: " << maxScore << " . Execution time: " << execTime2;

}