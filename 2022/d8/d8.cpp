#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include "../include/utils.h"
using namespace std;


int countVisibleTrees(vector<int>) {

}

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

    for (int i = 0; i < N; i++) {
        vector<int> maxHeight(4, -1); // Reset vector of tallest tree seen
        for (int j = 0; j < N; j++) {
            vector<int> x {i, i, j, N-j-1};
            vector<int> y {j, N-j-1, i, i};
            // 4 possible directions (d)
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
    /* I checked: there are no trees visible from all sides in full input,
    which would make this problem very easy.*/
    auto execStart2 = chrono::steady_clock::now();

    vector<vector<vector<int>>> distanceGrid(N, vector<vector<int>>(N, vector<int>(4)));

    for (int i = 0; i < N; i++) {
        vector<vector<int>> viewDistance(10, vector<int>(4, 0));

        for (int j = 0; j < N; j++) {
            vector<int> x {i, i, j, N-j-1};
            vector<int> y {j, N-j-1, i, i};

            for (int d = 0; d < 4; d++) {
                int treeHeight = treeGrid[x[d]][y[d]];
                distanceGrid[x[d]][y[d]][d] = viewDistance[treeHeight][d];
                for (int h = 0; h <= treeHeight; h++) {
                    viewDistance[h][d] = 0;
                }
                for (int h = 0; h < 10; h++) {
                    viewDistance[h][d]++;
                }
            }
        }
    }

    vector<vector<int>> scenicScore(N, vector<int>(N, 1));
    for (int d = 0; d < 4; d++) {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                scenicScore[i][j] *= distanceGrid[i][j][d];
            }
        }
    }

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