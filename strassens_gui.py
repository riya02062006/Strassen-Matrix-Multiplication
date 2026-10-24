import customtkinter as ctk
from tkinter import messagebox
import time


# ============================================================
# MATRIX OPERATIONS
# ============================================================

def add_matrix(A, B):
    n = len(A)
    return [
        [A[i][j] + B[i][j] for j in range(n)]
        for i in range(n)
    ]


def subtract_matrix(A, B):
    n = len(A)
    return [
        [A[i][j] - B[i][j] for j in range(n)]
        for i in range(n)
    ]


def normal_multiply(A, B):
    n = len(A)

    result = [
        [0 for _ in range(n)]
        for _ in range(n)
    ]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += A[i][k] * B[k][j]

    return result


def next_power_of_two(n):
    power = 1

    while power < n:
        power *= 2

    return power


# ============================================================
# BASIC STRASSEN RECURSIVE FUNCTION
# ============================================================

def strassen_recursive(A, B):

    n = len(A)

    # Base case
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    mid = n // 2

    # --------------------------------------------------------
    # Divide A
    # --------------------------------------------------------

    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    # --------------------------------------------------------
    # Divide B
    # --------------------------------------------------------

    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]

    # --------------------------------------------------------
    # Seven Strassen Products
    # --------------------------------------------------------

    M1 = strassen_recursive(
        add_matrix(A11, A22),
        add_matrix(B11, B22)
    )

    M2 = strassen_recursive(
        add_matrix(A21, A22),
        B11
    )

    M3 = strassen_recursive(
        A11,
        subtract_matrix(B12, B22)
    )

    M4 = strassen_recursive(
        A22,
        subtract_matrix(B21, B11)
    )

    M5 = strassen_recursive(
        add_matrix(A11, A12),
        B22
    )

    M6 = strassen_recursive(
        subtract_matrix(A21, A11),
        add_matrix(B11, B12)
    )

    M7 = strassen_recursive(
        subtract_matrix(A12, A22),
        add_matrix(B21, B22)
    )

    # --------------------------------------------------------
    # Calculate C quadrants
    # --------------------------------------------------------

    C11 = add_matrix(
        subtract_matrix(
            add_matrix(M1, M4),
            M5
        ),
        M7
    )

    C12 = add_matrix(M3, M5)

    C21 = add_matrix(M2, M4)

    C22 = add_matrix(
        subtract_matrix(
            add_matrix(M1, M3),
            M2
        ),
        M6
    )

    # --------------------------------------------------------
    # Combine quadrants
    # --------------------------------------------------------

    result = []

    for i in range(mid):
        result.append(C11[i] + C12[i])

    for i in range(mid):
        result.append(C21[i] + C22[i])

    return result


# ============================================================
# STRASSEN WITH IMPORTANT INTERMEDIATE STEPS
# ============================================================

