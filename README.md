# CGPA Calculator

A GUI application for calculating CGPA (Cumulative Grade Point Average) with current and future semester predictions. Built specifically for BRAC University's grading system.

## Features

- Calculate current CGPA with up to 5 decimal accuracy
- Predict future CGPA with semester plan system
- Attached standard grading scale display
- Dropdown to show Department-specific credit requirements
- Seperation Thesis/Internship grade inclusion option (4 credits)
- Manual CGPA input option for faster calculation
- Supports up to 5 courses per semester in prediction

## Installation & Usage

1. Download the latest release (`cg-calc.zip`) from the [releases page](https://github.com/ahshafin2315/cg-calc/releases)
2. Exclude file from antivirus block as it will be flagged malicious ([Virustotal Results](https://www.virustotal.com/gui/url/d557f5c32d2e3ca93ec6331df29a06b7a9ecdede140451c67e161d3449b5e4e0))
3. Extract the zip file to your preferred location
4. Run `cg-calc.exe` from the extracted folder
5. No installation required - just keep the extracted folder intact

## Quick Start Guide

### Current CGPA Calculation
1. Select your department from the dropdown
2. Enter number of courses for each grade you received
3. Enable thesis checkbox if completed and select grade
4. Click "Calculate Current CGPA"

### Future CGPA Prediction
1. Have your current CGPA calculated OR
2. Enable "Manual CGPA & Credit Input" and enter your details
3. Click "Add New Semester"
4. Add courses to each semester (max 5 per semester):
   - Select letter grade
   - Default credit is 3 (can be changed)
5. Add more semesters as needed
6. Click "Calculate Future CGPA"

### Tips
- Use the Clear All button (bottom right) to reset everything
- Remove individual courses using the X button
- Remove entire semesters using the X button
- Watch credit counts update automatically
- Check error messages for validation issues

## For Developers

### Setup
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

To create executable:

1. Navigate to the project directory:
   ```bash
   cd cg-calc
   ```
2. Running PyInstaller:
   ```bash
   pyinstaller --windowed --icon=app_icon.ico cg-calc.py
   ```
   - `--windowed`: Prevents console window from appearing
   - `--icon`: Specifies the application icon file
   
   The executable and its dependencies will be in the `dist/cg-calc` directory.
3. Creating distribution zip:
   - Navigate to `dist/cg-calc/` folder
   - Inside the folder you have all components and executable
   - Zip the compoments
   - The zip file is ready for distribution

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.
Contributions are welcome!

## License

This project is licensed under the MIT License - see the LICENSE file for details.


Thank You!
