import patoolib
import tempfile
from itertools import product
import argparse
import time
import sys
from tqdm import tqdm

# Default Constants
LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUMBERS = "0123456789"
SPECIAL_CHARACTERS = "!@#$%^&*()-_+=~`[]{}|\\:;\"'<>,.?"

def test_archive_password(file_path, password, verbose):
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
    total_password_count = 0
    for length in range(start_length, max_length + 1):
        start_time = time.time()
        password_count = 0

        # Create tqdm progress bar for the current password length
        total_combinations = len(character_set) ** length
        progress_bar = tqdm(product(character_set, repeat=length),
                            total=total_combinations,
                            desc=f"Trying passwords of length {length}",
                            unit="password")

        for password_tuple in progress_bar:
            password = ''.join(password_tuple)
            password_count += 1
            total_password_count += 1

            if test_archive_password(file_path, password, verbose):
                progress_bar.close()  # Close the progress bar
                print(f"\nPassword is correct: {password}")
                return password, total_password_count, time.time() - start_time

            # Update the progress bar description with attempts count
            progress_bar.set_postfix({"Attempts": password_count})

        progress_bar.close()
        end_time = time.time()
        if verbose:
            print(f"\nNo password match found for {password_count} passwords generated with length {length}.")
            print(f"Total time for this subset: {end_time - start_time:.2f} seconds")

    return None, total_password_count, 0

def customize_character_set(default_set, set_name):
    custom_set = input(
        f"The default {set_name} is: {default_set}\nDo you want to customize this {set_name} set? (y/n): ")
    if custom_set.lower().startswith('y'):
        custom_set = input(f"Enter your custom {set_name} set: ")
        return custom_set
    return default_set

def main():
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

    character_set = ""
    if input("Include letters? (y/n): ").lower().startswith('y'):
        character_set += customize_character_set(LETTERS, "letters")
    if input("Include numbers? (y/n): ").lower().startswith('y'):
        character_set += customize_character_set(NUMBERS, "numbers")
    if input("Include special characters? (y/n): ").lower().startswith('y'):
        character_set += customize_character_set(SPECIAL_CHARACTERS, "special characters")

    if not character_set:
        print("\nNo characters selected. Using default character set.")
        character_set = LETTERS + NUMBERS + SPECIAL_CHARACTERS

    print(f"\nCharacter set to be used: {character_set}")
    print(f"Total password combinations to be tried: {calculate_password_combinations(args.min_length, args.max_length, character_set)}")

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
