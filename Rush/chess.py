class Piece:
    def __init__(self, name, color, realname, display_name):
        self.name = name  # For internal logic (e.g., "p", "r")
        self.color = color
        self.realname = realname
        self.display_name = display_name  # For board display (e.g., "🅿", "𝗣")

    def is_valid_move(self, start, end, board, en_passant_target=None):
        if self.name == "p":  # Pawn
            return self.is_valid_pawn_move(start, end, board, en_passant_target)
        elif self.name == "r":  # Rook
            return self.is_valid_rook_move(start, end, board)
        elif self.name == "n":  # Knight
            return self.is_valid_knight_move(start, end)
        elif self.name == "b":  # Bishop
            return self.is_valid_bishop_move(start, end, board)
        elif self.name == "q":  # Queen
            return self.is_valid_queen_move(start, end, board)
        elif self.name == "k":  # King
            return self.is_valid_king_move(start, end, board)
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
                if (self.color == "white" and x1 == 6) or (self.color == "black" and x1 == 1):
                    return board[x2][y2] is None and board[x1 + direction][y2] is None
        
        # Diagonal capture
        elif abs(y2 - y1) == 1 and (x2 - x1) == direction:
            if en_passant_target and (x2, y2) == en_passant_target:
                return True
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

        if abs(x2 - x1) > 1 or abs(y2 - y1) > 1:
            return False

        target_piece = board[x2][y2]
        if target_piece is None or target_piece.color != self.color:
            return True

        return False
class ChessBoard:
    def __init__(self):
        #Board info
        self.board = [
            [Piece("r", "black", "Rook", "𝗥"), Piece("n", "black", "Knight", "𝗡"), Piece("b", "black", "Bishop", "𝗕"), Piece("q", "black", "Queen", "𝗤"), Piece("k", "black", "King", "𝗞"), Piece("b", "black", "Bishop", "𝗕"), Piece("n", "black", "Knight", "𝗡"), Piece("r", "black", "Rook", "𝗥")],
            [Piece("p", "black", "Pawn", "𝗣")] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Piece("p", "white", "Pawn", "🅿")] * 8,
            [Piece("r", "white", "Rook", "🆁"), Piece("n", "white", "Knight", "🅽"), Piece("b", "white", "Bishop", "🅱"), Piece("q", "white", "Queen", "🆀"), Piece("k", "white", "King", "🅺"), Piece("b", "white", "Bishop", "🅱"), Piece("n", "white", "Knight", "🅽"), Piece("r", "white", "Rook", "🆁")]
        ]
        self.turn = "white"
        self.en_passant_target = None
        self.moves_history = []

    def print_board(self):
        #Board Printer
        print("  •" + "———•" * 8)
        for i, row in enumerate(self.board):
            row_label = 8 - i  # Row labels in reverse order (8 to 1)
            row_pieces = [str(piece.display_name) if piece else " " for piece in row]
            print(f"{row_label} │ " + " │ ".join(row_pieces) + " │")
            print("  •" + "———•" * 8)

        print("    a   b   c   d   e   f   g   h".upper())
        print("  [       can Reset & Stop        ]")

    def is_valid_move(self, start, end):
        #Basic move rule
        x1, y1 = start
        piece = self.board[x1][y1]

        if piece is None:
            print(f"No piece at {chr(y1 + ord('a'))}{8 - x1}.")
            return False

        if piece.color != self.turn:
            print(f"It's {self.turn}'s turn!")
            return False

        if not piece.is_valid_move(start, end, self.board, self.en_passant_target):
            print(f"--------Invalid move for {piece.realname} from {chr(y1 + ord('a'))}--------")
            return False

        return True

    def move_piece(self, start, end, move):
        #move function
        x1, y1 = start
        x2, y2 = end
        piece = self.board[x1][y1]

        if self.is_valid_move(start, end):
            if isinstance(piece, Piece) and piece.name == "p" and self.en_passant_target == (x2, y2):
                captured_pawn_row = x2 - (-1 if piece.color == "white" else 1)
                self.board[captured_pawn_row][y2] = None

            self.board[x2][y2] = self.board[x1][y1]
            self.board[x1][y1] = None
            self.moves_history.append(move)
            self.en_passant_target = None

            if piece.name == "p" and abs(x2 - x1) == 2:
                self.en_passant_target = (x1 + (x2 - x1) // 2, y1)

            self.turn = "black" if self.turn == "white" else "white"


def main():
    board = ChessBoard()
    while True:
        board.print_board()
        move = input(f"{board.turn} to move: ").lower().strip()
        

        if move.lower() == "stop":
            # Print the game history
            print("Game History:")
            print("White   |   Black")
            for i in range(0, len(board.moves_history), 2):
                try:
                    move1 = board.moves_history[i]
                    move2 = board.moves_history[i + 1]
                    print(f"{i + 1}: {move1}  {i + 2}: {move2}")
                except IndexError:
                    # If there is an odd number of moves, just print the last one
                    move1 = board.moves_history[i]
                    print(f"{i + 1}: {move1}")

            break
        elif move.lower() == "reset":
        #reset the board
            board = ChessBoard()
            print("The board has been reset.")
            continue
        try:
            start_pos, end_pos = move.split()
            x1, y1 = 8 - int(start_pos[1]), ord(start_pos[0]) - ord('a')
            x2, y2 = 8 - int(end_pos[1]), ord(end_pos[0]) - ord('a')
            board.move_piece((x1, y1), (x2, y2), move)
            
        except (ValueError, IndexError):
            print("Invalid move format.")


if __name__ == "__main__":
    main()
