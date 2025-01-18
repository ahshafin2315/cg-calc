import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

GRADES = {
    "A+": 4.0,
    "A": 4.0,
    "A-": 3.7,
    "B+": 3.3,
    "B": 3.0,
    "B-": 2.7,
    "C+": 2.3,
    "C": 2.0,
    "C-": 1.7,
    "D+": 1.3,
    "D": 1.0,
    "D-": 0.7,
    "F": 0.0,
}

GRADE_RANGES = [
    (97, 100, "A+"),
    (90, 97, "A"),
    (85, 90, "A-"),
    (80, 85, "B+"),
    (75, 80, "B"),
    (70, 75, "B-"),
    (65, 70, "C+"),
    (60, 65, "C"),
    (57, 60, "C-"),
    (55, 57, "D+"),
    (52, 55, "D"),
    (50, 52, "D-"),
    (0, 50, "F"),
]

# Style configurations
COLORS = {
    "primary": "#2c3e50",  # Dark blue-gray
    "secondary": "#3498db",  # Blue
    "background": "#ecf0f1",  # Light gray
    "text": "#2c3e50",  # Dark blue-gray
    "error": "#e74c3c",  # Red
    "success": "#27ae60",  # Green
}

FONTS = {
    "header": ("Helvetica", 14, "bold"),
    "normal": ("Helvetica", 11),
    "normal-bold": ("Helvetica", 11, "bold"),
    "small": ("Helvetica", 10),
    "result": ("Helvetica", 14, "bold"),
}

# Undergrap Program Credit informations
PROGRAMS = {
    "Applied Physics and Electronics (APE)": {
        "credits": 130,
        "courses": ((130 - 4) / 3) + 1,
    },
    "Anthropology (ANT)": {"credits": 120, "courses": ((120 - 4) / 3) + 1},
    "Architecture (ARC)": {"credits": 207, "courses": ((207 - 4) / 3) + 1},
    "Biotechnology (BIO)": {"credits": 136, "courses": ((136 - 4) / 3) + 1},
    "Pharmacy": {"credits": 164, "courses": ((164 - 4) / 3) + 1},
    "Business Administration (BBA)": {"credits": 130, "courses": ((130 - 4) / 3) + 1},
    "Economics (ECO)": {"credits": 120, "courses": ((120 - 4) / 3) + 1},
    "Microbiology (MIC)": {"credits": 136, "courses": ((136 - 4) / 3) + 1},
    "Mathematics (MAT)": {"credits": 127, "courses": ((127 - 4) / 3) + 1},
    "Laws (LLB)": {"credits": 135, "courses": ((135 - 4) / 3) + 1},
    "Computer Science & Engineering (CSE)": {
        "credits": 136,
        "courses": ((136 - 4) / 3) + 1,
    },
    "Computer Science (CS)": {"credits": 124, "courses": ((124 - 4) / 3) + 1},
    "Electronic And Communication Engineering (ECE)": {
        "credits": 136,
        "courses": ((136 - 4) / 3) + 1,
    },
    "English (ENG)": {"credits": 120, "courses": ((120 - 4) / 3) + 1},
    "Physics": {"credits": 120, "courses": ((120 - 4) / 3) + 1},
    "Electrical and Electronic Engineering (EEE)": {
        "credits": 136,
        "courses": ((136 - 4) / 3) + 1,
    },
}


