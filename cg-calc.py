import tkinter as tk
from tkinter import ttk

GRADES = {
    'A+': 4.0,
    'A': 4.0,
    'A-': 3.7,
    'B+': 3.3,
    'B': 3.0,
    'B-': 2.7,
    'C+': 2.3,
    'C': 2.0,
    'C-': 1.7,
    'D+': 1.3,
    'D': 1.0,
    'D-': 0.7,
    'F': 0.0
}

GRADE_RANGES = [
    (97, 100, 'A+'),
    (90, 97, 'A'),
    (85, 90, 'A-'),
    (80, 85, 'B+'),
    (75, 80, 'B'),
    (70, 75, 'B-'),
    (65, 70, 'C+'),
    (60, 65, 'C'),
    (57, 60, 'C-'),
    (55, 57, 'D+'),
    (52, 55, 'D'),
    (50, 52, 'D-'),
    (0, 50, 'F')
]

# Style configurations
COLORS = {
    'primary': '#2c3e50',    # Dark blue-gray
    'secondary': '#3498db',  # Blue
    'background': '#ecf0f1', # Light gray
    'text': '#2c3e50',      # Dark blue-gray
    'error': '#e74c3c',     # Red
    'success': '#27ae60'    # Green
}

FONTS = {
    'header': ('Helvetica', 12, 'bold'),
    'normal': ('Helvetica', 10),
    'small': ('Helvetica', 9),
    'result': ('Helvetica', 14, 'bold')
}

