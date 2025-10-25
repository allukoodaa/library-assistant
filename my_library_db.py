import argparse
import os
import sys


def main():
    print(
        '\n***Welcome to Library Assistant 3000!***\n\n'
        'Reading given DB file...'
    )
    db_content = read_file()
    print(f'DB file contains {len(db_content)} lines.')
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
            curr_content = read_file()
            pretty_print(curr_content)
        else:
            print('Please choose a valid option.')


def add_book():
    print('\nPlease input the information of the book you want to add to the database.')
    while True:
        title = input('Title: ')
        author = input('Author: ')
        isbn = input('ISBN: ')
        if not isbn.isnumeric() or len(isbn) > 13:
            print(f'ISBN must be numeric and less than 14 characters, was {isbn!r}\n')
            continue
        year = input('Year of publication: ')
        if not year.isnumeric():
            print(f'Year must contain only numbers, was {year!r}\n')
            continue
        book = [title, author, isbn, year]
        print('\nYour entry:')
        while True:
            pretty_print([book])
            print(
                '\nWould you like to add this book to the database?\n'
                '1) Yes\n2) Try again\n3) Return to main menu.\n'
                )
            cmd = input('Input command: ')
            if cmd =='1':
                update_db(book)
                return
            elif cmd == '2':
                break
            elif cmd == '3':
                print('Returning to main menu.\n')
                return
            else:
                print('Please choose a valid option.\n')


def pretty_print(content):
    content.sort(key=lambda line : int(line[-1]))
    if os.get_terminal_size().columns < 120:
        print("For best user experience, terminal window width should be at least 120.")
        alternate_pretty_print(content)
        return
    print(f'\n{"TITLE":<50}{"AUTHOR":<35}{"ISBN":<15}YEAR')
    for line in content:
        t, a, i, y = line
        print(f'{t:<50}{a:<35}{i:<15}{y}')


def alternate_pretty_print(content):
    input('Reverting to alternate printing. Press any key to continue. ')
    for index, line in enumerate(content, 1):
        t, a, i, y = line
        print(
            f'{index}:\nTitle: {t!r}\nAuthor: {a!r}\nISBN: {i!r}\nYear: {y!r}\n'
        )


def update_db(new_book):
    print('Updating database...')
    curr_content = read_file()
    curr_content.append(new_book)
    curr_content.sort(key=lambda line : int(line[-1]))
    write_file(curr_content)
    print('Database updated successfully!')


def read_file():
    with open(filepath) as file:
        content = [line.strip().split('/') for line in file.readlines()]
    return content


def write_file(content):
    with open(filepath, 'w') as file:
        for line in content:
            parsed_line = '/'.join(line) + '\n'
            file.write(parsed_line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Library DB Assistant 3000')
    parser.add_argument('filepath', nargs=1, help="filename or absolute path to file")
    args = parser.parse_args()
    filepath, = args.filepath
    filepath = os.path.normpath(filepath)
    if not os.path.exists(filepath):
        print('ERROR!\nFile not found, check filename/path.')
    try:
        main()
    except KeyboardInterrupt:
        print('\nProgram terminated by user. Shutting down.')
        sys.exit(0)
