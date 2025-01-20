import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Grading scale for BRACU Undergrad Standard
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
    "AppName": ("Helvetica", 16, "bold"),
    "header": ("Helvetica", 14, "bold"),
    "subheader": ("Helvetica", 12, "bold"),
    "normal": ("Helvetica", 10),
    "normal-bold": ("Helvetica", 10, "bold"),
    "small": ("Helvetica", 9),
    "result": ("Helvetica", 14, "bold"),
}

# BRACU Undergrad Program Credit informations
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
        self.app.geometry("960x780") # Set window size
        self.app.resizable(False, False) # Make window non-resizable
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

        # Grade input options
        self.grade_rows = []

        # Thesis related variables
        self.thesis_grade = tk.StringVar()

        # Display variables
        self.calculate_future_btn = None  # To store the calculate future button
        
        self.manual_cgpa = tk.StringVar()
        self.thesis_frame = None
        
        # Consolidate tracking variables
        self.tracking = {
            "current_cgpa": None,
            "semester_count": 0,
            "semesters": [],
            "semester_list": {}
        }
        
        # Consolidate state variables
        self.state = {
            "manual_input_enabled": tk.BooleanVar(value=False),
            "include_thesis": tk.BooleanVar(),
            "error_var": tk.StringVar(),
            "program_info_var": tk.StringVar()
        }
        
        # Consolidate result variables
        self.results = {
            "current_result": tk.StringVar(value="Calculated CGPA: ---"),
            "future_result": tk.StringVar(value="Future CGPA: ---"),
            "total_credits": tk.StringVar(),
            "total_course_count": tk.StringVar()
        }

        # Set up variable traces
        self.selected_program.trace_add("write", self.update_program_info)
        self.results["total_credits"].trace_add("write", self.update_course_count)
        self.state["include_thesis"].trace_add("write", self.update_course_count)
        self.thesis_grade.trace_add("write", self.calculate_cgpa)

        # Add tooltip text
        self.thesis_tooltip = "Enable thesis/internship checkbox to input grade"

        # Add calculator variables
        self.grade_counts = {grade: tk.StringVar(value="0") for grade in GRADES.keys()}
        
        self.SETUP_UI()

    # FULL UI SETUP
    def SETUP_UI(self):
        # Main container with padding
        main_frame = tk.Frame(self.app, bg=COLORS["background"], padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Split into left and right frames with clear separation

        left_frame = tk.Frame(main_frame, bg=COLORS["background"], width=450)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        left_frame.pack_propagate(False)  # Maintain width

        separator = ttk.Separator(main_frame, orient="vertical")
        separator.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        right_frame = tk.Frame(main_frame, bg=COLORS["background"], width=450)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        right_frame.pack_propagate(False)  # Maintain width

        self.SETUP_left_frame(left_frame)
        self.SETUP_right_frame(right_frame)
    def SETUP_left_frame(self, parent):

        # Header & Instructions frame
        self.SETUP_instruction_frame(parent)

        # Degree selection frame
        self.SETUP_degree_frame(parent)

        # Include Thesis frame
        self.SETUP_thesis_section(parent)

        # BRACU Grading scale information frame
        self.SETUP_gradeInfo_frame(parent)

        # Grade count input section Frame
        self.SETUP_gradeInput_grid(parent)

        # Calculate button and Result display
        self.SETUP_result_frame(parent)
    def SETUP_right_frame(self, parent):
        # Header
        tk.Label(
            parent,
            text="Future CGPA Prediction",
            font=FONTS["AppName"],
            bg=COLORS["background"],
            fg=COLORS["secondary"],
        ).pack(pady=10)

        # Manual input frame
        self.SETUP_ManualInput_frame(parent)

        # Add semester button
        tk.Button(
            parent,
            text="Add New Semester",
            command=self.add_semester_box,
            bg=COLORS["secondary"],
            fg="white",
            font=FONTS["normal-bold"],
        ).pack(pady=5)

        # Semester container
        self.SETUP_scrollable_semester_frame(parent)

        # Calculate button
        self.calculate_future_btn = tk.Button(
            parent,
            text="Calculate Future CGPA",
            command=self.calculate_all_semesters,
            font=FONTS["normal-bold"],
            bg=COLORS["secondary"],
            fg="white",
        )
        self.calculate_future_btn.pack(pady=5)

        # Future CGPA display
        tk.Label(
            parent,
            textvariable=self.results["future_result"],
            font=FONTS["result"],
            bg=COLORS["background"],
            fg=COLORS["secondary"],
        ).pack(pady=8)

        # Clear All button at bottom right
        tk.Button(
            parent,
            text="Clear All",
            command=self.clear_all,
            font=FONTS["normal-bold"],
            bg=COLORS["error"],
            fg="white",
        ).pack(side=tk.BOTTOM, anchor=tk.SE, padx=10, pady=5)
    
    # LEFT FRAMES
    def SETUP_instruction_frame(self, parent):
        # Add header for current CGPA section
        tk.Label(
            parent,
            text="Current CGPA Calculator",
            font=FONTS["AppName"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(pady=5)

        # Add instructions
        instruction_frame = tk.Frame(parent, bg=COLORS["background"], relief="groove", borderwidth=1)
        instruction_frame.pack(fill=tk.X, pady=10, padx=5)
        
        tk.Label(
            instruction_frame,
            text="Calculate Your Current CGPA Upto 5 Decimal Accuracy",
            font=FONTS["subheader"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(pady=(5,0))
        
        tk.Label(
            instruction_frame,
            text="1. Select a degree from dropdown to see credit details\n2. Input below the number of courses you got each respected grade\n3. Include thesis/internship grade if completed",
            font=FONTS["normal"],
            bg=COLORS["background"],
            fg=COLORS["text"],
            justify="left",
        ).pack(pady=5)
    def SETUP_degree_frame(self, parent):
        degree_frame = tk.Frame(parent, bg=COLORS["background"])
        degree_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            degree_frame,
            text="Undergrad Degree Details:",
            font=FONTS["normal-bold"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(side=tk.LEFT, padx=5)

        # Degree selector dropdown
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
            parent,
            textvariable=self.state["program_info_var"],
            font=FONTS["normal"],
            bg=COLORS["background"],
            fg=COLORS["secondary"],
        ).pack(pady=5)
    def SETUP_thesis_section(self, parent):
        self.thesis_frame = tk.Frame(parent, bg=COLORS["background"])
        self.thesis_frame.pack(fill=tk.BOTH, pady=5)

        # Thesis label and grade selector
        tk.Label(
            self.thesis_frame,
            text="Thesis Grade:",
            font=FONTS["normal"],
            bg=COLORS["background"],
        ).pack(side=tk.LEFT, padx=5)

        grade_selector = ttk.Combobox(
            self.thesis_frame,
            values=list(GRADES.keys()),
            textvariable=self.thesis_grade,
            width=5,
            state="disabled",  # Initially disabled
            style="Custom.TCombobox",
        )
        grade_selector.pack(side=tk.LEFT, padx=5)

        tk.Checkbutton(
            self.thesis_frame,
            text="Include (4 Credits)",
            variable=self.state["include_thesis"],
            bg=COLORS["background"],
            command=self.toggle_thesis,
        ).pack(side=tk.LEFT, padx=5)
    def SETUP_gradeInfo_frame(self, parent):
        info_frame = tk.Frame(
            parent, bg=COLORS["background"], relief="groove", borderwidth=1
        )
        info_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            info_frame,
            text="Grading Scale (BRACU Undergrad Standard)",
            font=FONTS["subheader"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(pady=5)

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
    def SETUP_gradeInput_grid(self, parent):
        self.grade_counts_frame = tk.Frame(parent, bg=COLORS["background"])
        self.grade_counts_frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Header for grade input section
        tk.Label(
            self.grade_counts_frame,
            text="Course Count per Grade",
            font=FONTS["subheader"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(pady=(5,5))

        # Create grid frame
        grid_frame = tk.Frame(self.grade_counts_frame, bg=COLORS["background"])
        grid_frame.pack(pady=5)

        # Organize grades in a 4x4 grid
        row = 0
        col = 0
        for letter in GRADES.keys():
            frame = tk.Frame(grid_frame, bg=COLORS["background"])
            frame.grid(row=row, column=col, padx=2, pady=2)

            grade_text = f"{letter} ({GRADES[letter]:.1f})"
            tk.Label(
                frame,
                text=grade_text,
                font=FONTS["normal"],
                width=8,
                bg=COLORS["background"],
            ).pack(side=tk.LEFT)

            tk.Entry(
                frame,
                textvariable=self.grade_counts[letter],
                width=4,
                font=FONTS["normal"],
                state="normal",
            ).pack(side=tk.LEFT, padx=2)

            col += 1
            if col > 3:  # 4 columns
                col = 0
                row += 1

        # Course count display
        tk.Label(
            parent,
            textvariable=self.results["total_course_count"],
            font=FONTS["small"],
            bg=COLORS["background"],
            fg=COLORS["text"],
        ).pack(pady=5)

        # Button container for calculate button
        button_frame = tk.Frame(self.grade_counts_frame, bg=COLORS["background"])
        button_frame.pack(pady=10)

        # Calculate button
        self.calculate_btn = tk.Button(
            button_frame,
            text="Calculate Current CGPA",
            command=self.calculate_cgpa,
            font=FONTS["normal-bold"],
            bg=COLORS["secondary"],
            fg="white",
            state="normal",
        )
        self.calculate_btn.pack(pady=5)
    def SETUP_result_frame(self, parent):
        # Add result display frame after grade count section
        result_display = tk.Frame(parent, bg=COLORS["background"], relief="groove", borderwidth=1)
        result_display.pack(fill=tk.X, pady=10, padx=5)
        
        tk.Label(
            result_display,
            textvariable=self.results["current_result"],
            font=FONTS["result"],
            bg=COLORS["background"],
            fg=COLORS["primary"],
        ).pack(pady=5)

        tk.Label(
            result_display,
            textvariable=self.state["error_var"],
            font=FONTS["normal"],
            bg=COLORS["background"],
            fg=COLORS["error"],
            wraplength=400,
        ).pack(pady=5)

    # RIGHT FRAMES
    def SETUP_ManualInput_frame(self, parent):
        # Manual CGPA input section
        manual_frame = tk.Frame(parent, bg=COLORS["background"], relief="groove", borderwidth=1)
        manual_frame.pack(fill=tk.X, pady=5, padx=5)

        header_frame = tk.Frame(manual_frame, bg=COLORS["background"])
        header_frame.pack(fill=tk.X, pady=5)

        # Manual input toggle
        tk.Checkbutton(
            header_frame,
            text="Manual CGPA & Credit Input",
            variable=self.state["manual_input_enabled"],
            command=self.toggle_manual_input,
            bg=COLORS["background"],
        ).pack(side=tk.LEFT, padx=5)

        input_frame = tk.Frame(manual_frame, bg=COLORS["background"])
        input_frame.pack(pady=5)

        # Manual CGPA input
        tk.Label(
            input_frame,
            text="Current CGPA",
            font=FONTS["normal-bold"],
            bg=COLORS["background"],
        ).pack(side=tk.LEFT, padx=5)

        self.manual_cgpa_entry = tk.Entry(
            input_frame,
            textvariable=self.manual_cgpa,
            width=9,
            justify="center",
            state="disabled",
            font=FONTS["normal"],
        )
        self.manual_cgpa_entry.pack(side=tk.LEFT, padx=5)

        # Total credits input
        tk.Label(
            input_frame,
            text="Completed Total Credits:",
            font=FONTS["normal-bold"],
            bg=COLORS["background"],
        ).pack(side=tk.LEFT, padx=5)

        self.credits_entry = tk.Entry(
            input_frame,
            textvariable=self.results["total_credits"],
            width=10,
            justify="center",
            state="disabled",
            font=FONTS["normal"],
        )
        self.credits_entry.pack(side=tk.LEFT, padx=5)
    def SETUP_scrollable_semester_frame(self, parent):
        # Create scrollable container
        container = tk.Frame(parent, bg=COLORS["background"])
        container.pack(fill=tk.BOTH, expand=True, pady=5)

        # Create canvas with scrollbar
        self.canvas = tk.Canvas(container, bg="white")
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        
        # Create main frame for semesters
        self.semester_frame = tk.Frame(self.canvas, bg="white")
        self.semester_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Add the frame to the canvas
        self.canvas.create_window((0, 0), window=self.semester_frame, anchor="nw", width=430)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind mousewheel scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

    # HELPER FUNCTIONS
    def _reset_display(self):
        """Reset display after error"""
        self.results["current_result"].set("Calculated CGPA: ---")
        self.calculate_btn.config(bg=COLORS["secondary"])
    def update_program_info(self, *args):
        program = self.selected_program.get()
        if (program in PROGRAMS):
            info = PROGRAMS[program]
            regular_courses = (info["credits"] - 4) / 3  # Deduct thesis credits and convert to courses
            self.state["program_info_var"].set(
                f"Program requirement: {info['credits']} credits "
                f"({int(regular_courses)} regular courses + thesis/internship)"
            )
    def update_course_count(self, *args):
        """Update course count and maintain total credits"""
        total_courses = 0
        total_credits = 0
        
        # Calculate from grade inputs
        for grade, count_var in self.grade_counts.items():
            try:
                count = int(count_var.get() or 0)
                total_courses += count
                total_credits += count * 3  # Each course is 3 credits
            except ValueError:
                continue
        
        # Add thesis credits if included
        if self.state["include_thesis"].get():
            total_credits += 4
            thesis_text = " + thesis/internship"
        else:
            thesis_text = ""
            
        # Update displays
        self.results["total_course_count"].set(f"Total courses: {total_courses}{thesis_text}")
        
        # Only update total_credits if not in manual mode
        if not self.state["manual_input_enabled"].get():
            self.results["total_credits"].set(str(total_credits))
    def _create_semester_ui(self, semester_data):
        """Create and return UI elements for a semester"""
        # Create container
        container = tk.Frame(self.semester_frame, bg="white", relief="groove", borderwidth=1)
        container.pack(fill=tk.X, pady=5, padx=5)

        # Header frame
        header_frame = tk.Frame(container, bg="white")
        header_frame.pack(fill=tk.X, pady=5)

        # Left side: Semester number
        tk.Label(
            header_frame,
            text=f"Semester {semester_data['number']}",
            font=FONTS["subheader"],
            bg="white",
        ).pack(side=tk.LEFT, padx=5)

        # Right side: Stats and delete button
        right_frame = tk.Frame(header_frame, bg="white")
        right_frame.pack(side=tk.RIGHT, padx=5)

        # Delete semester button
        tk.Button(
            right_frame,
            text=chr(10005),
            command=lambda: self.delete_semester(container, semester_data),
            bg=COLORS["error"],
            fg="white",
            font=FONTS["normal"],
        ).pack(side=tk.RIGHT, padx=5)

        # Stats display
        tk.Label(
            right_frame,
            textvariable=semester_data["stats"]["course_count"],
            font=FONTS["small"],
            bg="white",
        ).pack(side=tk.RIGHT, padx=5)

        tk.Label(
            right_frame,
            textvariable=semester_data["stats"]["credits_count"],
            font=FONTS["small"],
            bg="white",
        ).pack(side=tk.RIGHT, padx=5)

        # Course container
        course_frame = tk.Frame(container, bg="white")
        course_frame.pack(fill=tk.X, pady=5)

        # Add course button
        tk.Button(
            container,
            text="Add Course",
            command=lambda: self.add_course_to_semester(semester_data),
            bg=COLORS["secondary"],
            fg="white",
            font=FONTS["normal-bold"],
        ).pack(pady=5)

        return {
            "container": container,
            "course_frame": course_frame
        }
    def add_semester_box(self):
        semester = {
            "number": self.tracking["semester_count"] + 1,
            "courses": [],
            "stats": {
                "course_count": tk.StringVar(value="0/5 courses"),
                "credits_count": tk.StringVar(value="Credits: 0")
            }
        }
        
        # Create UI elements
        semester["ui"] = self._create_semester_ui(semester)
        
        # Update tracking
        self.tracking["semester_count"] += 1
        self.tracking["semesters"].append(semester)
        self.tracking["semester_list"][semester["number"]] = semester
        
    def delete_semester(self, container, semester_data):
        """Delete a semester and update numbering"""
        try:
            if semester_data in self.tracking["semesters"]:
                self.tracking["semesters"].remove(semester_data)
            container.destroy()
            
            # Decrease semester count
            self.tracking["semester_count"] = len(self.tracking["semesters"])
            
            # Renumber remaining semesters
            for i, semester in enumerate(self.tracking["semesters"], 1):
                try:
                    semester["number"] = i
                    if "ui" in semester and "container" in semester["ui"]:
                        for widget in semester["ui"]["container"].winfo_children():
                            if isinstance(widget, tk.Frame):
                                for w in widget.winfo_children():
                                    if isinstance(w, tk.Label):
                                        w.config(text=f"Semester {i}")
                                        break
                except Exception as e:
                    print(f"Debug - Renumbering error: {str(e)}")
                    continue
            
            # Update button states
            self._update_future_calculation_state()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete semester: {str(e)}")
    def add_course_to_semester(self, semester_data):
        if len(semester_data["courses"]) >= 5:
            messagebox.showwarning("Limit Reached", "Maximum 5 courses allowed per semester")
            return

        course_frame = tk.Frame(semester_data["ui"]["course_frame"], bg="white")
        course_frame.pack(fill=tk.X, pady=2, padx=5)

        # Course inputs
        tk.Label(
            course_frame,
            text=f"Course {len(semester_data['courses']) + 1}:",
            font=FONTS["normal-bold"],
            bg="white",
        ).pack(side=tk.LEFT, padx=5)

        grade_var = tk.StringVar()
        credit_var = tk.StringVar(value="3")

        grade_combo = ttk.Combobox(
            course_frame,
            textvariable=grade_var,
            values=list(GRADES.keys()),
            width=5,
            state="readonly",
        )
        grade_combo.pack(side=tk.LEFT, padx=5)
        grade_combo.set("")  # Clear initial value

        tk.Entry(
            course_frame,
            textvariable=credit_var,
            width=5,
            font=FONTS["normal"],
        ).pack(side=tk.LEFT, padx=5)

        # Remove button
        tk.Button(
            course_frame,
            text=chr(10005),
            command=lambda: self.remove_course(course_frame, semester_data, (grade_var, credit_var)),
            bg=COLORS["error"],
            fg="white",
        ).pack(side=tk.RIGHT, padx=5)

        semester_data["courses"].append((grade_var, credit_var))
        
        # Update counters
        def update_stats(*args):
            try:
                credits = sum(float(cred.get() or 0) for _, cred in semester_data["courses"])
                if "stats" in semester_data:
                    semester_data["stats"]["credits_count"].set(f"Credits: {credits}")
                    semester_data["stats"]["course_count"].set(f"{len(semester_data['courses'])}/5 courses")
            except (ValueError, KeyError, AttributeError) as e:
                messagebox.showerror("Error", "Failed to update semester stats")
                print(f"Debug - Update stats error: {str(e)}")

        grade_var.trace_add("write", update_stats)
        credit_var.trace_add("write", update_stats)
        update_stats()
    def remove_course(self, frame, semester_data, course_vars):
        try:
            semester_data["courses"].remove(course_vars)
            frame.destroy()
            
            # Update course numbers safely
            for i, frame in enumerate(semester_data["ui"]["course_frame"].winfo_children(), 1):
                for widget in frame.winfo_children():
                    if isinstance(widget, tk.Label) and "Course" in widget.cget("text"):
                        widget.config(text=f"Course {i}:")
                        break
            
            # Update counters with safer access
            if "stats" in semester_data:
                credits = sum(float(cred.get() or 0) for _, cred in semester_data["courses"])
                semester_data["stats"]["credits_count"].set(f"Credits: {credits}")
                semester_data["stats"]["course_count"].set(f"{len(semester_data['courses'])}/5 courses")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove course: {str(e)}")
    def toggle_thesis(self):
        state_update = "readonly" if self.state["include_thesis"].get() else "disabled"
        for widget in self.thesis_frame.winfo_children():
            if isinstance(widget, ttk.Combobox):
                widget.config(state=state_update)
        self.calculate_cgpa()
    def toggle_manual_input(self):
        """Toggle manual CGPA input with proper credit sync"""
        if self.state["manual_input_enabled"].get():
            # Enable manual input
            self.manual_cgpa_entry.config(state="normal")
            self.credits_entry.config(state="normal")
            
            # Set current values if available
            if self.tracking["current_cgpa"]:
                self.manual_cgpa.set(f"{self.tracking['current_cgpa']:.5f}")
            else:
                self.manual_cgpa.set("")
                
            # Don't clear credits if they're already calculated
            if not self.results["total_credits"].get():
                self.credits_entry.delete(0, tk.END)
        else:
            # Disable manual input
            self.manual_cgpa_entry.config(state="disabled")
            self.credits_entry.config(state="disabled")
            
            # Sync with calculated values
            if self.tracking["current_cgpa"]:
                self.manual_cgpa.set(f"{self.tracking['current_cgpa']:.5f}")
            else:
                self.manual_cgpa.set("")
    def calculate_all_semesters(self):
        """Simplified future CGPA calculation"""
        try:
            # Get current CGPA and credits
            if self.state["manual_input_enabled"].get():
                try:
                    current_cgpa = float(self.manual_cgpa.get() or 0)
                    current_credits = float(self.results["total_credits"].get() or 0)
                    if current_cgpa == 0 or current_credits == 0:
                        messagebox.showwarning("Invalid Input", "Please enter valid CGPA and credits")
                        return
                except ValueError:
                    messagebox.showwarning("Invalid Input", "Invalid CGPA or credits format")
                    return
            elif self.tracking["current_cgpa"]:
                current_cgpa = self.tracking["current_cgpa"]
                current_credits = float(self.results["total_credits"].get())
            else:
                messagebox.showwarning("No CGPA", "Calculate current CGPA first or use manual input")
                return

            # Process each semester
            for semester in self.tracking["semesters"]:
                for grade_var, credit_var in semester["courses"]:
                    if not grade_var.get() or not credit_var.get():
                        messagebox.showwarning("Missing Data", f"Missing grade or credit in Semester {semester['number']}")
                        return

            # Calculate future CGPA
            total_points = current_cgpa * current_credits
            total_credits = current_credits

            for semester in self.tracking["semesters"]:
                for grade_var, credit_var in semester["courses"]:
                    credits = float(credit_var.get())
                    total_credits += credits
                    total_points += GRADES[grade_var.get()] * credits

            if total_credits > current_credits:
                future_cgpa = total_points / total_credits
                self.results["future_result"].set(
                    f"Future CGPA after {len(self.tracking['semesters'])} semester{'s' if len(self.tracking['semesters'])>1 else ''}: {future_cgpa:.5f}"
                )
            else:
                messagebox.showwarning("No Future Courses", "Add future courses to calculate")

        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
            self.results["future_result"].set("Future CGPA: Not calculated")
    def clear_all(self):
        """Clear all inputs and reset calculator"""
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear all entries?"):
            # Clear grade counts
            for var in self.grade_counts.values():
                var.set("0")
            
            # Clear thesis data
            self.state["include_thesis"].set(False)
            self.thesis_grade.set("")
            
            # Clear program selection
            self.selected_program.set("")
            
            # Clear result variables
            self.results["total_credits"].set("")
            self.results["current_result"].set("Calculated CGPA: ---")
            self.results["future_result"].set("Future CGPA: ---")
            
            # Clear tracking data
            self.tracking["current_cgpa"] = None
            
            # Clear all semesters
            for semester in self.tracking["semesters"][:]:  # Create a copy to iterate
                self.delete_semester(semester["ui"]["container"], semester)
            
            # Reset buttons
            self.calculate_btn.config(bg=COLORS["secondary"])
            self.calculate_future_btn.config(state="disabled")
            
            # Reset manual input if enabled
            if self.state["manual_input_enabled"].get():
                self.state["manual_input_enabled"].set(False)
                self.toggle_manual_input()

    # CGPA CALCULATION
    def calculate_cgpa(self, *args):
        try:
            totals = self._calculate_grade_totals()
            
            if totals["credits"] > 0:
                cgpa = totals["points"] / totals["credits"]
                self._update_cgpa_display(cgpa, totals["credits"])
            else:
                messagebox.showwarning("No Data", "No valid grades entered")
                self._reset_display()
                
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
            self._reset_display()
    def _calculate_grade_totals(self):
        totals = {"points": 0, "credits": 0, "courses": 0}
        
        # Calculate regular courses
        for letter, count_var in self.grade_counts.items():
            count = self._safe_int(count_var.get())
            if count > 0:
                totals["courses"] += count
                totals["credits"] += count * 3
                totals["points"] += GRADES[letter] * count * 3
        
        # Add thesis if included
        if self.state["include_thesis"].get() and self.thesis_grade.get():
            totals["credits"] += 4
            totals["points"] += GRADES[self.thesis_grade.get()] * 4
            
        return totals
    def _update_cgpa_display(self, cgpa, credits):
        """Update display with calculated CGPA"""
        self.tracking["current_cgpa"] = cgpa
        self.results["current_result"].set(f"Current CGPA: {cgpa:.5f}")
        self.calculate_btn.config(bg=COLORS["success"])
        self.state["error_var"].set("")
        
        # Update total credits if not in manual mode
        if not self.state["manual_input_enabled"].get():
            self.results["total_credits"].set(str(credits))
            
        # Enable future CGPA calculation
        self.calculate_future_btn.config(state="normal")
    def _safe_int(self, value):
        """Safely convert string to integer"""
        try:
            return int(value.strip() or 0)
        except ValueError:
            return 0
    def _update_future_calculation_state(self):
        """Helper method to update future calculation button state"""
        try:
            if self.state["manual_input_enabled"].get() and self.manual_cgpa.get() and self.results["total_credits"].get():
                self.calculate_future_btn.config(state="normal")
            elif not self.state["manual_input_enabled"].get() and self.tracking["current_cgpa"]:
                self.calculate_future_btn.config(state="normal")
            else:
                self.calculate_future_btn.config(state="disabled")
                self.results["future_result"].set("Future CGPA: Not calculated")
        except Exception as e:
            print(f"Debug - Button state update error: {str(e)}")


if __name__ == "__main__":
    calculator = CGPACalculator()
    calculator.app.mainloop()