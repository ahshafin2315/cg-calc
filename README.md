# Shortcut CGPA Calculator

A simple and user-friendly GUI application for calculating Cumulative Grade Point Average (CGPA) using Python and Tkinter.

## Features

- Input grades either as numerical scores (0-100) or letter grades
- Dynamic addition and removal of course grades
- Real-time CGPA calculation
- Comprehensive grading scale display
- Input validation and error handling

## Installation & Usage

1. Download the latest release (`cg-calc.exe`) from the releases page
2. Double-click the executable to run the application
3. No installation required - the application runs standalone

## Using the Calculator

1. Enter the total number of courses
2. Click "Add Grade" to add a new course entry
3. For each course:
   - Select input type (Score or Letter Grade)
   - Enter the grade
   - Enter the course count (credit hours/units)
4. The CGPA will be calculated automatically
5. Use the 'X' button to remove any course entry

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
