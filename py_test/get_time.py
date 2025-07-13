import time
from datetime import datetime
import random

def test_method(lambda_func, num_cycles=10):
    time_ls = []

    for _ in range(num_cycles):
        start = time.time()
        lambda_func()
        end = time.time()
        time_ls.append(end-start)

    return sum(time_ls)/num_cycles


def method1():
    now = datetime.now()
    current_time = now.strftime("%I:%M %p")

def method2():
    now = time.localtime()
    current_time = time.strftime("%I:%M %p", now)

def create_equation(target_number):
    """
    create equation of addition or subtraction
    
    target_number is the number the equation should equal
    
    returns: string representation of the equation
    """
    # randomly chosen between addition and subtraction
    operation = random.choice(['+', '-'])
    
    if operation == '+':
        # addition, pick a number smaller than target, add the difference
        if target_number <= 1:
            first_num = 0
            second_num = target_number
        else:
            first_num = random.randint(1, target_number - 1)
            second_num = target_number - first_num
        return f"{first_num} + {second_num}"
    
    else:  # subtraction
        # subtraction, pick a number larger than target, subtract the difference
        first_num = random.randint(target_number + 1, 99)
        second_num = first_num - target_number
        return f"{first_num} - {second_num}"

def display_albert_clock(hour, minute):
    
    hour_equation = create_equation(hour)
    minute_equation = create_equation(minute)
    
    print(f"The hour is {hour_equation} = {hour}")
    print(f"The minute is {minute_equation} = {minute}")
    print(f"Albert Clock: ({hour_equation}):({minute_equation})")

if __name__ == "__main__":
    now = datetime.now()

    current_time = now.strftime("%I:%M %p")

    print(current_time)

    current_hour = now.hour % 12
    if current_hour == 0:
      current_hour = 12

    # gets the current time using the second method which is faster
    now = time.localtime()

    # formats the current time as "HH:MM AM/PM" (12-hour format)
    current_time = time.strftime("%I:%M %p", now)
    print("Current time:", current_time)

    # get current hour and convert from 24-hour to 12-hour format
    current_hour = now.tm_hour % 12
    # makes it so 12am hour 0 will display as 12
    if current_hour == 0:
        current_hour = 12

    print("The hour is", current_hour)
    print("The minute is", now.tm_min)
    print("--------------")

    # display the Albert Clock
    display_albert_clock(current_hour, now.tm_min)

    """
    print(test_method(lambda_func=method1, num_cycles=100))
    print(test_method(lambda_func=method2, num_cycles=100))
    """
     
