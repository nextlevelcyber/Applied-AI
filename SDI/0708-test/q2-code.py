# Author: JIANGKUN CUI
# Date: 2024-07-08
#
# This program will calculate the monthly mortgage payment

# Declare variables and their values
principal = float(input("Enter the principal amount borrowed: "))
annual_interest_rate = float(input("Enter the annual interest rate as a percentage: "))
years = int(input("Enter the number of years: "))
# Convert the annual interest rate percentage into a monthly decimal rate
monthly_interest_rate = (annual_interest_rate / 100) / 12
# Convert years into total number of monthly payments
number_of_months = years * 12
# Calculate the monthly mortgage payment
monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_months) / ((1 + monthly_interest_rate) ** number_of_months - 1)
# Output the result
print(f"The payment for interest rate {annual_interest_rate:.2f}% over {years} years is {monthly_payment:.2f}")



