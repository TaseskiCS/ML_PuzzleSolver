import argparse
from puzzles import eight_puzzle, fifteen_puzzle

def main():
    parser = argparse.ArgumentParser(description="Select a puzzle solver to run.")
    parser.add_argument("puzzle", choices=["8", "15"], help="Choose '8' for the 8-puzzle or '15' for the 15-puzzle.")
    args = parser.parse_args()

    if args.puzzle == "8":
        eight_puzzle.main()
    else:
        fifteen_puzzle.main()

if __name__ == "__main__":
    main()
