from copy import deepcopy
from heapq import heappush, heappop
import time
import argparse
import sys

# ====================================================================================

char_goal = '1'
char_single = '2'


class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_goal, is_single, coord_x, coord_y, orientation):
        """
        :param is_goal: True if the piece is the goal piece and False otherwise.
        :type is_goal: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v')
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_goal = is_goal
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.is_goal, self.is_single,
                                       self.coord_x, self.coord_y,
                                       self.orientation)


class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 4
        self.height = 5

        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()

    # helper function convience for test
    def __str__(self) -> str:
        output = ''
        for i in self.grid:
            for j in i:
                output += j
            output += '\n'
        return output

    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_goal:
                self.grid[piece.coord_y][piece.coord_x] = char_goal
                self.grid[piece.coord_y][piece.coord_x + 1] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = char_goal
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = char_single
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'

    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='')
            print()


class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces.
    State has a Board and some extra information that is relevant to the search:
    heuristic function, f value, current depth and parent.
    """

    def __init__(self, board, f, depth, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param f: The f value of current state.
        :type f: int
        :param depth: The depth of current state in the search tree.
        :type depth: int
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.f = f
        self.depth = depth
        self.parent = parent
        self.id = hash(board)  # The id for breaking ties.

    def __str__(self) -> str:
        return str(self.board)

    def __lt__(self, other):
        return self.f < other.f


def expand(state):
    """
        Generate a list of states that can be reached by moving a piece on the board.

        :param state: The current state.
        :type state: State
        :return: The list of new states.
        :rtype: List[State]
    """
    pieces = state.board.pieces
    states = []
    movement = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # used to delete the class
    index = -1
    for piece in pieces:
        index += 1
        for x, y in movement:
            key = 0
            new_board = deepcopy(state.board)
            x_update = x + piece.coord_x
            y_update = y + piece.coord_y
            # specify the goal state
            if piece.is_goal:
                check_1 = 0
                # first check the limitation
                if 0 <= x_update < state.board.width - 1 and \
                        0 <= y_update < state.board.height - 1:
                    if state.board.grid[y_update][x_update] in ['.', char_goal] \
                            and state.board.grid[y_update][x_update + 1] in [
                        '.', char_goal] \
                            and state.board.grid[y_update + 1][x_update] in [
                        '.', char_goal] \
                            and state.board.grid[y_update + 1][
                        x_update + 1] in ['.', char_goal]:
                        check_1 = 1
                        key = 1
                        new_board.grid[y_update][x_update] = char_goal
                        new_board.grid[y_update][x_update + 1] = char_goal
                        new_board.grid[y_update + 1][x_update] = char_goal
                        new_board.grid[y_update + 1][
                            x_update + 1] = char_goal
                        # which means the puzzle shift right
                        if x_update - piece.coord_x > 0:
                            new_board.grid[y_update][x_update - 1] = '.'
                            new_board.grid[y_update + 1][x_update - 1] = '.'
                            # which means the puzzle shift left
                        elif x_update - piece.coord_x < 0:
                            new_board.grid[y_update][x_update + 2] = '.'
                            new_board.grid[y_update + 1][
                                x_update + 2] = '.'
                        elif y_update - piece.coord_y > 0:
                            # which means the puzzle shift downward
                            new_board.grid[y_update - 1][x_update] = '.'
                            new_board.grid[y_update - 1][x_update + 1] = '.'
                            # which means the puzzle shift upward
                        elif y_update - piece.coord_y < 0:
                            new_board.grid[y_update + 2][x_update] = '.'
                            new_board.grid[y_update + 2][
                                x_update + 1] = '.'

                        # bound checking, adding and remove pieces
                        del new_board.pieces[index]
                        new_board.pieces.append \
                            (Piece(True, False, x_update, y_update, None))
                if check_1 == 0:
                    continue
            elif piece.is_single:
                check_2 = 0
                if 0 <= x_update < state.board.width and 0 <= y_update < state.board.height:
                    if new_board.grid[y_update][x_update] == '.':
                        key = 1
                        new_board.grid[y_update][x_update] = char_single
                        new_board.grid[piece.coord_y][piece.coord_x] = '.'
                        check_2 = 1
                        del new_board.pieces[index]
                        new_board.pieces.append \
                            (Piece(False, True, x_update, y_update, None))
                if check_2 == 0:
                    continue
            elif piece.orientation == 'h':
                # devide into case that piece shift to right  or not
                # shift vertically
                if 0 <= x_update < state.board.width - 1 and \
                        0 <= y_update < state.board.height:
                    if y == 1 or y == -1:
                        if state.board.grid[y_update][x_update] == '.':
                            if state.board.grid[y_update][x_update + 1] != '.':
                                continue
                            else:
                                key = 1
                                new_board.grid[piece.coord_y][
                                    piece.coord_x] = '.'
                                new_board.grid[piece.coord_y][
                                    piece.coord_x + 1] = '.'
                                new_board.grid[y_update][x_update] = '<'
                                new_board.grid[y_update][x_update + 1] = '>'
                    # shift right horizontally
                    if x == 1:
                        if state.board.grid[y_update][x_update + 1] != '.':
                            continue
                        else:
                            key = 1
                            new_board.grid[piece.coord_y][piece.coord_x] = '.'
                            new_board.grid[y_update][x_update] = '<'
                            new_board.grid[y_update][x_update + 1] = '>'
                        # shift right horizontally
                    if x == -1:
                        if state.board.grid[y_update][x_update] != '.':
                            continue
                        else:
                            key = 1
                            new_board.grid[piece.coord_y][piece.coord_x] = '>'
                            new_board.grid[y_update][x_update] = '<'
                            new_board.grid[piece.coord_y][
                                piece.coord_x + 1] = '.'

                    del new_board.pieces[index]
                    new_board.pieces.append \
                        (Piece(False, False, x_update, y_update, 'h'))

            elif piece.orientation == 'v':
                if 0 <= x_update < state.board.width and \
                        0 <= y_update < state.board.height - 1:
                    # piece shift horizontally
                    if x == -1 or x == 1:
                        if new_board.grid[y_update][x_update] != '.' or \
                                new_board.grid[y_update + 1][x_update] != '.':
                            continue
                        else:
                            key = 1
                            new_board.grid[piece.coord_y][piece.coord_x] = '.'
                            new_board.grid[piece.coord_y + 1][
                                piece.coord_x] = '.'
                            new_board.grid[y_update][x_update] = '^'
                            new_board.grid[y_update + 1][x_update] = 'v'
                    # piece shift vertically
                    elif y == 1:
                        if new_board.grid[y_update + 1][x_update] != '.':
                            continue
                        else:
                            key = 1
                            new_board.grid[piece.coord_y][piece.coord_x] = '.'
                            new_board.grid[y_update][x_update] = '^'
                            new_board.grid[y_update + 1][x_update] = 'v'
                    elif y == -1:
                        if new_board.grid[y_update][x_update] != '.':
                            continue
                        else:
                            key = 1
                            # check here
                            new_board.grid[piece.coord_y + 1][
                                piece.coord_x] = '.'
                            new_board.grid[y_update][x_update] = '^'
                            new_board.grid[y_update + 1][x_update] = 'v'
                    del new_board.pieces[index]
                    new_board.pieces.append \
                        (Piece(False, False, x_update, y_update, 'v'))
            if key == 1:
                states.append(State(new_board,
                                    state.depth + 1 + Heuristic_function(
                                        new_board),
                                    state.depth + 1, state))
    return states


def get_solution(final_state):
    """
            :param final_state: final state
            :type final_state: State
            :rtype: List[State]
    """
    # tracing through from goal state to initial state
    walk_through = []
    while final_state is not None:
        walk_through.append(final_state)
        final_state = final_state.parent
    return walk_through[::-1]


def Heuristic_function(board):
    """
        :param board: The board of state.
        :type board: Board
        :rtype: int
    """
    for piece in board.pieces:
        if piece.is_goal:
            return abs(piece.coord_x - 1) + abs(piece.coord_y - 3)


def goal_test(state):
    """
        :param state: The state of puzzle.
        :type state: State
    """
    if state.board.grid[3][1] == char_goal and \
            state.board.grid[3][2] == char_goal and \
            state.board.grid[4][1] == char_goal and \
            state.board.grid[4][2] == char_goal:
        return True
    else:
        return False


def dfs_multi_pruning(start_state):
    """
    :param start_state: The state of puzzle.
    :type start_state: State
    :rtype: Boolean
    """
    # what exactly dfs will return
    if goal_test(start_state):
        return start_state
    frontier = [start_state]
    explored = set()
    while frontier:
        cur_state = frontier.pop()
        if str(cur_state.board.grid) not in explored:
            explored.add(str(cur_state.board.grid))
            if goal_test(cur_state):
                return cur_state
            frontier.extend(expand(cur_state))
    return None


def Astar_search(start_state):
    """
        :param start_state: The state of puzzle.
        :type start_state: State
    """
    frontier = []
    # we might need pruning to reduce the cost
    visited = set()
    heappush(frontier, (start_state.f, start_state))
    visited.add(str(start_state.board.grid))
    while frontier:
        cur_f, cur_state = heappop(frontier)
        if goal_test(cur_state):
            return cur_state
        for child_state in expand(cur_state):
            if str(child_state.board.grid) not in visited:
                visited.add(str(child_state.board.grid))
                heappush(frontier, (child_state.f, child_state))
    return None



# def Astar_search(start_state):
#     """
#         :param start_state: The state of puzzle.
#         :type start_state: State
#         :rtype: Boolean
#     """
#     frontier = []
#     # we might need pruning to reduce the cose
#     visited = set()
#     heappush(frontier, (start_state.f, start_state.id, start_state))
#     while frontier:
#         cur_f, cur_id, cur_state = heappop(frontier)
#         if goal_test(cur_state):
#             return cur_state
#         visited.add(cur_id)
#         for state in expand(cur_state):
#             if state.id in visited:
#                 continue
#             heappush(frontier, (state.f, state.id, state))
#     return None


def read_from_file(filename):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename, "r")

    line_index = 0
    pieces = []
    g_found = False

    for line in puzzle_file:

        for x, ch in enumerate(line):
            if ch == '^':  # found vertical piece
                pieces.append(Piece(False, False, x, line_index, 'v'))
            elif ch == '<':  # found horizontal piece
                pieces.append(Piece(False, False, x, line_index, 'h'))
            elif ch == char_single:
                pieces.append(Piece(False, True, x, line_index, None))
            elif ch == char_goal:
                if g_found == False:
                    pieces.append(Piece(True, False, x, line_index, None))
                    g_found = True
        line_index += 1

    puzzle_file.close()

    board = Board(pieces)

    return board


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()

    # read the board from the file
    board = read_from_file(args.inputfile)
    # create the initial state
    initial_state = State(board, 0, 0, None)

    # solve the puzzle
    if args.algo == 'astar':
        solution = Astar_search(initial_state)
    elif args.algo == 'dfs':
        solution = dfs_multi_pruning(initial_state)
    solutions = get_solution(solution)
    # f = open('test.txt', 'w')
    f = open(args.outputfile, 'w')
    for state in solutions:
        f.write(str(state))
        f.write('\n')
    f.close()
