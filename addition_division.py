# addition
num1 = float(input("Enter first number for addition: "))
num2 = float(input("Enter second number for addition: "))
sum_result = num1 + num2
print(f"sum: {num1} + {num2} = {sum_result }")

enter first number for division: 5
enter second number for division: 6
sum: 5.0 + 6.0 = 11.0

# division
num3 = float(input("Enter the number for division: "))
num4 = float(input("Enter the number for division: "))
if num4 != 0:
    division_result = num3 / num4
    print(f"division: {num3} / {num4} = {division_result}")
    print("error: division by zero is not allowed")
else:
    div_result = num3 / num4
    print(f"division: {num3} / {num4} = {div_result}")

enter the number for division: 25
enter the number for division: 5
division: 25.0 / 5.0 = 5.0

