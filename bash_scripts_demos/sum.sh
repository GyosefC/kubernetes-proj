#!/bin/bash

echo "Enter the first number:"
read num1

echo "Enter the second number:"
read num2

# Check for numeric input
if [[ ! $num1 =~ ^[0-9]+$ || ! $num2 =~ ^[0-9]+$ ]]; then
  echo "Please enter only numbers."
  exit 1
fi


# Calculate the sum
sum=$((num1 + num2))

echo "The sum of numbers $num1 and $num2 is $sum."
