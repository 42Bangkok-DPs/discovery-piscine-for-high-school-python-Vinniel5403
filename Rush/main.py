from checkmate import checkmate
def main():
    # Test case where the King is checked by a Knight
    board = [
        "R...",
        ".K..",
        "..P.",
        "...."        
    ]
    checkmate(board)  # Expected output: Success

if __name__ == "__main__":
    main()
