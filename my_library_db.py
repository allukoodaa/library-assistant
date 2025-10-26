"""Library Assistant 3000

v1.0

by allukoodaa
"""

import argparse
import os
import sys


def main():
    """Main terminal UI logic.

    Reads the file given as an argument to the program and prints the number of lines.
    Then displays the main menu of the program and asks user for input.
    Programn ends if user types 'Q' or 'q' in the main menu, EOF signal (eg. Ctrl-D)
    to any input prompt or KeyboardInterrupt (Ctrl-C) at any time.
    """
    print('\n***Welcome to Library Assistant 3000!***\n\nReading given DB file...')
    # Read the file and inform the user of the number of entries in the 'database'.
    db_content = read_file()
    print(f'DB file contains {len(db_content)} lines.')
    # Delete db content to save memory.
    del db_content
    # Main menu UI starts here.
    while True:
        print(
            '\nWhat would you like to do next?\n'
            '1) Add new book to database\n'
            '2) Print current database content\n'
            'Q) Quit\n'
        )
        cmd = input('Input command: ')
        if cmd.casefold() == 'q':
            print('\nShutting down, goodbye!')
            break
        elif cmd == '1':
            add_book()
        elif cmd == '2':
            # Reads the file here to get most recent database content.
            curr_content = read_file()
            pretty_print(curr_content)
        else:
            print('Please choose a valid option.')


def add_book():
    """Helper function that extends the terminal user interface.

    The program asks the user for Title, Author, ISBN and Year of publication.
    Program verifies the input:
        - Title and Author fields can not be empty.
        - ISBN has to be less than 14 chars long and numeric.
        - Year must be numeric.
    """
    print('\nPlease input the information of the book you want to add to the database.')
    # Needs a new while loop.
    while True:
        title = input('Title: ')
        author = input('Author: ')
        # Simple check for empty input in the first two fields.
        if not title or not author:
            print('Warning: "Title" and/or "Author" field was empty. Try again.')
            continue
        isbn = input('ISBN: ')
        # ISBN should be 10 or 13 digits.
        if not isbn.isnumeric() or len(isbn) > 13:
            print(f'ISBN must be numeric and less than 14 characters, was {isbn!r}\n')
            continue
        year = input('Year of publication: ')
        # Year MUST be numeric or else the sorting step fails later.
        if not year.isnumeric():
            print(f'Year must contain only numbers, was {year!r}\n')
            continue
        # Pack the book info into a list
        book = [title, author, isbn, year]
        print('\nYour entry:')
        # Yet another while loop to account for user error in the next input step.
        while True:
            # pretty_print() expects a list of lists to function correctly.
            pretty_print([book])
            print(
                '\nWould you like to add this book to the database?\n'
                '1) Yes\n2) Try again\n3) Return to main menu.\n'
            )
            cmd = input('Input command: ')
            # Only option that will alter the db file.
            if cmd == '1':
                update_db(book)
                return
            # Breaks the inner while loop.
            elif cmd == '2':
                break
            # Goes straight back to the main menu in main().
            elif cmd == '3':
                print('Returning to main menu. Changes not written to the file.\n')
                return
            else:
                print('Please choose a valid option.\n')


def pretty_print(content):
    """Prints the current database content to the console.

    Console width should be at least 110 columns due to the whitespace normalization of the table.
    If the program detects a smaller terminal window, the alternate pretty print function is
    called instead.
    """
    # The database should be in ascending order by publishing year.
    # content.sort(key=lambda line: int(line[-1]))
    # Terminal window too narrow for pretty print.
    if os.get_terminal_size().columns < 110:
        print('The absolute minimum terminal window width for the pretty print is 110 columns.')
        alternate_pretty_print(content)
        return
    # Whitespace normalization for header row.
    print(f'\n{"INDEX":<6}{"TITLE":<50}{"AUTHOR":<35}{"ISBN":<15}YEAR')
    for ind, line in enumerate(content, start=1):
        # Unpack title, author, isbn and year from the list `line`.
        t, a, i, y = line
        # Whitespace normalization for each row.
        print(f'{ind:<6}{t:<50}{a:<35}{i:<15}{y}')


def alternate_pretty_print(content):
    """Alternate pretty print function for users with terminal windows less than 110 colums.

    Prints each column of a row in the database along with the associated header.
    """
    # User is informed of the chance in printing style.
    input('Reverting to alternate printing. Press "Enter" to continue. ')
    for index, line in enumerate(content, 1):
        t, a, i, y = line
        print(f'{index}:\nTitle: {t!r}\nAuthor: {a!r}\nISBN: {i!r}\nYear: {y!r}\n')


def update_db(new_book):
    """Updates database with new book information given by user.

    Reads current db file. Appends new book information to the end of the aquired list.
    Sorts the whole list in ascending order based on year of publication (int).
    Writes the newly sorted list containing old and new data to the same db file.
    """
    print('Updating database...')
    curr_content = read_file()
    curr_content.append(new_book)
    # Sorts the db content in place using the last column, `year` the key.
    curr_content.sort(key=lambda line: int(line[-1]))
    write_file(curr_content)
    print('Database updated successfully!')


def read_file():
    """Reads file and saves stripped content row for row as list of lists."""
    with open(filepath) as file:
        content = [line.strip().split('/') for line in file.readlines()]
    return content


def write_file(content):
    """Writes the given content to the DB file.

    Joins each row of data with the separator `/` and adds a newline at the end.
    """
    with open(filepath, 'w') as file:
        for line in content:
            parsed_line = '/'.join(line) + '\n'
            file.write(parsed_line)


if __name__ == '__main__':
    # Init argument parser.
    parser = argparse.ArgumentParser(prog='Library DB Assistant 3000')
    # Specify mandatory argument - fails if number of arguments is 0 or more than 1.
    parser.add_argument('filepath', nargs=1, help='filename or absolute path to file')
    args = parser.parse_args()
    # Unpacks the sole argument from `args`.
    (filepath,) = args.filepath
    # Normalize path for current OS.
    filepath = os.path.normpath(filepath)
    # Avoid FileNotFoundErrors along the way.
    if not os.path.exists(filepath):
        print(f'ERROR!\nFile {filepath!r} not found, check filename/path.')
        sys.exit(1)
    if not os.path.isfile(filepath):
        print(f'ERROR!\nGiven argument {filepath!r} is not a valid file.')
        sys.exit(2)
    # Execute main() in the try-except block to exit the program gracefully.
    try:
        main()
    except KeyboardInterrupt:  # User sends Ctrl-C
        print('\nProgram terminated by user. Shutting down.')
        sys.exit(0)
    except EOFError:  # User sends Ctrl-D or Ctrl-Z+Enter
        print('\nIllegal input: "EOF signal". This incident will be reported... ;) jk')
        sys.exit(0)
