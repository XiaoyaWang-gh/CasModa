import sys

def main(start, count):
    start = int(start)
    count = int(count)
    numbers = [str(start + i) for i in range(count)]
    print(','.join(numbers))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m cc <start> <count>")
    else:
        _, start, count = sys.argv
        main(start, count)
