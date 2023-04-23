# -Solving-Hua-Rong-Dao-using-Search

## introduction
For this assignment, you will implement a solver for the Hua Rong Dao sliding puzzle. Hua Rong Dao is a sliding puzzle that is popular in China. Check out the following page for some background story on the puzzle and an English description of the (rules)[https://chinesepuzzles.org/huarong-pass-sliding-block-puzzle/].
The puzzle board is four spaces wide and five spaces tall. We will consider the variants of this puzzle with ten pieces. There are four kinds of pieces:

    One 2x2 piece.
    Five 1x2 pieces. Each 1x2 piece can be horizontal or vertical.
    Four 1x1 pieces.
Once we place the ten pieces on the board, two empty spaces should remain.

Look at the most classic initial configuration of this puzzle below. (Don't worry about the Chinese characters. They are not crucial for understanding the puzzle.) In this configuration, one 1x2 piece is horizontal, and the other four 1x2 pieces are vertical.
![classic puzzle for HuaRong puzzle](https://q.utoronto.ca/courses/293717/files/24240073/preview)

The goal is to move the pieces until the 2x2 piece is above the bottom opening (i.e. helping Cao Cao escape through the Hua Rong Dao/Pass). You may move each piece horizontally or vertically only into an available space. You are not allowed to rotate any piece or move it diagonally.

## TASK
Implement DFS and A* Search to solve HuaRong puzzle
The following configuration is for testing the code:
\```bash
python3 hrd.py --algo astar --inputfile <input file> --outputfile <output file>
python3 hrd.py --algo dfs --inputfile <input file> --outputfile <output file>
\```



## The Input and Output File Formats
In the input and output files, we will represent each state in the following format.

    Each state is a grid of 20 characters. The grid has 5 rows with 4 characters per row.
    The empty squares are denoted by the period symbol.
    The 2x2 piece is denoted by 1.
    The single pieces are denoted by 2.
    A horizontal 1x2 piece is denoted by < on the left and > on the right. 
    A vertical 1x2 piece is denoted by ^ on the top and v on the bottom (lower cased letter v).

Here is an example of a state.
<pre>
```
^^^^
vvvv
22..
11<>
1122
```
</pre>
Each input file contains one state, representing a puzzle's initial state.

Each output file contains a sequence of states. The first state in the sequence is the initial configuration of the puzzle. The last state is a goal state. There is one empty line between any two consecutive states. 

Here are examples of[inputfile](https://github.com/dkhhandsome/-Solving-Hua-Rong-Dao-using-Search/files/11304883/testhrd_easy1.txt) and [outputfile](https://github.com/dkhhandsome/-Solving-Hua-Rong-Dao-using-Search/files/11304884/testhrd_easy1sol_astar.txt) The output file is an optimal solution for the puzzle found by A* search.







