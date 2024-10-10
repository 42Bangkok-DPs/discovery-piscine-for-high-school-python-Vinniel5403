'''
Checkmate
'''
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

    def is_checked_by_knight(board, kr, kc):
        # Knight's L-shaped moves
        knight_moves = [
            (-2, -1), (-2, +1), (+2, -1), (+2, +1), 
            (-1, -2), (-1, +2), (+1, -2), (+1, +2)
        ]
        for move in knight_moves:
            nr, nc = kr + move[0], kc + move[1]
            if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
                if board[nr][nc] == 'N':
                    return True
        return False

    # Check board validity
    board_size = len(board)
    for row in board:
        if len(row) != board_size:
            print("Failed Sq")
            return

    # Find the King's position and count
    king_position, king_count = find_king(board)
    if king_count != 1:
        print("Failed K")
        return

    # Check if the King is in check by Rook, Bishop, Queen, Pawn, or Knight
    kr, kc = king_position
    if (is_checked_by_rook(board, kr, kc) or 
        is_checked_by_bishop(board, kr, kc) or 
        is_checked_by_pawn(board, kr, kc) or
        is_checked_by_knight(board, kr, kc)):
        print("Success")  # King is in check
    else:
        print("Failed")  # King is safe
