#!/usr/bin/env python3


def iter_product(*iterables, repeat=1):
    pools = [tuple(pool) for pool in iterables] * repeat

    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]

    for prod in result:
        yield tuple(prod)


def unique_product(*iterables):
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
    seen = set()
    result = [None] * n
    results = []
    inner(0)
    return results


def is_solution(words, result, mapping, operation) -> bool:
    words_int = [int("".join(str(mapping[c]) for c in word)) for word in words]
    result_int = int("".join(str(mapping[c]) for c in result))
    match operation:
        case "1":
            return sum(words_int) == result_int
        case "2":
            return words_int[0] - sum(words_int[1:]) == result_int

        case "3":
            prod = 1
            for num in words_int:
                prod *= num

            return prod == result_int

        case "4":
            div = words_int[0]
            for num in words_int[1:]:
                if num == 0:
                    return False
                div /= num
            return div == result_int
    return False


def solve_cryptarithm(words, result, operation) -> None:
    unique_chars = set("".join(words) + result)

    result_initial_letter = result[0]
    word_initial_letters = [word[0] for word in words]
    initial_letters = "".join(set([result_initial_letter] + word_initial_letters))
    word_len = [len(word) for word in words]

    # leading zeros not allowed by default
    prevent_leading_zero = True
    prevent_duplicate_character = True

    if len(unique_chars) > 10:
        print("Too many unique characters!")
        return

    digits = "0123456789"
    possibility = dict()

    for char in unique_chars:
        if prevent_leading_zero and char in initial_letters:
            possibility[char] = [*digits.replace("0", "")]
            continue
        possibility[char] = [*digits]

    if all(x == word_len[0] for x in word_len) and len(result) == word_len[0] + 1:
        possibility[result[0]] = ["1"]

    print(*possibility.items(), sep="\n")

    keys, values = zip(*possibility.items())
    n_solution = 1
    n_iteration = 1

    product = unique_product if prevent_duplicate_character else iter_product
    for combo in product(*values):
        mapping = dict(zip(keys, combo))
        print(f"iter-{n_iteration}:{mapping}", end="\r")
        if is_solution(words, result, mapping, operation):
            print(f"\n solution-{n_solution} found:")
            for word in words:
                print(f"{word} -> {''.join(mapping[c] for c in word)}")
            print(f"{result} -> {''.join(mapping[c] for c in result)}")
            n_solution += 1
        n_iteration += 1


def main():
    print("Cryptarithm Solver")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Exit")
    choice = input("Choose an operation: ")

    words = "II II".upper().split()
    result = "IUI".upper()
    print(f"{words} = {result}")

    solve_cryptarithm(words, result, choice)


if __name__ == "__main__":
    main()