def strassen_with_steps(A, B):

    original_size = len(A)

    # --------------------------------------------------------
    # Padding
    # --------------------------------------------------------

    size = next_power_of_two(original_size)

    padded_A = [
        row[:] + [0] * (size - original_size)
        for row in A
    ]

    while len(padded_A) < size:
        padded_A.append([0] * size)

    padded_B = [
        row[:] + [0] * (size - original_size)
        for row in B
    ]

    while len(padded_B) < size:
        padded_B.append([0] * size)

    # --------------------------------------------------------
    # If size is 1
    # --------------------------------------------------------

    if size == 1:

        result = strassen_recursive(
            padded_A,
            padded_B
        )

        return result, {}

    mid = size // 2

    # --------------------------------------------------------
    # Divide matrices
    # --------------------------------------------------------

    A11 = [row[:mid] for row in padded_A[:mid]]
    A12 = [row[mid:] for row in padded_A[:mid]]
    A21 = [row[:mid] for row in padded_A[mid:]]
    A22 = [row[mid:] for row in padded_A[mid:]]

    B11 = [row[:mid] for row in padded_B[:mid]]
    B12 = [row[mid:] for row in padded_B[:mid]]
    B21 = [row[:mid] for row in padded_B[mid:]]
    B22 = [row[mid:] for row in padded_B[mid:]]

    # --------------------------------------------------------
    # Seven IMPORTANT top-level Strassen calculations
    #
    # Each M is calculated recursively.
    # We display these top-level intermediate results.
    # --------------------------------------------------------

    M1 = strassen_recursive(
        add_matrix(A11, A22),
        add_matrix(B11, B22)
    )

    M2 = strassen_recursive(
        add_matrix(A21, A22),
        B11
    )

    M3 = strassen_recursive(
        A11,
        subtract_matrix(B12, B22)
    )

    M4 = strassen_recursive(
        A22,
        subtract_matrix(B21, B11)
    )

    M5 = strassen_recursive(
        add_matrix(A11, A12),
        B22
    )

    M6 = strassen_recursive(
        subtract_matrix(A21, A11),
        add_matrix(B11, B12)
    )

    M7 = strassen_recursive(
        subtract_matrix(A12, A22),
        add_matrix(B21, B22)
    )

    # --------------------------------------------------------
    # Final quadrants
    # --------------------------------------------------------

    C11 = add_matrix(
        subtract_matrix(
            add_matrix(M1, M4),
            M5
        ),
        M7
    )

    C12 = add_matrix(M3, M5)

    C21 = add_matrix(M2, M4)

    C22 = add_matrix(
        subtract_matrix(
            add_matrix(M1, M3),
            M2
        ),
        M6
    )

    # --------------------------------------------------------
    # Final padded result
    # --------------------------------------------------------

    result = []

    for i in range(mid):
        result.append(C11[i] + C12[i])

    for i in range(mid):
        result.append(C21[i] + C22[i])

    # Remove padding
    final_result = [
        row[:original_size]
        for row in result[:original_size]
    ]

    # --------------------------------------------------------
    # Save important intermediate information
    # --------------------------------------------------------

    steps = {

        "size": size,

        "padded_A": padded_A,

        "padded_B": padded_B,

        "A11": A11,
        "A12": A12,
        "A21": A21,
        "A22": A22,

        "B11": B11,
        "B12": B12,
        "B21": B21,
        "B22": B22,

        "M1": M1,
        "M2": M2,
        "M3": M3,
        "M4": M4,
        "M5": M5,
        "M6": M6,
        "M7": M7,

        "C11": C11,
        "C12": C12,
        "C21": C21,
        "C22": C22
    }

    return final_result, steps


# ============================================================
# GUI
# ============================================================