class CGPACalculator:
    def __init__(self):
        self.app = tk.Tk()
        self.app.title("CGPA Calculator")
        self.app.geometry("1000x800")
        self.app.resizable(True, True)  # Make window non-resizable
        # Add icon to window
        try:
            self.app.iconbitmap("app_icon.ico")
        except tk.TclError:
            pass  # Icon file not found, use default

        self.app.configure(bg=COLORS["background"])

        # Create style for ttk widgets
        self.style = ttk.Style()
        self.style.configure("Custom.TCombobox", padding=5)
        self.style.configure("Custom.TButton", padding=5)

        # Program selection variables
        self.selected_program = tk.StringVar()
        self.program_info_var = tk.StringVar()

        # Credit and course tracking variables
        self.total_credits = tk.StringVar()
        self.course_count_var = tk.StringVar()

        # Grade input options
        self.input_types = ["Letter Grade", "Score (0-100)"]
        self.grade_rows = []

        # Thesis related variables
        self.include_thesis = tk.BooleanVar()
        self.thesis_grade_var = tk.StringVar()
        self.thesis_letter_grade_var = tk.StringVar()
        self.thesis_input_type_var = tk.StringVar(value=self.input_types[0])

        # Display variables
        self.result_var = tk.StringVar(value="Current CGPA: ---")
        self.error_var = tk.StringVar()

        # Set up variable traces
        self.selected_program.trace_add("write", self.update_program_info)
        self.total_credits.trace_add("write", self.update_course_count)
        self.include_thesis.trace_add("write", self.update_course_count)

        # Add new traces for thesis updates
        self.thesis_input_type_var.trace_add("write", self.update_thesis_input)
        self.thesis_grade_var.trace_add("write", self.update_thesis_grade)

        # Add tooltip text
        self.thesis_tooltip = "Enable thesis/internship checkbox to input grade"

        # Add calculator variables
        self.calc_display = tk.StringVar(value="0")
        self.calc_expression = tk.StringVar(value="")  # New: shows full expression
        self.current_num = "0"
        self.prev_num = None
        self.operation = None
        self.new_number = True  # Flag to handle new number input

        self.setup_ui()

    def setup_ui(self):
        # Main container with padding
        main_frame = tk.Frame(self.app, bg=COLORS["background"], padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Content frame to hold left and right frames
        content_frame = tk.Frame(main_frame, bg=COLORS["background"])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Create left and right frames for split layout
        left_frame = tk.Frame(content_frame, bg=COLORS["background"])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right_frame = tk.Frame(content_frame, bg=COLORS["background"])
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Bottom frame for CGPA display
        bottom_frame = tk.Frame(
            main_frame,
            bg=COLORS["background"],
            height=10,
            relief="groove",
            borderwidth=1,
        )
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, pady=5)

        # Header with app name (in left frame)
        header_frame = tk.Frame(left_frame, bg=COLORS["background"])
        header_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            header_frame,
            text="CGPA Calculator",
            font=FONTS["header"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack()

        degree_frame = tk.Frame(left_frame, bg=COLORS["background"])
        degree_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            degree_frame,
            text="Undergrad Program Details:",
            font=FONTS["normal-bold"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(side=tk.LEFT, padx=5)

        # Degree selection
        degree_selector = ttk.Combobox(
            degree_frame,
            values=list(PROGRAMS.keys()),
            textvariable=self.selected_program,
            width=40,
            state="readonly",
        )
        degree_selector.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # Degree info display
        tk.Label(
            left_frame,
            textvariable=self.program_info_var,
            font=FONTS["normal"],
            bg=COLORS["background"],
            fg=COLORS["secondary"],
        ).pack(pady=5)

        # Credits completed frame
        credits_frame = tk.Frame(left_frame, bg=COLORS["background"])
        credits_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            credits_frame,
            text="Total credits completed (w/o thesis):",
            font=FONTS["normal"],
            bg=COLORS["background"],
        ).pack(side=tk.LEFT, padx=5)

        tk.Entry(
            credits_frame,
            textvariable=self.total_credits,
            width=10,
            font=FONTS["normal"],
        ).pack(side=tk.LEFT, padx=5)

        # Course count display
        tk.Label(
            left_frame,
            textvariable=self.course_count_var,
            font=FONTS["small"],
            bg=COLORS["background"],
            fg=COLORS["text"],
        ).pack(pady=5)

        # Thesis checkbox
        thesis_check = tk.Checkbutton(
            left_frame,
            text="Include Thesis/Internship (4 credits)",
            variable=self.include_thesis,
            bg=COLORS["background"],
            font=FONTS["normal"],
            command=self.toggle_thesis,
        )
        thesis_check.pack(pady=5)

        # Grading scale information
        info_frame = tk.Frame(
            left_frame, bg=COLORS["background"], relief="groove", borderwidth=1
        )
        info_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            info_frame,
            text="Grading Scale",
            font=FONTS["header"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(pady=5)

        tk.Label(
            info_frame,
            text="(BRAC University Undergrad Standard)",
            font=FONTS["normal-bold"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(pady=(5, 0))

        scale_frame = tk.Frame(info_frame, bg=COLORS["background"])
        scale_frame.pack(pady=5)

        # Grading scale labels with better formatting
        grades_info = [
            "97-100: A+ (4.0)  |  90-<97: A (4.0)  |  85-<90: A- (3.7)",
            "80-<85: B+ (3.3)  |  75-<80: B (3.0)  |  70-<75: B- (2.7)",
            "65-<70: C+ (2.3)  |  60-<65: C (2.0)  |  57-<60: C- (1.7)",
            "55-<57: D+ (1.3)  |  52-<55: D (1.0)  |  50-<52: D- (0.7)",
            "<50: F (0.0)",
        ]

        for info in grades_info:
            tk.Label(
                scale_frame,
                text=info,
                font=FONTS["small"],
                bg=COLORS["background"],
                fg=COLORS["text"],
            ).pack()

        # Add mini calculator
        calc_frame = tk.Frame(
            left_frame, bg=COLORS["background"], relief="groove", borderwidth=1
        )
        calc_frame.pack(fill=tk.X, pady=10)

        # Calculator title and expression display
        tk.Label(
            calc_frame,
            text="Quick Calculator",
            font=FONTS["normal-bold"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(pady=(5, 0))

        # Create a frame to hold both display and expression
        display_frame = tk.Frame(
            calc_frame, bg=COLORS["background"], relief="groove", borderwidth=1
        )
        display_frame.pack(expand=True, fill=tk.X, padx=150, pady=5)

        # Calculator input/display
        calc_entry = tk.Entry(
            display_frame,
            textvariable=self.calc_display,
            font=FONTS["normal"],
            justify="right",
            width=15,
            relief="solid",
        )
        calc_entry.pack(side=tk.LEFT, padx=(0, 5))

        # Expression display
        tk.Label(
            display_frame,
            textvariable=self.calc_expression,
            font=FONTS["small"],
            bg=COLORS["background"],
            fg=COLORS["text"],
            anchor="w",
            width=10,
        ).pack(side=tk.LEFT, padx=(5, 0))

        # Bind keyboard events
        calc_entry.bind("<Key>", self.handle_key)
        calc_entry.bind("<Return>", lambda e: self.calculator_click("="))
        calc_entry.bind("<Escape>", lambda e: self.calculator_click("C"))
        calc_entry.bind("<BackSpace>", self.handle_backspace)

        # Calculator buttons
        button_configs = [
            ("7", "8", "9", "/"),
            ("4", "5", "6", "*"),
            ("1", "2", "3", "-"),
            ("0", ".", "=", "+"),
            ("C", "CE"),
        ]

        for row in button_configs:
            btn_frame = tk.Frame(calc_frame, bg=COLORS["background"])
            btn_frame.pack(pady=2)

            for text in row:
                btn = tk.Button(
                    btn_frame,
                    text=text,
                    width=5,
                    font=FONTS["normal"],
                    relief="flat",
                    bg=(
                        COLORS["error"]
                        if text in "CE C"
                        else COLORS["secondary"] if text in "=/+-*" else "white"
                    ),
                    fg="white" if text in "=/+-*CE C" else COLORS["text"],
                    command=lambda x=text: self.calculator_click(x),
                )
                btn.pack(side=tk.LEFT, padx=2)

        # Organize right frame contents
        right_top_frame = tk.Frame(right_frame, bg=COLORS["background"])
        right_top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        # Create title for course management section
        tk.Label(
            right_top_frame,
            text="Course Management",
            font=FONTS["header"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(pady=(0, 10))

        # Add grade button at the top of right frame
        button_frame = tk.Frame(right_top_frame, bg=COLORS["background"])
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Add Course",
            font=FONTS["normal"],
            bg=COLORS["secondary"],
            fg="white",
            relief="flat",
            command=self.add_grade_row,
            padx=20,
            pady=5,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            button_frame,
            text="Clear All",
            font=FONTS["normal"],
            bg=COLORS["error"],
            fg="white",
            relief="flat",
            command=self.clear_all,
            padx=20,
            pady=5,
        ).pack(side=tk.LEFT, padx=5)

        # Create scrollable frame for course management with white background
        course_frame = tk.Frame(right_frame, bg="white", relief="solid", borderwidth=2)
        course_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=(5, 0))

        course_canvas = tk.Canvas(course_frame, bg="white")
        scrollbar = ttk.Scrollbar(
            course_frame, orient="vertical", command=course_canvas.yview
        )
        self.container = tk.Frame(course_canvas, bg="white")

        # Configure scrolling
        self.container.bind(
            "<Configure>",
            lambda e: course_canvas.configure(scrollregion=course_canvas.bbox("all")),
        )

        course_canvas.create_window((0, 0), window=self.container, anchor="nw")
        course_canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the scrollable components
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        course_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add thesis frame at the bottom of right frame
        thesis_frame = tk.Frame(right_frame, bg=COLORS["background"])
        thesis_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        # Thesis input setup
        tk.Label(
            thesis_frame,
            text="Thesis Grade:",
            font=FONTS["normal"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(side=tk.LEFT, padx=5)

        # Input type selector for thesis
        self.thesis_type_combo = ttk.Combobox(
            thesis_frame,
            values=self.input_types,
            textvariable=self.thesis_input_type_var,
            width=12,
            state="readonly",
            style="Custom.TCombobox",
        )
        self.thesis_type_combo.pack(side=tk.LEFT, padx=5)

        # Frame for thesis grade input
        self.thesis_grade_frame = tk.Frame(thesis_frame, bg=COLORS["background"])
        self.thesis_grade_frame.pack(side=tk.LEFT, padx=5)

        # Letter grade display
        self.thesis_letter_label = tk.Label(
            thesis_frame,
            textvariable=self.thesis_letter_grade_var,
            width=4,
            font=FONTS["normal"],
            bg=COLORS["background"],
        )
        self.thesis_letter_label.pack(side=tk.LEFT, padx=5)

        # Initialize thesis input and disable it
        self.update_thesis_input()
        self.toggle_thesis()

        # Add tooltip binding for thesis frame
        self.thesis_grade_frame.bind("<Enter>", self.show_tooltip)
        self.thesis_grade_frame.bind("<Leave>", self.hide_tooltip)
        self.thesis_type_combo.bind("<Enter>", self.show_tooltip)
        self.thesis_type_combo.bind("<Leave>", self.hide_tooltip)

        # Center the result display in bottom frame with better spacing
        result_frame = tk.Frame(bottom_frame, bg=COLORS["background"])
        result_frame.pack(expand=True, fill=tk.BOTH)

        # CGPA display with more prominent styling
        tk.Label(
            result_frame,
            textvariable=self.result_var,
            font=FONTS["result"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(expand=True, fill=tk.BOTH, pady=5)

        # Error message with enhanced visibility
        tk.Label(
            result_frame,
            textvariable=self.error_var,
            font=FONTS["normal"],
            bg=COLORS["background"],
            fg=COLORS["error"],
            wraplength=600,
        ).pack(expand=True, fill=tk.BOTH)

    def toggle_thesis(self):
        state = "normal" if self.include_thesis.get() else "disabled"
        fg_color = COLORS["primary"] if self.include_thesis.get() else "gray"

        # Update thesis input widgets
        self.thesis_type_combo.config(state=state)

        # Update all widgets in thesis_grade_frame
        for widget in self.thesis_grade_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.config(state=state)
            elif isinstance(widget, ttk.Combobox):
                widget.config(
                    state="readonly" if self.include_thesis.get() else "disabled"
                )

        # Update labels
        for widget in self.thesis_type_combo.master.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(fg=fg_color)

        self.thesis_letter_label.config(fg=fg_color)
        self.calculate_cgpa()

    def update_thesis_input(self, *args):
        for widget in self.thesis_grade_frame.winfo_children():
            widget.destroy()

        state = "normal" if self.include_thesis.get() else "disabled"

        if self.thesis_input_type_var.get() == "Score (0-100)":
            entry = tk.Entry(
                self.thesis_grade_frame,
                width=5,
                textvariable=self.thesis_grade_var,
                font=FONTS["normal"],
                relief="solid",
                state=state,
                validate="key",
                validatecommand=(self.app.register(self.validate_score), "%P"),
            )
            entry.pack(side=tk.LEFT)
        else:
            grade_selector = ttk.Combobox(
                self.thesis_grade_frame,
                values=list(GRADES.keys()),
                textvariable=self.thesis_grade_var,
                width=5,
                state="readonly" if self.include_thesis.get() else "disabled",
                style="Custom.TCombobox",
            )
            grade_selector.pack(side=tk.LEFT)

        # Reset and recalculate
        self.thesis_grade_var.set("")
        self.thesis_letter_grade_var.set("")
        self.calculate_cgpa()

    def update_thesis_grade(self, *args):
        input_val = self.thesis_grade_var.get()
        if input_val:
            letter = self.get_letter_grade(input_val, self.thesis_input_type_var.get())
            if self.thesis_input_type_var.get() == "Score (0-100)":
                self.thesis_letter_grade_var.set(letter if letter else "")
            else:
                self.thesis_letter_grade_var.set("")
        else:
            self.thesis_letter_grade_var.set("")
        self.calculate_cgpa()

    def get_letter_grade(self, value, input_type):
        if input_type == "Score (0-100)":
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
        frame = tk.Frame(self.container, bg="white")  # Changed background to white
        frame.pack(fill=tk.X, pady=5)

        grade_var = tk.StringVar()
        count_var = tk.StringVar()
        letter_grade_var = tk.StringVar()
        input_type_var = tk.StringVar(value=self.input_types[0])

        # Input type selector
        input_type = ttk.Combobox(
            frame,
            values=self.input_types,
            textvariable=input_type_var,
            width=12,
            state="readonly",
            style="Custom.TCombobox",
        )
        input_type.pack(side=tk.LEFT, padx=5)

        # Grade input (will be updated based on input type)
        grade_frame = tk.Frame(frame, bg="white")
        grade_frame.pack(side=tk.LEFT, padx=5)

        def update_grade_input(*args):
            # Clear grade frame
            for widget in grade_frame.winfo_children():
                widget.destroy()

            if input_type_var.get() == "Score (0-100)":
                tk.Entry(
                    grade_frame,
                    width=5,
                    textvariable=grade_var,
                    font=FONTS["normal"],
                    relief="solid",
                    validate="key",
                    validatecommand=(self.app.register(self.validate_score), "%P"),
                ).pack(side="left")
            else:
                grade_selector = ttk.Combobox(
                    grade_frame,
                    values=list(GRADES.keys()),
                    textvariable=grade_var,
                    width=5,
                    state="readonly",
                    style="Custom.TCombobox",
                )
                grade_selector.pack(side="left")

            # Reset grade value
            grade_var.set("")
            letter_grade_var.set("")

        # Letter grade display (only shown for numerical input)
        letter_label = tk.Label(
            frame,
            textvariable=letter_grade_var,
            width=4,
            font=FONTS["normal"],
            bg="white",
        )
        letter_label.pack(side=tk.LEFT, padx=5)

        tk.Label(frame, text="Count:", font=FONTS["normal"], bg="white").pack(
            side=tk.LEFT, padx=5
        )
        count_entry = tk.Entry(
            frame, width=5, textvariable=count_var, font=FONTS["normal"], relief="solid"
        )
        count_entry.pack(side=tk.LEFT, padx=5)

        # Delete button
        tk.Button(
            frame,
            text="×",
            font=("Helvetica", 12),
            bg=COLORS["error"],
            fg="white",
            relief="flat",
            command=lambda: self.delete_row(
                frame, (grade_var, count_var, letter_grade_var)
            ),
        ).pack(side=tk.LEFT, padx=5)

        def update_grade(*args):
            input_val = grade_var.get()
            if input_val:  # Changed from (input_val) to input_val for consistency
                letter = self.get_letter_grade(input_val, input_type_var.get())
                letter_grade_var.set(
                    letter if letter and input_type_var.get() == "Score (0-100)" else ""
                )
            else:
                letter_grade_var.set("")  # Clear letter grade when input is empty
            self.calculate_cgpa()

        input_type_var.trace_add("write", update_grade_input)
        grade_var.trace_add("write", update_grade)
        count_var.trace_add("write", self.calculate_cgpa)

        self.grade_rows.append((grade_var, count_var, letter_grade_var))
        update_grade_input()  # Initialize grade input

    def delete_row(self, frame, vars):
        self.grade_rows.remove(vars)
        frame.destroy()
        self.calculate_cgpa()

    def update_program_info(self, *args):
        program = self.selected_program.get()
        if program in PROGRAMS:
            info = PROGRAMS[program]
            regular_courses = (
                info["credits"] - 4
            ) / 3  # Deduct thesis credits and convert to courses
            self.program_info_var.set(
                f"Program requirement: {info['credits']} credits "
                f"({int(regular_courses)} regular courses + thesis/internship)"
            )

    def update_course_count(self, *args):
        if not self.total_credits.get().strip():
            self.course_count_var.set("")
            self.error_var.set("Please enter total credits completed")
            return
            
        try:
            credits = float(self.total_credits.get())
            courses = credits / 3
            thesis_text = " + thesis/internship" if self.include_thesis.get() else ""
            self.course_count_var.set(
                f"Equivalent to {courses:.1f} courses{thesis_text}"
            )
            self.calculate_cgpa()
        except ValueError:
            self.course_count_var.set("")

    def calculate_cgpa(self, *args):
        try:
            credits = float(self.total_credits.get() or 0)
            base_courses = credits / 3
            total_target = base_courses + (1 if self.include_thesis.get() else 0)
            current_total = 0
            total_points = 0
            total_credits = 0

            # Calculate for regular courses
            for grade_var, count_var, letter_grade_var in self.grade_rows:
                grade = grade_var.get()
                count = count_var.get()
                letter_grade = letter_grade_var.get() or grade

                if letter_grade and count and letter_grade in GRADES:
                    count = int(count)
                    current_total += count
                    credits_for_courses = count * 3
                    total_credits += credits_for_courses
                    total_points += GRADES[letter_grade] * credits_for_courses

            # Add thesis grade if included
            if self.include_thesis.get() and self.thesis_grade_var.get():
                thesis_grade = self.thesis_grade_var.get()
                thesis_letter = (
                    self.thesis_letter_grade_var.get()
                    if self.thesis_input_type_var.get() == "Score (0-100)"
                    else thesis_grade
                )

                if thesis_letter in GRADES:
                    current_total += 1
                    total_credits += 4
                    total_points += GRADES[thesis_letter] * 4

            # Show partial CGPA even if not all courses are added
            if total_credits > 0:
                cgpa = total_points / total_credits
                self.result_var.set(f"Current CGPA: {cgpa:.2f}")
            else:
                self.result_var.set("Current CGPA: - - -")

            # Update error/warning messages
            if total_target == 0:  # No credits entered yet
                self.error_var.set("")
            elif current_total > total_target:
                self.error_var.set(
                    f"Error: Total courses ({current_total}) exceeds target ({total_target:.0f})"
                )
            elif total_target > current_total:
                remaining = total_target - current_total
                self.error_var.set(
                    f"Remaining: {remaining:.0f} more course{'s' if remaining > 1 else ''} needed! Please add in course management."
                )
            elif current_total > 0:  # Only show success message if courses are added
                self.error_var.set("All required courses added!")

        except ValueError as e:
            self.error_var.set("Please enter valid numbers")
            if not self.total_credits.get():
                self.result_var.set("Current CGPA: - - -")

        except Exception as e:
            self.error_var.set(f"An error occurred: {str(e)}")
            self.result_var.set("Current CGPA: - - -")

    def validate_score(self, value):
        """Validate numeric score input"""
        if not value:  # Allow empty values
            return True
        try:
            score = float(value)
            return 0 <= score <= 100
        except ValueError:
            return False

    def show_tooltip(self, event=None):
        if not self.include_thesis.get():
            x, y, _, _ = event.widget.bbox("insert")
            x += event.widget.winfo_rootx() + 25
            y += event.widget.winfo_rooty() + 20

            # Create tooltip
            self.tooltip = tk.Toplevel(self.app)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")

            label = tk.Label(
                self.tooltip,
                text=self.thesis_tooltip,
                bg="lightyellow",
                font=FONTS["small"],
                relief="solid",
                borderwidth=1,
            )
            label.pack()

    def hide_tooltip(self, event=None):
        if hasattr(self, "tooltip"):
            self.tooltip.destroy()

    def clear_all(self):
        """Clear all inputs and reset calculator"""
        if messagebox.askyesno(
            "Confirm Clear", "Are you sure you want to clear all entries?"
        ):
            # Clear regular courses
            for frame, _ in [
                (child, child.destroy()) for child in self.container.winfo_children()
            ]:
                pass
            self.grade_rows.clear()

            # Clear thesis
            self.include_thesis.set(False)
            self.thesis_grade_var.set("")
            self.thesis_letter_grade_var.set("")
            self.thesis_input_type_var.set(self.input_types[0])

            # Clear credits
            self.total_credits.set("")
            self.selected_program.set("")

            # Reset result
            self.result_var.set("Current CGPA: - - -")
            self.error_var.set("")

    def handle_key(self, event):
        """Handle keyboard input for calculator"""
        if event.char.isdigit() or event.char == ".":
            self.calculator_click(event.char)
            return "break"
        elif event.char in "+-*/":
            self.calculator_click(event.char)
            return "break"
        return "break"  # Prevent default handling

    def handle_backspace(self, event):
        """Handle backspace in calculator input"""
        if self.current_num and not self.new_number:
            self.current_num = self.current_num[:-1] or "0"
            self.calc_display.set(self.current_num)
        return "break"

    def calculator_click(self, value):
        try:
            if value.isdigit() or value == ".":
                if self.new_number:
                    self.current_num = value
                    self.new_number = False
                else:
                    if value == "." and "." in self.current_num:
                        return
                    self.current_num = (self.current_num + value).lstrip("0") or "0"
                self.calc_display.set(self.current_num)

            elif value in "+-*/":
                if self.prev_num is not None and self.operation and not self.new_number:
                    self.calculate_result()
                self.prev_num = float(self.current_num or "0")
                self.operation = value
                self.new_number = True
                # Update expression display
                self.calc_expression.set(f"{self.prev_num} {value}")

            elif value == "=":
                if self.prev_num is not None and self.operation:
                    self.calculate_result()
                    self.calc_expression.set("")  # Clear expression after result
                    self.new_number = True

            elif value == "C":  # Clear all
                self.current_num = "0"
                self.prev_num = None
                self.operation = None
                self.new_number = True
                self.calc_display.set("0")
                self.calc_expression.set("")

            elif value == "CE":  # Clear entry
                self.current_num = "0"
                self.calc_display.set("0")
                self.new_number = True

        except Exception as e:
            self.calc_display.set("Error")
            self.calc_expression.set("")
            self.current_num = "0"
            self.prev_num = None
            self.operation = None
            self.new_number = True

    def calculate_result(self):
        try:
            current = float(self.current_num or "0")
            if self.operation == "/" and current == 0:
                raise ZeroDivisionError

            expression = f"{self.prev_num}{self.operation}{current}"
            result = eval(expression)  # Safe here as we control the input

            # Format result
            if result.is_integer():
                formatted = str(int(result))
            else:
                formatted = f"{result:.6f}".rstrip("0").rstrip(".")

            self.calc_display.set(formatted)
            self.current_num = formatted
            self.prev_num = None
            self.operation = None

        except ZeroDivisionError:
            self.calc_display.set("Error: Division by zero")
            self.current_num = "0"
            self.prev_num = None
            self.operation = None
            self.new_number = True

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    calculator = CGPACalculator()
    calculator.run()
