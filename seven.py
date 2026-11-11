# addition
num1 = float(input("Enter first number for addition: "))
num2 = float(input("Enter second number for addition: "))
sum_result = num1 + num2
print(f"sum: {num1} + {num2} = {sum_result}")

# division
num3 = float(input("Enter the number for division: "))
num4 = float(input("Enter the number for division: "))

if num4 != 0:
    division_result = num3 / num4
    print(f"division: {num3} / {num4} = {division_result}")
else:
    print("error: division by zero is not allowed")