# Input two variables
a = float(input("Enter the first variable (a): "))
b = float(input("Enter the second variable (b): "))
# Display the original values
print(f"Original values: a = {a}, b = {b}")
# Swap the values using a temporary variable
temp = a
a = b
b = temp
# Display the swapped values
print(f"Swapped values: a = {a}, b = {b}")