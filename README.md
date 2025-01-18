# Shortcut CGPA Calculator

A comprehensive GUI application for calculating Cumulative Grade Point Average (CGPA) using Python and Tkinter, with enhanced features and a modern interface.

## Features

- Input grades either as numerical scores (0-100) or letter grades
- Dynamic addition and removal of course grades
- Real-time CGPA calculation
- Built-in quick calculator for grade calculations
- Comprehensive grading scale display
- Degree-specific credit requirements display for various departments
- Separate thesis/internship (4 credits) grade input
- Input validation and error handling
- Scrollable course management interface
- Modern UI with color themes and tooltips

## Installation & Usage

1. Download the latest release (`cg-calc.exe`) from the [releases page](https://github.com/ahshafin2315/cg-calc/releases)
2. Double-click the executable to run the application
3. No installation required - the application runs standalone

## Using the Calculator

1. Select your undergraduate program from the dropdown menu to see credit details
2. Enter the total credits completed (excluding thesis/internship)
3. Click "Add Course" to add course entries
4. For each course:
   - Select input type (Score or Letter Grade)
   - Enter the grade
   - Enter the course count (credit hours/units)
5. Enable thesis/internship checkbox if applicable and enter grade
6. The CGPA will be calculated automatically
7. Use the built-in calculator for quick calculations if needed
8. Use the 'X' button to remove any course entry
9. Click "Clear All" to reset all entries

## For Developers

If you want to run the Python source code directly:

1. Ensure you have Python 3.x installed
2. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/cg-calc.git
   ```
3. Install required packages:
   ```bash
   pip install pyinstaller
   ```
4. Run the script:
   ```bash
   python cg-calc.py
   ```

### Building the Executable

To create a standalone executable:

1. Navigate to the project directory:
   ```bash
   cd cg-calc
   ```
2. Run PyInstaller:
   ```bash
   pyinstaller --onefile --windowed --icon=app_icon.ico cg-calc.py
   ```
   - `--onefile`: Creates a single executable file
   - `--windowed`: Prevents console window from appearing
   - `--icon`: Specifies the application icon file

The executable will be created in the `dist` directory.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.
Contributions are welcome!

## License

This project is licensed under the MIT License - see the LICENSE file for details.


Thank You!
