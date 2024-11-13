# PyQt6 Calculator

This project is a basic calculator GUI application built using Python and the PyQt6 library. It features a user-friendly interface with a variety of functionalities including arithmetic operations, memory storage, and special operations like percentage and square root calculation.

## Features

- Basic arithmetic operations: addition, subtraction, multiplication, and division.
- Memory functions: store and recall values.
- Percentage calculation and square root functions.
- Error handling for invalid operations (e.g., division by zero).
- Visual display of inputs and results using an LCD display.

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/JefeThePug/calculator.git
   cd calculator
    ```
   
2. **Install required libraries** (if not already installed):
    ```bash
    pip install PyQt6
    ```

## Usage

Run the game from the command line by executing:
```bash
    python calculator.py
```

## Code Overview

### Main Components

- **Colors**: Custom colors for various parts of the application are defined at the start for easy theme adjustments.
- **Calculator Window**: The main window (inherited from `QMainWindow`) contains the layout and functionality for buttons, the display, and memory indicators.
- **Button Actions**: Buttons are dynamically created and linked to their respective operations using partial functions.
- **Operations**: Functions handle different operations:
  - `append_to_number`: Manages number entry, including decimal handling.
  - `add_operator`: Adds arithmetic operators.
  - `totaling`: Evaluates the expression when `=` is pressed.
  - `percent`, `square root (√)`, and `memory functions (MR, M+, MC)`: Provides additional operations.
  - `clear`, `clear_mem`: Reset and memory clearing functions.

### Error Handling

- Displays `ERROR` on the LCD display for cases such as division by zero or invalid input.

### File Structure

All functionalities are contained within a single file, making it easy to run as a standalone application.

## Future Improvements

Potential future updates could include:
- Adding more complex operations (e.g., trigonometric functions).
- Saving calculation history.

## License

This project is open-source and available for modification and distribution.

---

Enjoy using this simple calculator app powered by PyQt6!
