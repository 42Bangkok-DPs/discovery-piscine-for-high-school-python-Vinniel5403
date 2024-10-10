class Piece:
    def __init__(self, name, color, realname):
        self.name = name
        self.color = color
        self.realname = realname

    def is_valid_move(self, start, end, board, en_passant_target=None):
        if self.name.lower() == "p":  # Pawn
            return self.is_valid_pawn_move(start, end, board, en_passant_target)
        elif self.name.lower() == "r":  # Rook
            return self.is_valid_rook_move(start, end, board)
        elif self.name.lower() == "n":  # Knight
            return self.is_valid_knight_move(start, end)
        elif self.name.lower() == "b":  # Bishop
            return self.is_valid_bishop_move(start, end, board)
        elif self.name.lower() == "q":  # Queen
            return self.is_valid_queen_move(start, end, board)
        elif self.name.lower() == "k":  # King
            return self.is_valid_king_move(start, end)
        return False

    def is_valid_pawn_move(self, start, end, board, en_passant_target=None):
        x1, y1 = start
        x2, y2 = end
        direction = -1 if self.color == "white" else 1

        # Standard move forward
        if y1 == y2:
            if (x2 - x1) == direction:
                return board[x2][y2] is None
            elif (x2 - x1) == 2 * direction:
                # Ensure the pawn is on the initial row
                if (self.color == "white" and x1 == 6) or (self.color == "black" and x1 == 1):
                    return board[x2][y2] is None and board[x1 + direction][y2] is None
        
        # Diagonal capture
        elif abs(y2 - y1) == 1 and (x2 - x1) == direction:
            # En passant capture
            if en_passant_target and (x2, y2) == en_passant_target:
                return True
            # Normal capture
            return board[x2][y2] is not None and board[x2][y2].color != self.color

        return False

    def is_valid_rook_move(self, start, end, board):
        x1, y1 = start
        x2, y2 = end

        if x1 != x2 and y1 != y2:
            return False

        # path_checker
        if x1 == x2:  # Y axis
            step = 1 if y2 > y1 else -1
            for i in range(y1 + step, y2, step):
                if board[x1][i] is not None:
                    return False
        else:  # X axis
            step = 1 if x2 > x1 else -1
            for i in range(x1 + step, x2, step):
                if board[i][y1] is not None:
                    return False

        return board[x2][y2] is None or board[x2][y2].color != self.color

    def is_valid_knight_move(self, start, end):
        x1, y1 = start
        x2, y2 = end
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        return (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

    def is_valid_bishop_move(self, start, end, board):
        x1, y1 = start
        x2, y2 = end
        if abs(x2 - x1) != abs(y2 - y1):
            return False

        step_x = 1 if x2 > x1 else -1
        step_y = 1 if y2 > y1 else -1
        for i in range(1, abs(x2 - x1)):
            if board[x1 + i * step_x][y1 + i * step_y] is not None:
                return False

        return board[x2][y2] is None or board[x2][y2].color != self.color

    def is_valid_queen_move(self, start, end, board):
        return self.is_valid_rook_move(start, end, board) or self.is_valid_bishop_move(start, end, board)

    def is_valid_king_move(self, start, end, board):
        x1, y1 = start
        x2, y2 = end
    
    # Ensure the king moves only one square in any direction
        if abs(x2 - x1) > 1 or abs(y2 - y1) > 1:
            return False

    # Ensure the destination square is either empty or contains an opponent's piece
        target_piece = board[x2][y2]
        if target_piece is None or target_piece.color != self.color:
            return True

        return False




class ChessBoard:
    def __init__(self):
        self.board = [
            [Piece("r", "black", "Rook"), Piece("n", "black", "Knight"), Piece("b", "black", "Bishop"), Piece("q", "black", "Queen"), Piece("k", "black", "King"), Piece("b", "black", "Bishop"), Piece("n", "black", "Knight"), Piece("r", "black", "Rook")],
            [Piece("p", "black", "Pawn")] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Piece("P", "white", "Pawn")] * 8,
            [Piece("R", "white", "Rook"), Piece("N", "white", "Knight"), Piece("B", "white", "Bishop"), Piece("Q", "white", "Queen"), Piece("K", "white", "King"), Piece("B", "white", "Bishop"), Piece("N", "white", "Knight"), Piece("R", "white", "Rook")]
        ]
        self.turn = "white"
        self.en_passant_target = None  # Tracks the square available for en passant capture

    def print_board(self):
        print("  +" + "---+" * 8)

        # Print board with row labels
        for i, row in enumerate(self.board):
            row_label = 8 - i  # Row labels in reverse order (8 to 1)
            row_pieces = [str(piece.name) if piece else " " for piece in row]
            print(f"{row_label} | " + " | ".join(row_pieces) + " |")
            print("  +" + "---+" * 8)

        # Column labels again at the bottom
        print("    a   b   c   d   e   f   g   h".upper())

    def is_valid_move(self, start, end, move):
        x1, y1 = start
        x2, y2 = end
        piece = self.board[x1][y1]

        if piece is None:
            print(f"No piece at {chr(y1 + ord('a'))}{8 - x1}.")
            return False

        if piece.color != self.turn:
            print(f"It's {self.turn}'s turn!")
            return False

        if not piece.is_valid_move(start, end, self.board, self.en_passant_target):
            print(f"--------Invalid move for {piece.realname} from {chr(y1 + ord('a'))}{8 - x1} to {chr(y2 + ord('a'))}{8 - x2}--------")
            return False

        return True

    def move_piece(self, start, end, move):
        x1, y1 = start
        x2, y2 = end
        piece = self.board[x1][y1]

        if self.is_valid_move(start, end, move):
            # Check if it's an en passant capture
            if isinstance(piece, Piece) and piece.name.lower() == "p" and self.en_passant_target == (x2, y2):
                # En passant: remove the captured pawn
                captured_pawn_row = x2 - (-1 if piece.color == "white" else 1)
                self.board[captured_pawn_row][y2] = None

            # Move the piece
            self.board[x2][y2] = self.board[x1][y1]
            self.board[x1][y1] = None

            # Reset en passant target
            self.en_passant_target = None

            # If a pawn moves two squares, mark the en passant target
            if piece.name.lower() == "p" and abs(x2 - x1) == 2:
                self.en_passant_target = (x1 + (x2 - x1) // 2, y1)

            # Switch turns
            self.turn = "black" if self.turn == "white" else "white"


def main():
    board = ChessBoard()
    while True:
        board.print_board()
        move = input(f"{board.turn}'s move: ").strip()

        if move.lower() == "stop":
            # Print the game history
            print("Game History:")
            for index, m in enumerate(board.moves_history, start=1):
                print(f"{index}: {m}")
            break  # End the game loop
            
        elif move.lower() == "reset":
            board = ChessBoard()
            print("The board has been reset.")
            continue  # Skip the rest of the loop and continue with the new board

        try:
            start_pos, end_pos = move.split()
            x1, y1 = 8 - int(start_pos[1]), ord(start_pos[0]) - ord('a')
            x2, y2 = 8 - int(end_pos[1]), ord(end_pos[0]) - ord('a')
            board.move_piece((x1, y1), (x2, y2), move)
        except (ValueError, IndexError):
            print("Invalid move format. Please use the format 'e2 e4'.")

if __name__ == "__main__":
    main()
