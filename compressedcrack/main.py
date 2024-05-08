import patoolib
import tempfile
from itertools import product
import argparse
import time
import sys

# Default Constants
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"
SPECIAL_CHARACTERS = "!@#$%^&*()-_+=~`[]{}|\\:;\"'<>,.?"


def test_archive_password(file_path, password, verbose):
    """
    Attempts to extract the archive using the specified password.

    Parameters:
    - file_path: The path to the archive file.
    - password: The password to attempt.
    - verbose: If True, prints additional information during the process.

    Returns:
    - True if the password successfully extracts the archive, False otherwise.
    """

    if verbose:
        sys.stdout.flush()
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            patoolib.extract_archive(
                file_path, outdir=temp_dir, verbosity=-1, interactive=False, password=password)
            return True
    except patoolib.util.PatoolError:
        return False


def calculate_password_combinations(start_length, max_length, character_set):
    return sum(len(character_set) ** i for i in range(start_length, max_length + 1))


def brute_force_password(file_path, start_length, max_length, character_set, verbose):
    """
    Generates password combinations within specified length range and character set,
    testing each against the provided archive.

    Parameters:
    - file_path: Path to the archive file to be cracked.
    - start_length: Minimum length of passwords to generate.
    - max_length: Maximum length of passwords to generate.
    - character_set: Characters to use for generating passwords.
    - verbose: If True, enables verbose output.

    Returns:
    - The correct password if found, otherwise None.
    - Total number of passwords tried.
    - Time taken to process the last subset of passwords.
    """

    total_password_count = 0
    for length in range(start_length, max_length + 1):
        start_time = time.time()
        password_count = 0
        # if verbose, print total number of passwords will be generated
        if verbose:
            print("-" * 50)
            print(
                f"\nGenerating passwords with length {length}...")
            print(
                f"\nTotal passwords to be generated: {len(character_set) ** length}")
        for password_tuple in product(character_set, repeat=length):
            password = ''.join(password_tuple)
            password_count += 1
            total_password_count += 1
            if test_archive_password(file_path, password, verbose):
                print(f"\nPassword is correct: {password}")
                return password, total_password_count, time.time() - start_time
        end_time = time.time()
        if verbose:
            print(
                f"\nNo password match found for {password_count} passwords generated with length {length}.")
            print(
                f"Total time for this subset: {end_time - start_time:.2f} seconds")
    return None, total_password_count, 0


def customize_character_set(default_set, set_name):
    custom_set = input(
        f"The default {set_name} is: {default_set}\nDo you want to customize this {set_name} set? (y/n): ")
    if custom_set.lower().startswith('y'):
        custom_set = input(f"Enter your custom {set_name} set: ")
        return custom_set
    return default_set


def main():
    """
    Main function to parse command line arguments and initiate the brute force process.
    """
    parser = argparse.ArgumentParser(
        description="Crack password-protected archives using brute force.")
    parser.add_argument("file_path", help="Path to the compressed file.")
    parser.add_argument("--min-length", type=int, default=1,
                        help="Minimum password length.")
    parser.add_argument("--max-length", type=int, default=5,
                        help="Maximum password length.")
    parser.add_argument("--verbose", action="store_true",
                        help="Increase output verbosity.")

    args = parser.parse_args()

   # Interactive character set definition with customization option
    character_set = ""
    if input("Include letters? (y/n): ").lower().startswith('y'):
        character_set += customize_character_set(LETTERS, "letters")
    if input("Include numbers? (y/n): ").lower().startswith('y'):
        character_set += customize_character_set(NUMBERS, "numbers")
    if input("Include special characters? (y/n): ").lower().startswith('y'):
        character_set += customize_character_set(
            SPECIAL_CHARACTERS, "special characters")

    if not character_set:
        print("\nNo characters selected. Using default character set.")
        character_set = LETTERS + NUMBERS + SPECIAL_CHARACTERS

    # Print the character set to be used
    print(f"\nCharacter set to be used: {character_set}")
    print(
        f"Total password combinations to be tried: {calculate_password_combinations(args.min_length, args.max_length, character_set)}")

    overall_start_time = time.time()
    password, total_password_count, subset_time = brute_force_password(
        args.file_path, args.min_length, args.max_length, character_set, args.verbose)
    overall_end_time = time.time()
    overall_time = overall_end_time - overall_start_time

    if password:
        print(f"\nPassword found: {password}")
    else:
        print("\nPassword not found.")
    print(f"Total passwords tried: {total_password_count}")
    print(f"Total execution time: {overall_time:.2f} seconds")


if __name__ == "__main__":
    main()
