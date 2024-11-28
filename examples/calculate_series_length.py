def series(last_digit: int, increment: int) -> int:
    count = 1 # The first number.

    next_num = last_digit + increment
    while next_num < 10000:
        count += 1
        next_num += increment

    return count

print(f"F1: {series(4,6)}")
print(f"F2: {series(2,6)}")
print(f"F3: {series(6,6)}")

print(f"M1: {series(1,6)}")
print(f"M2: {series(3,6)}")
print(f"M3: {series(5,6)}")
