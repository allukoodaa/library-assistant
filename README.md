# Library Assistant 3000

Library Assistant 3000 is a lightweight terminal companion for maintaining a plain-text catalog of books. Point it at a database file and it gives you a guided UI for browsing entries or appending new titles—perfect for quick experiments, coding assignments, or tiny personal collections.

## Features

- **Quick start:** Launch the CLI with a single file path argument.
- **Interactive menu:** Add new books or print the current database contents at any time.
- **Input validation:** Guards against empty titles/authors, non-numeric years, and malformed ISBNs.
- **Pretty printing:** Wide-format table output with a narrow-terminal fallback.
- **Safe updates:** Database stays sorted by publication year after every write.

## Getting Started

### Prerequisites

- Python 3.7+
- A database file containing one book per line in `Title/Author/ISBN/Year` format (sample files live in `test_data/`)

### Installation

```bash
git clone <your-fork-or-clone-url>
cd library_db
python3 --version  # ensure 3.7+
```

No additional dependencies are required for runtime.

## Usage

Run the assistant with the database you want to manage:

```bash
python my_library_db.py test_data/test_library.txt
```

You’ll see an introductory message followed by the main menu:

```
***Welcome to Library Assistant 3000!***

Reading given DB file...
DB file contains 3 lines.

What would you like to do next?
1) Add new book to database
2) Print current database content
Q) Quit
```

### Adding a Book

1. Choose option `1`.
2. Provide Title, Author, ISBN (should be 10 or 13 digits), and Year (numeric).
3. Review the preview of your entry.
4. Confirm to write it to the database, retry, or cancel.

Entries are stored as slash-separated fields and the file is re-sorted by year every time you add a book.

### Viewing the Database

Select option `2` to display all books.
- The recommended terminal width is ≥120 columns, absolute minimum for intended printing schema is 110. The standard pretty print renders the database entries in an aligned table with normalized whitespace.
- Narrower terminals automatically switch to an alternate, per-record layout—just press `Enter` to continue when prompted.

### Data Format

Each line in the database file uses `/` as a delimiter:

```
Title/Author/ISBN/Year
```

Example (`test_data/test_library.txt`):

```
Idiot/Fyodor Dostoyevsky/9780850670356/1971
Moby Dick/Herman Melville/9781974305032/1981
```

Feel free to start with the provided samples or create an empty file to begin fresh or run the program with your own data as long as it follows the same convention.

## Development Notes

- Source: `my_library_db.py`
- Optional tooling: `ruff` (listed under the `dev` extra in `pyproject.toml`)
    - To run linter: `ruff check`

## Troubleshooting

- **`File not found, check filename/path.`** Ensure you passed the correct relative or absolute path.
- **Terminal too narrow for table view.** Resize your window while in the main menu or continue with the alternate layout when prompted.
- **Interrupted session.** `Ctrl+C` or `Ctrl+D` exits gracefully; just rerun the command to restart the program.

## Disclaimer about AI use in the project

- Large test data file generated with **Mistral**
- README.md generated with **Codex**, edited by author.


## License

Licensed under the MIT License. See `LICENSE` for details.
