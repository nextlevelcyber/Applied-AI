# Author: JIANGKUN CUI
# Date: 2024-07-08
#
# This program will calculate the volume of a pyramid

# user need to input the pyramid dimensions
base_length = float(input("Enter the base length: "))
base_width = float(input("Enter the base width: "))
height = float(input("Enter the height: "))

# Calculate the volume using the formula: V = lwh / 3
volume = (base_length * base_width * height) / 3

# Output the results to the user
print(f"The volume of the pyramid with base {base_length:.2f} x {base_width:.2f} and height {height:.2f} is {volume:.2f}")