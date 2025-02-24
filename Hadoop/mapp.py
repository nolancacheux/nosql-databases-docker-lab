import sys

# Read input line by line from standard input (STDIN)
for line in sys.stdin:
    line = line.strip()  # Remove leading and trailing spaces
    words = line.split()  # Split the line into words using space as a separator

    # Print each word followed by a tab and the number 1
    for word in words:
        print('%s\t%s' % (word, 1)) #display the word and the number 1 separated by a tab
