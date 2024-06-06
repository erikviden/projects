from functools import cache
import time

def calculate_factorial(value):
    result = 1
    for number in range(1, value + 1):
        result *= number
    return result

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        calculation_time = end - start
        with open("factorial.txt", "a") as file:
            file.write(f"Calculation time of factorial {args[0]} is {calculation_time}\n")
        return result
    return wrapper

@measure_time
@cache
def factorial(value):
    return calculate_factorial(value)

values = [1, 9, 27, 88, 175, 299, 512, 1024]

for value in values:
    print(f"Factorial {value}: {factorial(value)}")