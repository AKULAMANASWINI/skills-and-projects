"""Python 01 exercises. Replace each `raise NotImplementedError` with your code."""


def celsius_to_fahrenheit(c: float) -> float:
    """Convert Celsius to Fahrenheit: F = C * 9 / 5 + 32."""
    return c * 9 / 5 + 32


def is_even(n: int) -> bool:
    """True if n is even. Hint: the % operator."""
    return n % 2 == 0


def net_amount(quantity: int, unit_price: float, discount: float = 0.0) -> float:
    """Revenue for one order line, rounded to 2 decimals: quantity * unit_price * (1 - discount)."""
    return round(quantity * unit_price * (1 - discount), 2)


def price_band(unit_price: float) -> str:
    """'budget' below 30, 'mid' from 30 up to (not including) 100, 'premium' from 100.
    (Same rule as SQL 02 q8.)"""
    if unit_price < 30:
        return "budget"
    if unit_price < 100:
        return "mid"
    return "premium"


def sum_to_n(n: int) -> int:
    """Sum of 1 + 2 + ... + n using a loop. sum_to_n(0) is 0."""
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


def count_vowels(text: str) -> int:
    """Number of vowels (a, e, i, o, u — either case) in text."""
    count = 0
    for ch in text.lower():
        if ch in "aeiou":
            count += 1
    return count


def initials(full_name: str) -> str:
    """'  priya   reddy ' -> 'P.R.' : first letter of each word, uppercase, each followed by '.'.
    Extra spaces anywhere must not matter."""
    result = ""
    for word in full_name.split():
        result += word[0].upper() + "."
    return result


def fizzbuzz(n: int) -> list[str]:
    """For 1..n: 'Fizz' if divisible by 3, 'Buzz' by 5, 'FizzBuzz' by both, else the number as a string.
    fizzbuzz(5) == ['1', '2', 'Fizz', '4', 'Buzz']"""
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(str(i))
    return out
