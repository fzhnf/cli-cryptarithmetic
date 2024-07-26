#!/usr/bin/env python3

# leading zeros not allowed by default
from collections.abc import Iterable

prevent_leading_zero = True
prevent_duplicate_character = True

possibility: dict = {}


def constraint(f):
    possibility.setdefault(f.__name__, f)


@constraint
def sum_constraint(words, result):
    possibilities = dict()
    words_length = [len(word) for word in words]

    if (
        all(i == words_length[0] for i in words_length)
        and len(result) == words_length[0] + 1
    ):
        possibilities[result[0]] = ["1"]

    return possibilities


def iter_product(*iterables, repeat=1) -> Iterable:
    pools = [tuple(pool) for pool in iterables] * repeat
    result: list = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]

    for prod in result:
        yield tuple(prod)


def unique_product(*iterables) -> Iterable:
    def inner(i):
        if i == n:
            results.append(tuple(result))
            return
        for pool in pools[i] - seen:
            seen.add(pool)
            result[i] = pool
            inner(i + 1)
            seen.remove(pool)

    pools = [set(pool) for pool in iterables]
    n = len(pools)
    seen: set = set()
    result: list = [None] * n
    results: list = []
    inner(0)
    return results


def is_solution(words, result, mapping, operation) -> bool:
    words_counts = [float("".join(str(mapping[c]) for c in word)) for word in words]
    result_count = float("".join(str(mapping[c]) for c in result))
    match operation:
        case "1":
            return sum(words_counts) == result_count
        case "2":
            return words_counts[0] - sum(words_counts[1:]) == result_count

        case "3":
            prod = 1.0
            for num in words_counts:
                prod *= num

            return prod == result_count

        case "4":
            div = words_counts[0]
            for num in words_counts[1:]:
                if num == 0.0:
                    return False
                div /= num
            return div == result_count
    return False


def solve_cryptarithm(words, result, operation) -> None:
    unique_chars: set = set("".join(words) + result)
    if len(unique_chars) > 10:
        print("Too many unique characters!")
        return

    possibilities: dict[str, list[str]] = sum_constraint(words, result)

    digits: str = "0123456789"
    result_initial_letter: str = result[0]
    word_initial_letters = [word[0] for word in words]
    initial_letters = "".join(set([result_initial_letter] + word_initial_letters))
    for char in initial_letters:
        if possibilities.get(char) is None:
            possibilities[char] = [*digits.replace("0", "")]

    for char in unique_chars:
        if possibilities.get(char) is None:
            possibilities[char] = [*digits]

    print(*possibilities.items(), sep="\n")

    keys, values = zip(*possibilities.items())
    n_solution = 1
    n_iteration = 1
    product: Iterable = (
        unique_product(*values)
        if prevent_duplicate_character
        else iter_product(*values)
    )

    for combo in product:
        mapping = dict(zip(keys, combo))
        print(f"iter-{n_iteration}:{mapping}", end="\r")
        if is_solution(words, result, mapping, operation):
            print(f"\n solution-{n_solution} found:")
            for word in words:
                print(f"{word} -> {''.join(mapping[c] for c in word)}")
            print(f"{result} -> {''.join(mapping[c] for c in result)}")
            n_solution += 1
        n_iteration += 1


def main() -> None:
    print("Cryptarithm Solver")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")
    choice: str = input("Choose an operation: ")

    words: list[str] = str("II II").split(" ")
    result: str = "HIU"
    print(f"{words} = {result}")

    solve_cryptarithm(words, result, choice)


if __name__ == "__main__":
    main()
