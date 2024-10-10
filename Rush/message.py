def checkmate(board):
    def find_king(board):
        king_count = 0
        king_position = None
        for r, row in enumerate(board):
            for c, char in enumerate(row):
                if char == 'K':
                    king_count += 1
                    king_position = (r, c)
        return king_position, king_count

    def is_checked_by_rook(board, kr, kc):
        # Check rows (left and right)
        for c in range(kc + 1, len(board[0])):
            if board[kr][c] != '.':
                if board[kr][c] == 'R' or board[kr][c] == 'Q':
                    return True
                break
        for c in range(kc - 1, -1, -1):
            if board[kr][c] != '.':
                if board[kr][c] == 'R' or board[kr][c] == 'Q':
                    return True
                break
        # Check columns (up and down)
        for r in range(kr + 1, len(board)):
            if board[r][kc] != '.':
                if board[r][kc] == 'R' or board[r][kc] == 'Q':
                    return True
                break
        for r in range(kr - 1, -1, -1):
            if board[r][kc] != '.':
                if board[r][kc] == 'R' or board[r][kc] == 'Q':
                    return True
                break
        return False

    def is_checked_by_bishop(board, kr, kc):
        # Check diagonals
        for d in range(1, len(board)):
            if kr + d < len(board) and kc + d < len(board[0]):
                if board[kr + d][kc + d] != '.':
                    if board[kr + d][kc + d] == 'B' or board[kr + d][kc + d] == 'Q':
                        return True
                    break
            if kr - d >= 0 and kc - d >= 0:
                if board[kr - d][kc - d] != '.':
                    if board[kr - d][kc - d] == 'B' or board[kr - d][kc - d] == 'Q':
                        return True
                    break
            if kr + d < len(board) and kc - d >= 0:
                if board[kr + d][kc - d] != '.':
                    if board[kr + d][kc - d] == 'B' or board[kr + d][kc - d] == 'Q':
                        return True
                    break
            if kr - d >= 0 and kc + d < len(board[0]):
                if board[kr - d][kc + d] != '.':
                    if board[kr - d][kc + d] == 'B' or board[kr - d][kc + d] == 'Q':
                        return True
                    break
        return False

    def is_checked_by_pawn(board, kr, kc):
        # Pawns attack diagonally (one step forward)
        if kr - 1 >= 0 and kc - 1 >= 0 and board[kr - 1][kc - 1] == 'P':
            return True
        if kr - 1 >= 0 and kc + 1 < len(board[0]) and board[kr - 1][kc + 1] == 'P':
            return True
        return False

    # Check board validity
    board_size = len(board)
    for row in board:
        if len(row) != board_size:
            print("Error: Board must be square")
            return

    # Find the King's position and count
    king_position, king_count = find_king(board)
    if king_count != 1:
        print("Error: There must be exactly one King on the board")
        return

    # Check if the King is in check by Rook, Bishop, Queen, or Pawn
    kr, kc = king_position
    if (is_checked_by_rook(board, kr, kc) or 
        is_checked_by_bishop(board, kr, kc) or 
        is_checked_by_pawn(board, kr, kc)):
        print("Checked")  # King is in check
    else:
        print("Safe")  # King is safe

# Example Test Cases
def main():
    # Test case where the King is checked
    board1 = [
        "R..R",
        ".K..",
        "...K",
        ".R.Q"
    ]
    checkmate(board1)  # Expected output: Checked

    # Test case where the King is safe
    board2 = [
        ".R..",
        ".K..",
        "....",
        "...."
    ]
    checkmate(board2)  # Expected output: Safe

    # Test case with invalid board size
    board3 = [
        "R..R",
        ".K..",
        "...K",
        ".R.Q",
        "...."  # Extra row, making it not square
    ]
    checkmate(board3)  # Expected output: Error: Board must be square

    # Test case with more than one King
    board4 = [
        "R..R",
        ".K..",
        "K...",
        "...."
    ]
    checkmate(board4)  # Expected output: Error: There must be exactly one King on the board

if __name__ == "__main__":
    main()
