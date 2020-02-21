import secrets
import time


def main():

    # initial variables
    # board dimensions / number of queens
    x = 16
    # maximum number of queen movements allowed
    max_steps = 10000000000000
    # time variables
    endTime = time.time()+20
    # x by x board with x queens randomly placed
    board = createBoard(x)
    # stop repeat movements
    conflictIndex = -1

    # repeats as long as specified
    for i in range(max_steps):
        # gets the index of one of the queens with the maximum number of conflicts. Cannot find the same index twice
        conflictIndex = getConflicts(board, x, conflictIndex)

        # if there are no conflicts, the board is solved
        if conflictIndex is None:
            # track the number of steps and stop repeating the process
            print("Steps: ", i)
            # print the placements of the queens on the board at the final state
            print("Solution:")
            for j in board:
                print(j, end=" ")
            print()
            break

        # if the board is not solved, move the chosen queen to its space with the least conflicts
        else:
            board = minimizeConflicts(board, conflictIndex, x)

        if time.time() > endTime:
            print("No solution found. Steps: ", i)
            break


# returns one (of the potential many) queen that has the highest number of conflicts
def getConflicts(board, x, lastVal):
    # variables for tracking the queens with the highest conflicts
    maxConflicts = 0
    conflictIndex = []
    # for each queen
    for i in range(x):
        conflicts = 0
        # find the total number of conflicts with other queens
        for j in range(x):
            conflicts += getConflictCount(board, i, j)

        # if it has a new maximum conflict number, track the number of conflicts and the index of the queen
        if conflicts > maxConflicts and i is not lastVal:
            maxConflicts = conflicts
            conflictIndex = [i]
        # if it is equal to the current highest conflict number, track this queen as well as previous
        elif conflicts == maxConflicts and conflicts != 0 and i is not lastVal:
            conflictIndex.append(i)
    # return None if there are no conflicts
    if len(conflictIndex) == 0:
        return None
    # otherwise, return a random queen that has the highest conflict number
    else:
        return secrets.choice(conflictIndex)


# moves a queen at a given index to a spot where it has the fewest conflicts
def minimizeConflicts(board, conflictIndex, x):
    # variables that track the best new position for the queen
    newPosition = []
    minConflicts = x
    # a variable to make sure a queen cannot move to its initial position
    # this stops repeat states where the program can do nothing
    changeGuarantee = board[conflictIndex]

    # for each potential queen position
    for i in range(x):
        # set the board so that the queen is moved to this position
        board[conflictIndex] = i
        conflicts = 0

        # check the number of conflicts for the queen if it is in this position
        for j in range(x):
            conflicts += getConflictCount(board, i, j)

        # if the position is the best position, track the index
        if conflicts < minConflicts and i is not changeGuarantee:
            minConflicts = conflicts
            newPosition = [i]
        # if the position has the same amount of conflicts as other best cases, track all the indexes
        elif conflicts == minConflicts and i is not changeGuarantee:
            newPosition.append(i)

    # put the queen in a random position that has the fewest conflicts and return the board
    board[conflictIndex] = secrets.choice(newPosition)
    return board


# checks if there are conflicts between 2 queens
def getConflictCount(board, i, j):
    # checks if the queens are in the same row
    if board[i] == board[j] and i is not j:
        return 1

    # checks if the queens are in the same diagonal to the left
    if j < i:
        diag = abs(j - i)
        if board[i - diag] == board[i] - diag or board[i - diag] == board[i] + diag:
            return 1

    # checks if the queens are in the same diagonal to the right
    if j > i:
        diag = abs(j - i)
        if board[i + diag] == board[i] - diag or board[i + diag] == board[i] + diag:
            return 1
    # returns 0 if the queens are not in conflict
    return 0


# creates a randomized board with 1 queen in every column
def createBoard(x):
    array = [secrets.randbelow(x) for i in range(x)]
    return array


if __name__ == "__main__":
    main()