# Author: JIANGKUN CUI
# Date: 2024-07-08
# This program will calculate the monthly mortgage payment for different interest rates and years

# Declare variables and their values
principal = float(input("Enter the principal amount borrowed: "))
annual_interest_rate = float(input("Enter the annual interest rate as a percentage: "))

# Convert annual interest rate percentage to monthly decimal rate
monthly_interest_rate = (annual_interest_rate / 100) / 12

# Calculate and display payments for 5, 10, 15, 20, and 25 years
for years in range(5, 26, 5):
    number_of_months = years * 12

    monthly_payment = principal * (
        monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_months
    ) / (
        (1 + monthly_interest_rate) ** number_of_months - 1
    )

    print(f"The payment for interest rate {annual_interest_rate:.1f}% over {years} years is {monthly_payment:.0f}")