# Implementation

## Requirements

## Final Requirements
### Functional
- The calculator must accept two numbers as input from the user.
- The calculator must perform addition, subtraction, multiplication and division on the input numbers.
- The calculator must display the result of the operation to the user.

### Non-Functional
- The calculator should be able to handle invalid inputs (e.g. non-numeric characters).
- The calculator should be able to handle overflow or underflow errors.

### Assumptions
- The user will enter two numbers and a valid arithmetic operator.
- The calculator will not need to perform any advanced calculations like polynomial equations or matrices.

### Constraints
- The calculator must run on a standard Linux/Unix environment.
- The calculator should use the minimum number of external libraries possible.

## Architecture
- **System Architecture**: The system will consist of a single script that takes user input, performs the desired operation, and displays the result.
- **Technology Choices**:
  - Programming Language: Python (version 3.8 or higher)
  - External Libraries: `argparse` for command-line argument parsing, `logging` for error logging

## Project Structure
```bash
calculator/
__init__.py
calculator.py
requirements.txt
```

## Code
```python
import argparse
import logging
import operator

# Configure basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def get_float_input(prompt):
    """Get a float input from the user."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            logging.error("Invalid input. Please enter a number.")

def perform_operation(num1, num2, operator_str):
    """Perform the desired operation on two numbers."""
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }
    if operator_str in operators:
        try:
            return operators[operator_str](num1, num2)
        except ZeroDivisionError:
            logging.error("Cannot divide by zero.")
            return None
    else:
        logging.error("Invalid operator. Please use '+', '-', '*', or '/'.")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--num1', type=float, required=True)
    parser.add_argument('--num2', type=float, required=True)
    parser.add_argument('--operator', type=str, choices=['+', '-', '*', '/'], required=True)
    args = parser.parse_args()

    # Get the input numbers and operator from the user
    num1 = get_float_input(f"Enter the first number: ")
    num2 = get_float_input(f"Enter the second number: ")

    # Perform the desired operation
    result = perform_operation(num1, num2, args.operator)

    if result is not None:
        logging.info(f"{num1} {args.operator} {num2} = {result}")

if __name__ == "__main__":
    main()
```

## Setup Instructions

### Install Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should contain the following line:

```
argparse==1.8.0
```

However, since `argparse` is a built-in Python module in version 3.2 and later, you can skip installing it if you're using a supported Python version.

### Run the Code

```bash
python calculator.py --num1 <number> --num2 <number> --operator <operator>
```

Replace `<number>` with the desired number, and `<operator>` with one of `+`, `-`, `*`, or `/`.

## Usage

To use the calculator from the terminal:

1. Run the script using the command above.
2. Enter two numbers when prompted.
3. Enter an arithmetic operator (`+`, `-`, `*`, or `/`) when prompted.
4. The result of the operation will be displayed in the console.

Note: This implementation assumes that the user will enter valid input. If you want to add more error handling, consider using a try-except block around the code that performs the operation.