class CGPACalculator:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("CGPA Calculator")
        self.app.geometry("500x700")
        # Add icon to window
        try:
            self.app.iconbitmap('app_icon.ico')
        except tk.TclError:
            pass  # Icon file not found, use default
        
        self.app.configure(bg=COLORS['background'])
        
        # Create style for ttk widgets
        self.style = ttk.Style()
        self.style.configure('Custom.TCombobox', padding=5)
        self.style.configure('Custom.TButton', padding=5)
        
        self.grade_rows = []
        self.total_courses = tk.StringVar()
        self.total_courses.trace_add('write', self.validate_total)  # Updated
        self.result_var = tk.StringVar()
        self.error_var = tk.StringVar()
        self.input_types = ['Letter Grade', 'Score (0-100)']  # Add input types
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.app, bg=COLORS['background'], padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header = tk.Label(main_frame, text="CGPA Calculator", 
                         font=('Helvetica', 16, 'bold'),
                         bg=COLORS['background'],
                         fg=COLORS['primary'],
                         pady=10)
        header.pack()

        # Total courses input frame
        input_frame = tk.Frame(main_frame, bg=COLORS['background'])
        input_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(input_frame, text="Total number of courses:", 
                font=FONTS['normal'],
                bg=COLORS['background'],
                fg=COLORS['text']).pack(side=tk.LEFT, padx=5)
        
        tk.Entry(input_frame, textvariable=self.total_courses,
                width=10,
                font=FONTS['normal'],
                relief='solid').pack(side=tk.LEFT, padx=5)

        # Grading scale information
        info_frame = tk.Frame(main_frame, bg=COLORS['background'],
                            relief='groove', borderwidth=1)
        info_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(info_frame, text="Grading Scale",
                font=FONTS['header'],
                bg=COLORS['background'],
                fg=COLORS['primary']).pack(pady=5)

        scale_frame = tk.Frame(info_frame, bg=COLORS['background'])
        scale_frame.pack(pady=5)
        
        # Grading scale labels with better formatting
        grades_info = [
            "97-100: A+ (4.0)  |  90-<97: A (4.0)  |  85-<90: A- (3.7)",
            "80-<85: B+ (3.3)  |  75-<80: B (3.0)  |  70-<75: B- (2.7)",
            "65-<70: C+ (2.3)  |  60-<65: C (2.0)  |  57-<60: C- (1.7)",
            "55-<57: D+ (1.3)  |  52-<55: D (1.0)  |  50-<52: D- (0.7)",
            "<50: F (0.0)"
        ]
        
        for info in grades_info:
            tk.Label(scale_frame, text=info,
                    font=FONTS['small'],
                    bg=COLORS['background'],
                    fg=COLORS['text']).pack()

        # Add grade button
        tk.Button(main_frame, text="Add Course",
                 font=FONTS['normal'],
                 bg=COLORS['secondary'],
                 fg='white',
                 relief='flat',
                 command=self.add_grade_row,
                 padx=20, pady=5).pack(pady=10)

        # Container for grade rows
        self.container = tk.Frame(main_frame, bg=COLORS['background'])
        self.container.pack(fill=tk.BOTH, expand=True)

        # Result and error labels
        self.result_var.set("Current CGPA: --")
        tk.Label(main_frame, textvariable=self.result_var,
                font=FONTS['result'],
                bg=COLORS['background'],
                fg=COLORS['primary']).pack(pady=10)
        
        tk.Label(main_frame, textvariable=self.error_var,
                font=FONTS['normal'],
                bg=COLORS['background'],
                fg=COLORS['error']).pack(pady=5)

    def get_letter_grade(self, value, input_type):
        if input_type == 'Score (0-100)':
            try:
                score = float(value)
                for min_score, max_score, letter in GRADE_RANGES:
                    if min_score <= score <= max_score:
                        return letter
            except ValueError:
                return None
        else:  # Letter Grade input
            return value if value in GRADES else None
        return None

    def add_grade_row(self):
        row = len(self.grade_rows)
        frame = tk.Frame(self.container, bg=COLORS['background'])
        frame.pack(fill=tk.X, pady=5)
        
        grade_var = tk.StringVar()
        count_var = tk.StringVar()
        letter_grade_var = tk.StringVar()
        input_type_var = tk.StringVar(value=self.input_types[0])
        
        # Input type selector
        input_type = ttk.Combobox(frame, values=self.input_types, 
                                 textvariable=input_type_var, width=12, state='readonly', style='Custom.TCombobox')
        input_type.pack(side=tk.LEFT, padx=5)
        
        # Grade input (will be updated based on input type)
        grade_frame = tk.Frame(frame, bg=COLORS['background'])
        grade_frame.pack(side=tk.LEFT, padx=5)
        
        def update_grade_input(*args):
            # Clear grade frame
            for widget in grade_frame.winfo_children():
                widget.destroy()
            
            if input_type_var.get() == 'Score (0-100)':
                tk.Entry(grade_frame, width=5, textvariable=grade_var, font=FONTS['normal'], relief='solid').pack(side='left')
            else:
                grade_selector = ttk.Combobox(grade_frame, values=list(GRADES.keys()), 
                                            textvariable=grade_var, width=5, state='readonly', style='Custom.TCombobox')
                grade_selector.pack(side='left')
            
            # Reset grade value
            grade_var.set('')
            letter_grade_var.set('')
        
        # Letter grade display (only shown for numerical input)
        letter_label = tk.Label(frame, textvariable=letter_grade_var, width=4, font=FONTS['normal'], bg=COLORS['background'])
        letter_label.pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame, text="Count:", font=FONTS['normal'], bg=COLORS['background']).pack(side=tk.LEFT, padx=5)
        count_entry = tk.Entry(frame, width=5, textvariable=count_var, font=FONTS['normal'], relief='solid')
        count_entry.pack(side=tk.LEFT, padx=5)
        
        # Delete button
        tk.Button(frame, text="×", font=('Helvetica', 12), bg=COLORS['error'], fg='white', relief='flat', 
                 command=lambda: self.delete_row(frame, (grade_var, count_var, letter_grade_var))).pack(side=tk.LEFT, padx=5)
        
        def update_grade(*args):
            input_val = grade_var.get()
            if input_val:
                letter = self.get_letter_grade(input_val, input_type_var.get())
                if input_type_var.get() == 'Score (0-100)':
                    letter_grade_var.set(letter if letter else '')
                else:
                    letter_grade_var.set('')
            self.calculate_cgpa()
        
        input_type_var.trace_add('write', update_grade_input)
        grade_var.trace_add('write', update_grade)
        count_var.trace_add('write', self.calculate_cgpa)
        
        self.grade_rows.append((grade_var, count_var, letter_grade_var))
        update_grade_input()  # Initialize grade input

    def delete_row(self, frame, vars):
        self.grade_rows.remove(vars)
        frame.destroy()
        self.calculate_cgpa()
        
    def validate_total(self, *args):
        self.calculate_cgpa()
        
    def calculate_cgpa(self, *args):
        try:
            total_target = int(self.total_courses.get())
            current_total = 0
            total_points = 0
            
            for grade_var, count_var, letter_grade_var in self.grade_rows:
                grade = grade_var.get()
                count = count_var.get()
                letter_grade = letter_grade_var.get() or grade
                
                if letter_grade and count and letter_grade in GRADES:
                    count = int(count)
                    current_total += count
                    total_points += GRADES[letter_grade] * count
            
            if current_total > total_target:
                self.error_var.set(f"Error: Total courses ({current_total}) exceeds target ({total_target})")
                self.result_var.set("")
            else:
                remaining = total_target - current_total
                if remaining > 0:
                    self.error_var.set(f"Warning: Still need to add {remaining} more course{'s' if remaining > 1 else ''}")
                else:
                    self.error_var.set("")
                
                if current_total > 0:
                    cgpa = total_points / current_total
                    self.result_var.set(f"Current CGPA: {cgpa:.2f}")
                else:
                    self.result_var.set("")
                    
        except (ValueError, KeyError):
            self.error_var.set("Please enter valid numbers")
            self.result_var.set("")
    
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    calculator = CGPACalculator()
    calculator.run()