class StrassenGUI(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title(
            "Strassen Matrix Multiplication"
        )

        self.geometry("1250x820")

        self.minsize(
            1050,
            700
        )

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(
            fg_color="#0f172a"
        )

        self.matrix_size = 3

        self.entries_A = []
        self.entries_B = []

        self.result_cells = []

        self.current_steps = None

        self.create_layout()

        self.create_matrix_inputs()

        self.create_result_area()


    # ========================================================
    # MAIN LAYOUT
    # ========================================================

    def create_layout(self):

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#111827",
            height=100
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="STRASSEN MATRIX MULTIPLICATION",
            font=ctk.CTkFont(
                family="Arial",
                size=28,
                weight="bold"
            ),
            text_color="#60a5fa"
        )

        title.pack(
            pady=(20, 2)
        )

        subtitle = ctk.CTkLabel(
            header,
            text=(
                "Fast Matrix Multiplication using "
                "the Strassen Algorithm"
            ),
            font=ctk.CTkFont(
                size=14
            ),
            text_color="#94a3b8"
        )

        subtitle.pack()

        # ----------------------------------------------------
        # CONTROL BAR
        # ----------------------------------------------------

        control = ctk.CTkFrame(
            self,
            fg_color="#1e293b",
            corner_radius=15,
            height=75
        )

        control.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        size_label = ctk.CTkLabel(
            control,
            text="Matrix Size:",
            font=ctk.CTkFont(
                size=15,
                weight="bold"
            )
        )

        size_label.pack(
            side="left",
            padx=(20, 10)
        )

        self.size_combo = ctk.CTkComboBox(
            control,
            values=[
                "2 x 2",
                "3 x 3",
                "4 x 4",
                "5 x 5",
                "6 x 6",
                "7 x 7",
                "8 x 8"
            ],
            width=120,
            height=35,
            command=self.change_size
        )

        self.size_combo.set(
            "3 x 3"
        )

        self.size_combo.pack(
            side="left",
            padx=5
        )

        generate_btn = ctk.CTkButton(
            control,
            text="Generate Matrices",
            width=160,
            height=35,
            corner_radius=8,
            command=self.generate_matrices
        )

        generate_btn.pack(
            side="left",
            padx=10
        )

        calculate_btn = ctk.CTkButton(
            control,
            text="CALCULATE RESULT",
            width=190,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            ),
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.calculate
        )

        calculate_btn.pack(
            side="right",
            padx=10
        )

        clear_btn = ctk.CTkButton(
            control,
            text="Clear",
            width=80,
            height=35,
            corner_radius=8,
            fg_color="#475569",
            hover_color="#334155",
            command=self.clear_all
        )

        clear_btn.pack(
            side="right",
            padx=5
        )

        # ----------------------------------------------------
        # CONTENT
        # ----------------------------------------------------

        self.content = ctk.CTkScrollableFrame(
            self,
            fg_color="#0f172a",
            corner_radius=0
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )


    # ========================================================
    # MATRIX INPUT AREA
    # ========================================================

    def create_matrix_inputs(self):

        self.input_frame = ctk.CTkFrame(
            self.content,
            fg_color="#111827",
            corner_radius=15
        )

        self.input_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # ----------------------------------------------------
        # MATRIX A
        # ----------------------------------------------------

        self.matrix_A_frame = ctk.CTkFrame(
            self.input_frame,
            fg_color="#1e293b",
            corner_radius=12
        )

        self.matrix_A_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 8),
            pady=15
        )

        label_A = ctk.CTkLabel(
            self.matrix_A_frame,
            text="MATRIX A",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            ),
            text_color="#60a5fa"
        )

        label_A.pack(
            pady=(15, 5)
        )

        # ----------------------------------------------------
        # MATRIX B
        # ----------------------------------------------------

        self.matrix_B_frame = ctk.CTkFrame(
            self.input_frame,
            fg_color="#1e293b",
            corner_radius=12
        )

        self.matrix_B_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(8, 15),
            pady=15
        )

        label_B = ctk.CTkLabel(
            self.matrix_B_frame,
            text="MATRIX B",
            font=ctk.CTkFont(
                size=19,
                weight="bold"
            ),
            text_color="#34d399"
        )

        label_B.pack(
            pady=(15, 5)
        )

        self.create_input_grids()


    # ========================================================
    # INPUT GRIDS
    # ========================================================

    def create_input_grids(self):

        # Remove old widgets except title
        for widget in self.matrix_A_frame.winfo_children()[1:]:
            widget.destroy()

        for widget in self.matrix_B_frame.winfo_children()[1:]:
            widget.destroy()

        self.entries_A = []
        self.entries_B = []

        grid_A = ctk.CTkFrame(
            self.matrix_A_frame,
            fg_color="transparent"
        )

        grid_A.pack(
            pady=10
        )

        grid_B = ctk.CTkFrame(
            self.matrix_B_frame,
            fg_color="transparent"
        )

        grid_B.pack(
            pady=10
        )

        for i in range(self.matrix_size):

            row_A = []
            row_B = []

            for j in range(self.matrix_size):

                entry_A = ctk.CTkEntry(
                    grid_A,
                    width=60,
                    height=45,
                    justify="center",
                    font=ctk.CTkFont(
                        size=16,
                        weight="bold"
                    ),
                    corner_radius=6,
                    border_width=1,
                    border_color="#3b82f6"
                )

                entry_A.grid(
                    row=i,
                    column=j,
                    padx=4,
                    pady=4
                )

                entry_B = ctk.CTkEntry(
                    grid_B,
                    width=60,
                    height=45,
                    justify="center",
                    font=ctk.CTkFont(
                        size=16,
                        weight="bold"
                    ),
                    corner_radius=6,
                    border_width=1,
                    border_color="#10b981"
                )

                entry_B.grid(
                    row=i,
                    column=j,
                    padx=4,
                    pady=4
                )

                row_A.append(entry_A)
                row_B.append(entry_B)

            self.entries_A.append(row_A)
            self.entries_B.append(row_B)


    # ========================================================
    # RESULT AREA
    # ========================================================

    def create_result_area(self):

        self.result_frame = ctk.CTkFrame(
            self.content,
            fg_color="#111827",
            corner_radius=15
        )

        self.result_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        title = ctk.CTkLabel(
            self.result_frame,
            text="RESULT MATRIX",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            ),
            text_color="#fbbf24"
        )

        title.pack(
            pady=(15, 5)
        )

        self.result_grid = ctk.CTkFrame(
            self.result_frame,
            fg_color="#1e293b",
            corner_radius=10
        )

        self.result_grid.pack(
            pady=10,
            padx=20
        )

        self.result_placeholder = ctk.CTkLabel(
            self.result_grid,
            text=(
                "Click 'CALCULATE RESULT' "
                "to display the result"
            ),
            font=ctk.CTkFont(
                size=14
            ),
            text_color="#64748b"
        )

        self.result_placeholder.pack(
            padx=50,
            pady=30
        )

        # ----------------------------------------------------
        # ALGORITHM STEPS BUTTON
        # ----------------------------------------------------

        self.steps_button = ctk.CTkButton(
            self.result_frame,
            text="VIEW STRASSEN INTERMEDIATE STEPS",
            width=280,
            height=38,
            corner_radius=8,
            fg_color="#7c3aed",
            hover_color="#6d28d9",
            font=ctk.CTkFont(
                size=13,
                weight="bold"
            ),
            command=self.show_steps
        )

        self.steps_button.pack(
            pady=(5, 10)
        )

        # ----------------------------------------------------
        # PERFORMANCE
        # ----------------------------------------------------

        self.performance_frame = ctk.CTkFrame(
            self.result_frame,
            fg_color="#172033",
            corner_radius=10
        )

        self.performance_frame.pack(
            fill="x",
            padx=20,
            pady=(5, 15)
        )

        self.performance_label = ctk.CTkLabel(
            self.performance_frame,
            text=(
                "Performance information "
                "will appear here."
            ),
            font=ctk.CTkFont(
                size=14
            ),
            text_color="#cbd5e1"
        )

        self.performance_label.pack(
            pady=12
        )


    # ========================================================
    # CHANGE SIZE
    # ========================================================

    def change_size(self, value):

        self.matrix_size = int(
            value.split()[0]
        )

        self.create_input_grids()

        self.clear_result()


    # ========================================================
    # GENERATE RANDOM MATRICES
    # ========================================================

    def generate_matrices(self):

        import random

        for i in range(self.matrix_size):

            for j in range(self.matrix_size):

                self.entries_A[i][j].delete(
                    0,
                    "end"
                )

                self.entries_A[i][j].insert(
                    0,
                    str(random.randint(1, 9))
                )

                self.entries_B[i][j].delete(
                    0,
                    "end"
                )

                self.entries_B[i][j].insert(
                    0,
                    str(random.randint(1, 9))
                )

        self.clear_result()


    # ========================================================
    # READ MATRIX
    # ========================================================

    def get_matrix(self, entries):

        matrix = []

        try:

            for row in entries:

                matrix_row = []

                for entry in row:

                    value = entry.get().strip()

                    if value == "":
                        raise ValueError

                    matrix_row.append(
                        int(value)
                    )

                matrix.append(
                    matrix_row
                )

            return matrix

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                (
                    "Please enter valid integer "
                    "values in all matrix cells."
                )
            )

            return None


    # ========================================================
    # CALCULATE
    # ========================================================

    def calculate(self):

        A = self.get_matrix(
            self.entries_A
        )

        B = self.get_matrix(
            self.entries_B
        )

        if A is None or B is None:
            return

        # ----------------------------------------------------
        # Normal multiplication
        # ----------------------------------------------------

        start_normal = time.perf_counter()

        normal_result = normal_multiply(
            A,
            B
        )

        normal_time = (
            time.perf_counter()
            - start_normal
        )

        # ----------------------------------------------------
        # Strassen
        # ----------------------------------------------------

        start_strassen = time.perf_counter()

        strassen_result, steps = strassen_with_steps(
            A,
            B
        )

        strassen_time = (
            time.perf_counter()
            - start_strassen
        )

        self.current_steps = steps

        # ----------------------------------------------------
        # Verify result
        # ----------------------------------------------------

        if normal_result != strassen_result:

            messagebox.showerror(
                "Calculation Error",
                (
                    "Strassen result does not match "
                    "normal multiplication."
                )
            )

            return

        # ----------------------------------------------------
        # Display
        # ----------------------------------------------------

        self.display_result(
            strassen_result
        )

        self.performance_label.configure(
            text=(
                f"Normal Multiplication: "
                f"{normal_time:.8f} seconds     "
                f"│     "
                f"Strassen Algorithm: "
                f"{strassen_time:.8f} seconds     "
                f"│     "
                f"Result Verified ✓"
            ),
            text_color="#34d399"
        )


    # ========================================================
    # DISPLAY RESULT
    # ========================================================

    def display_result(self, result):

        for widget in self.result_grid.winfo_children():
            widget.destroy()

        self.result_cells = []

        for i in range(len(result)):

            row_cells = []

            for j in range(len(result)):

                cell = ctk.CTkLabel(
                    self.result_grid,
                    text=str(result[i][j]),
                    width=70,
                    height=50,
                    fg_color="#334155",
                    corner_radius=5,
                    font=ctk.CTkFont(
                        size=17,
                        weight="bold"
                    ),
                    text_color="#f8fafc"
                )

                cell.grid(
                    row=i,
                    column=j,
                    padx=4,
                    pady=4
                )

                row_cells.append(
                    cell
                )

            self.result_cells.append(
                row_cells
            )


    # ========================================================
    # MATRIX TO TEXT
    # ========================================================

    def matrix_to_text(self, matrix):

        lines = []

        for row in matrix:

            line = "   ".join(
                f"{value:>6}"
                for value in row
            )

            lines.append(
                line
            )

        return "\n".join(lines)


    # ========================================================
    # SHOW STRASSEN STEPS
    # ========================================================

    def show_steps(self):

        if self.current_steps is None:

            messagebox.showinfo(
                "No Calculation",
                (
                    "Please calculate the result "
                    "first."
                )
            )

            return

        steps = self.current_steps

        # ----------------------------------------------------
        # New window
        # ----------------------------------------------------

        step_window = ctk.CTkToplevel(
            self
        )

        step_window.title(
            "Strassen Intermediate Steps"
        )

        step_window.geometry(
            "1000x750"
        )

        step_window.minsize(
            850,
            650
        )

        step_window.configure(
            fg_color="#0f172a"
        )

        # ----------------------------------------------------
        # Header
        # ----------------------------------------------------

        header = ctk.CTkFrame(
            step_window,
            fg_color="#111827",
            corner_radius=0,
            height=80
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = ctk.CTkLabel(
            header,
            text="STRASSEN INTERMEDIATE CALCULATIONS",
            font=ctk.CTkFont(
                size=23,
                weight="bold"
            ),
            text_color="#a78bfa"
        )

        title.pack(
            pady=(15, 2)
        )

        subtitle = ctk.CTkLabel(
            header,
            text=(
                "Important intermediate M1–M7 calculations "
                "used by the Strassen algorithm"
            ),
            font=ctk.CTkFont(
                size=13
            ),
            text_color="#94a3b8"
        )

        subtitle.pack()

        # ----------------------------------------------------
        # Scrollable area
        # ----------------------------------------------------

        scroll = ctk.CTkScrollableFrame(
            step_window,
            fg_color="#0f172a"
        )

        scroll.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # ----------------------------------------------------
        # Padding information
        # ----------------------------------------------------

        info_frame = ctk.CTkFrame(
            scroll,
            fg_color="#1e293b",
            corner_radius=12
        )

        info_frame.pack(
            fill="x",
            padx=5,
            pady=5
        )

        if steps["size"] != self.matrix_size:

            info_text = (
                f"Input size: {self.matrix_size} × "
                f"{self.matrix_size}\n"
                f"Strassen works with powers of 2, so the "
                f"matrices were padded to "
                f"{steps['size']} × {steps['size']} "
                f"using zeros."
            )

        else:

            info_text = (
                f"Matrix size: {steps['size']} × "
                f"{steps['size']}\n"
                f"No padding was required."
            )

        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(
                size=14
            ),
            text_color="#cbd5e1",
            justify="left"
        )

        info_label.pack(
            anchor="w",
            padx=20,
            pady=15
        )

        # ----------------------------------------------------
        # Formula information
        # ----------------------------------------------------

        formula_frame = ctk.CTkFrame(
            scroll,
            fg_color="#111827",
            corner_radius=12
        )

        formula_frame.pack(
            fill="x",
            padx=5,
            pady=8
        )

        formula_title = ctk.CTkLabel(
            formula_frame,
            text="Seven Strassen Products",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#60a5fa"
        )

        formula_title.pack(
            anchor="w",
            padx=20,
            pady=(15, 8)
        )

        formulas = [
            "M1 = (A11 + A22) × (B11 + B22)",
            "M2 = (A21 + A22) × B11",
            "M3 = A11 × (B12 − B22)",
            "M4 = A22 × (B21 − B11)",
            "M5 = (A11 + A12) × B22",
            "M6 = (A21 − A11) × (B11 + B12)",
            "M7 = (A12 − A22) × (B21 + B22)"
        ]

        for formula in formulas:

            label = ctk.CTkLabel(
                formula_frame,
                text=formula,
                font=ctk.CTkFont(
                    size=14
                ),
                text_color="#cbd5e1",
                anchor="w"
            )

            label.pack(
                anchor="w",
                padx=25,
                pady=2
            )

        # ----------------------------------------------------
        # M1-M7 results
        # ----------------------------------------------------

        m_frame = ctk.CTkFrame(
            scroll,
            fg_color="#111827",
            corner_radius=12
        )

        m_frame.pack(
            fill="x",
            padx=5,
            pady=8
        )

        m_title = ctk.CTkLabel(
            m_frame,
            text="Intermediate Matrix Results",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#34d399"
        )

        m_title.pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        for name in [
            "M1",
            "M2",
            "M3",
            "M4",
            "M5",
            "M6",
            "M7"
        ]:

            card = ctk.CTkFrame(
                m_frame,
                fg_color="#1e293b",
                corner_radius=8
            )

            card.pack(
                fill="x",
                padx=20,
                pady=5
            )

            value = self.matrix_to_text(
                steps[name]
            )

            text = (
                f"{name}\n"
                f"{value}"
            )

            label = ctk.CTkLabel(
                card,
                text=text,
                font=ctk.CTkFont(
                    family="Consolas",
                    size=14
                ),
                text_color="#e2e8f0",
                justify="left"
            )

            label.pack(
                anchor="w",
                padx=15,
                pady=10
            )

        # ----------------------------------------------------
        # Final quadrant calculation
        # ----------------------------------------------------

        quadrant_frame = ctk.CTkFrame(
            scroll,
            fg_color="#111827",
            corner_radius=12
        )

        quadrant_frame.pack(
            fill="x",
            padx=5,
            pady=8
        )

        q_title = ctk.CTkLabel(
            quadrant_frame,
            text="Final Matrix Quadrants",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            ),
            text_color="#fbbf24"
        )

        q_title.pack(
            anchor="w",
            padx=20,
            pady=(15, 10)
        )

        quadrant_formulas = [
            "C11 = M1 + M4 − M5 + M7",
            "C12 = M3 + M5",
            "C21 = M2 + M4",
            "C22 = M1 + M3 − M2 + M6"
        ]

        for formula in quadrant_formulas:

            label = ctk.CTkLabel(
                quadrant_frame,
                text=formula,
                font=ctk.CTkFont(
                    size=14,
                    weight="bold"
                ),
                text_color="#cbd5e1"
            )

            label.pack(
                anchor="w",
                padx=25,
                pady=3
            )

        # ----------------------------------------------------
        # Actual C quadrant values
        # ----------------------------------------------------

        c_values = [
            ("C11", steps["C11"]),
            ("C12", steps["C12"]),
            ("C21", steps["C21"]),
            ("C22", steps["C22"])
        ]

        for name, matrix in c_values:

            card = ctk.CTkFrame(
                quadrant_frame,
                fg_color="#1e293b",
                corner_radius=8
            )

            card.pack(
                fill="x",
                padx=20,
                pady=4
            )

            text = (
                f"{name}\n"
                f"{self.matrix_to_text(matrix)}"
            )

            label = ctk.CTkLabel(
                card,
                text=text,
                font=ctk.CTkFont(
                    family="Consolas",
                    size=14
                ),
                text_color="#e2e8f0",
                justify="left"
            )

            label.pack(
                anchor="w",
                padx=15,
                pady=8
            )

        # ----------------------------------------------------
        # Close button
        # ----------------------------------------------------

        close_btn = ctk.CTkButton(
            step_window,
            text="CLOSE",
            width=120,
            height=35,
            corner_radius=8,
            command=step_window.destroy
        )

        close_btn.pack(
            pady=(0, 15)
        )


    # ========================================================
    # CLEAR RESULT
    # ========================================================

    def clear_result(self):

        self.current_steps = None

        for widget in self.result_grid.winfo_children():
            widget.destroy()

        self.result_placeholder = ctk.CTkLabel(
            self.result_grid,
            text=(
                "Click 'CALCULATE RESULT' "
                "to display the result"
            ),
            font=ctk.CTkFont(
                size=14
            ),
            text_color="#64748b"
        )

        self.result_placeholder.pack(
            padx=50,
            pady=30
        )

        self.performance_label.configure(
            text=(
                "Performance information "
                "will appear here."
            ),
            text_color="#cbd5e1"
        )


    # ========================================================
    # CLEAR EVERYTHING
    # ========================================================

    def clear_all(self):

        for row in self.entries_A:

            for entry in row:

                entry.delete(
                    0,
                    "end"
                )

        for row in self.entries_B:

            for entry in row:

                entry.delete(
                    0,
                    "end"
                )

        self.clear_result()


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    app = StrassenGUI()

    app.mainloop()