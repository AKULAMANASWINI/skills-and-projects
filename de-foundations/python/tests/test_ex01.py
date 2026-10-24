from ex01_basics import (celsius_to_fahrenheit, count_vowels, fizzbuzz, initials, is_even,
                         net_amount, price_band, sum_to_n)


def test_celsius_to_fahrenheit():
    assert celsius_to_fahrenheit(0) == 32
    assert celsius_to_fahrenheit(100) == 212
    assert celsius_to_fahrenheit(-40) == -40


def test_is_even():
    assert is_even(4) is True
    assert is_even(7) is False
    assert is_even(0) is True


def test_net_amount():
    assert net_amount(2, 25.0) == 50.0
    assert net_amount(2, 25.0, 0.1) == 45.0
    assert net_amount(3, 19.99, 0.2) == 47.98


def test_price_band():
    assert price_band(10) == "budget"
    assert price_band(30) == "mid"
    assert price_band(99.99) == "mid"
    assert price_band(100) == "premium"


def test_sum_to_n():
    assert sum_to_n(0) == 0
    assert sum_to_n(1) == 1
    assert sum_to_n(100) == 5050


def test_count_vowels():
    assert count_vowels("Hyderabad") == 3
    assert count_vowels("AEIOU xyz") == 5
    assert count_vowels("") == 0


def test_initials():
    assert initials("priya reddy") == "P.R."
    assert initials("  manaswini   akula  ") == "M.A."
    assert initials("Ada") == "A."


def test_fizzbuzz():
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
    assert fizzbuzz(15)[-1] == "FizzBuzz"
    assert fizzbuzz(0) == []
