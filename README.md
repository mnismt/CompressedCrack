# CompressedCrack

![Banner](./assets/banner.png)

[![](https://img.shields.io/badge/Chat_with_CompressedCrack-Ask_Cody-%238A16D7?labelColor=%23383838)](https://sourcegraph.com/github.com/mnismt/CompressedCrack)

CompressedCrack is a command-line tool that utilizes the brute-force method to crack any password-protected compressed file. It generates password combinations based on user-defined character sets and length range, and attempts to extract the archive using each generated password until the correct password is found.

## Features

- Supports various compressed file formats (e.g., zip, rar, 7z) using `patoolib` library.
- Allows customization of character sets (letters, numbers, special characters).
- Configurable minimum and maximum password lengths.
- Displays the found password, total number of attempts, and execution time.
- Verbose mode for detailed output during the cracking process.

## Requirements

- Python >= 3.6

## Installation

You can install CompressedCrack directly from pip using the following command:

```
pip install compressedcrack
```

## Usage

```
compressedcrack [-h] [--min-length MIN_LENGTH] [--max-length MAX_LENGTH] [--verbose] file_path

Crack password-protected archives using brute force.

positional arguments:
  file_path             Path to the compressed file.

options:
  -h, --help            show this help message and exit
  --min-length MIN_LENGTH
                        Minimum password length.
  --max-length MAX_LENGTH
                        Maximum password length.
  --verbose             Increase output verbosity.

```

### Customizing Character Sets

When the script is started, the user will be asked for selecting character sets, including letters, numbers and special characters.

Default character sets:

- Letters: `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ`
- Numbers: `0123456789`
- Special characters: `!@#$%^&\*()-\_+=~[]{}|\:;"'<>,.?\`

If no character types are selected, the script will use the combination of all default character sets.

## Examples

Crack a password-protected file `archive.zip` with a minimum password length of 3 characters, maximum password length of 5 characters, verbose output, and the custom character set is `abcdef12345`:

```
compressedcrack --min-length 3 --max-length 5 --verbose archive.zip
```

![Example](./assets/example.gif)
