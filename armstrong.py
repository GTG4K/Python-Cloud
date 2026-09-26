armstrong_numbers = []

def digit_count(n):
    digit_to_string = str(n)
    return len(digit_to_string)


def is_armstrong(n):
    power = digit_count(n)
    total = 0

    value = str(n)
    while len(value) > 0:
        digit = int(value[-1])
        total += digit ** power
        value = value[:-1]

    return total == n


for n in range(9, 10000):
    if is_armstrong(n):
        armstrong_numbers.append(n)


def sum_recursive(numbers, index=0):
    if index >= len(numbers):
        return 0
    return numbers[index] + sum_recursive(numbers, index + 1)


total = sum_recursive(armstrong_numbers)
