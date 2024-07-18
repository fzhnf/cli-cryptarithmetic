#!/usr/bin/env python3

"""
+------------------------+
| TUI Cryptarithm Solver |
+------------------------+
"""

import itertools

# def product(*iterables, repeat=1):
#     # https://docs.python.org/3/library/itertools.html#itertools.product
#     # product('ABCD', 'xy') → Ax Ay Bx By Cx Cy Dx Dy
#     # product(range(2), repeat=3) → 000 001 010 011 100 101 110 111
#
#     pools = [tuple(pool) for pool in iterables] * repeat
#
#     result = [[]]
#     for pool in pools:
#         result = [x + [y] for x in result for y in pool]
#
#     for prod in result:
#         yield tuple(prod)


def is_solution(words, result, mapping, operation):
    words_int = [int("".join(str(mapping[c]) for c in word)) for word in words]
    result_int = int("".join(str(mapping[c]) for c in result))

    if operation == "1":  # Addition
        return sum(words_int) == result_int
    elif operation == "2":  # Subtraction
        return words_int[0] - sum(words_int[1:]) == result_int
    elif operation == "3":  # Multiplication
        prod = 1
        for num in words_int:
            prod *= num
        return prod == result_int
    elif operation == "4":  # Division
        try:
            div = words_int[0]
            for num in words_int[1:]:
                div /= num
            return div == result_int
        except ZeroDivisionError:
            return False
    return False


def solve_cryptarithm(words, result, operation):
    unique_chars = set("".join(words) + result)
    initial_letters = "".join(set(itertools.chain(result[0], (a[0] for a in words))))
    word_len = [len(word) for word in words]

    # leading zeros not allowed by default
    prevent_leading_zero = True
    result_initial_letter_must_be_one = False
    if all(x == word_len[0] for x in word_len) and len(result) == word_len[0] + 1:
        print(f"{result[0]} must be 1")
        result_initial_letter_must_be_one = True

    # print(initial_letters)

    if len(unique_chars) > 10:
        print("Too many unique characters!")
        return

    digits = "0123456789"
    iter_num = 1
    solution_num = 1
    for perm in itertools.permutations(digits, len(unique_chars)):
        mapping = dict(zip(unique_chars, perm))

        if prevent_leading_zero and any(
            mapping[letter] == "0" for letter in initial_letters
        ):
            continue
        if result_initial_letter_must_be_one and mapping[result[0]] != "1":
            continue
        print(mapping[result[0]], end="\r")

        # print(f"iteration-{iter_num}:{mapping}", end="\r")
        iter_num += 1
        # for perm in permutations(digits, len(unique_chars)):
        # print(f"iter:{perm}")

        if is_solution(words, result, mapping, operation):
            print(f"\n{solution_num} Solution found")
            for word in words:
                print(f"{word} -> {''.join(mapping[c] for c in word)}")
            print(f"{result} -> {''.join(mapping[c] for c in result)}")
            solution_num += 1


def main():
    while True:
        print("Cryptarithm Solver")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")
        choice = input("Choose an operation: ")

        if choice == "5":
            break

        if choice not in "1234":
            print("Invalid choice!")
            continue

        # words = input("Enter the words (space-separated): ").split()
        # result = input("Enter the result word: ")
        words = "SEND MORE".upper().split()
        result = "MONEY".upper()
        print(f"{words} = {result}")

        solve_cryptarithm(words, result, choice)

        print("\nWould you like to solve another cryptarithm? (yes/no)")
        continue_choice = input().strip().lower()
        if continue_choice != "yes":
            break
        print("\n" * 3)  # Add empty lines


if __name__ == "__main__":
    main()
