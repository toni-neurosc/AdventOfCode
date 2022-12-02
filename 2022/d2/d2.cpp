#include <iostream>
#include <fstream>
#include <string>
using namespace std;

void updateScorePart1(int& score, int oppPlay, int myPlay){
    // Calculate result by checking if your choice is to the right or left of opponent
    int result = (myPlay - oppPlay + 1) % 3;
    result = (result + 3) % 3; // Make modulo positive
    score += result * 3 + myPlay + 1; 
}

void updateScorePart2(int& score, int oppPlay, int result){
    /*  
        Find which play you need to make based on result.
        If you need to lose, move one left (-1), if you need to win, move one right (+1)
        and don't move (0) if you want to draw.
        Since result list order is XYZ --> Lose, Draw, Win, 
        we substract 1 from indexes to get the require move: -1, 0, +1
    */
    int myPlay = (oppPlay + result - 1) % 3;
    myPlay = (myPlay + 3) % 3; // Make modulo positive
    score += result * 3 + myPlay + 1; 
}

int main (int argc, char **argv) 
{
    // Possible plays for each player in order: Rock, Paper, Scissors
    string oppPlays = "ABC"; 
    string myPlays = "XYZ"; // For part 2, this represents result: Lose, Draw, Win   
    // Scores are index+1: Rock (1), Paper (2), Scissors (3)
    // Scores for results are index * 3:  Lose(0), Draw (3), Win(6)

    // Initialize scores
    int score1 = 0;
    int score2 = 0;

    // Read input
    ifstream inFile(argv[1]);
    string line;
    if ( inFile.is_open() ) 
    {
        while ( getline(inFile, line) ) 
        {   
            int oppPlay = oppPlays.find(line[0]);      // Get opponent play index

            int myPlay = myPlays.find(line[2]);        // Find my play for Part 1
            updateScorePart1(score1, oppPlay, myPlay); // Update score for Part 1

            int result = myPlays.find(line[2]);        // Find desired outcome for Part 2
            updateScorePart2(score2, oppPlay, result); // Update score for Part 2
        }

        cout << "Solution to Part 1: " << score1 << endl
             << "Solution to Part 2: " << score2;
    }
}