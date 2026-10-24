
import streamlit as st
import time

st.set_page_config(
    page_title="Strassen Matrix Multiplier",
    page_icon="🔢",
    layout="wide"
)

st.title("Strassen Matrix Multiplication")
st.caption("An interactive visualizer for Divide and Conquer matrix multiplication.")

st.markdown("""
This application compares conventional matrix multiplication with
Strassen's algorithm and displays the seven intermediate products.
""")

def add(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)]
            for i in range(n)]

def sub(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)]
            for i in range(n)]

def split(A):
    n = len(A)
    mid = n // 2
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]
    return A11, A12, A21, A22

def join(C11, C12, C21, C22):
    top = [C11[i] + C12[i] for i in range(len(C11))]
    bottom = [C21[i] + C22[i] for i in range(len(C21))]
    return top + bottom

def strassen(A, B, trace=None, depth=0):
    n = len(A)

    if n == 1:
        return [[A[0][0] * B[0][0]]]

    A11, A12, A21, A22 = split(A)
    B11, B12, B21, B22 = split(B)

    # Seven products used by Strassen's algorithm
    M1 = strassen(add(A11, A22), add(B11, B22))
    M2 = strassen(add(A21, A22), B11)
    M3 = strassen(A11, sub(B12, B22))
    M4 = strassen(A22, sub(B21, B11))
    M5 = strassen(add(A11, A12), B22)
    M6 = strassen(sub(A21, A11), add(B11, B12))
    M7 = strassen(sub(A12, A22), add(B21, B22))

    if trace is not None and depth == 0:
        trace.update({
            "M1": M1, "M2": M2, "M3": M3,
            "M4": M4, "M5": M5, "M6": M6, "M7": M7
        })

    C11 = add(sub(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(add(sub(M1, M2), M3), M6)

    return join(C11, C12, C21, C22)

def normal_multiply(A, B):
    n = len(A)
    return [
        [
            sum(A[i][k] * B[k][j] for k in range(n))
            for j in range(n)
        ]
        for i in range(n)
    ]

def pad_matrix(A, size):
    n = len(A)
    return [
        row + [0] * (size - n) for row in A
    ] + [
        [0] * size for _ in range(size - n)
    ]

def next_power_of_two(n):
    size = 1
    while size < n:
        size *= 2
    return size

st.subheader("1. Enter your matrices")

n = st.select_slider(
    "Matrix order (n × n)",
    options=list(range(2, 9)),
    value=2
)

with st.form("matrix_form"):
    left, right = st.columns(2)
    A = []
    B = []

    with left:
        st.markdown("#### Matrix A")
        for i in range(n):
            cols = st.columns(n)
            row = []
            for j in range(n):
                row.append(
                    cols[j].number_input(
                        f"A[{i+1},{j+1}]",
                        value=1 if i == j else 0,
                        step=1,
                        key=f"a_{n}_{i}_{j}"
                    )
                )
            A.append(row)

    with right:
        st.markdown("#### Matrix B")
        for i in range(n):
            cols = st.columns(n)
            row = []
            for j in range(n):
                row.append(
                    cols[j].number_input(
                        f"B[{i+1},{j+1}]",
                        value=1 if i == j else 0,
                        step=1,
                        key=f"b_{n}_{i}_{j}"
                    )
                )
            B.append(row)

    run = st.form_submit_button(
        "Calculate Matrices",
        type="primary",
        use_container_width=True
    )

if run:
    A = [[int(x) for x in row] for row in A]
    B = [[int(x) for x in row] for row in B]

    st.subheader("2. Input matrices")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("Matrix A")
        st.table(A)
    with col_b:
        st.write("Matrix B")
        st.table(B)

    # Conventional multiplication
    start = time.perf_counter()
    normal_result = normal_multiply(A, B)
    normal_time = time.perf_counter() - start

    # Pad matrices to a power-of-two order for Strassen
    size = next_power_of_two(n)
    A_pad = pad_matrix(A, size)
    B_pad = pad_matrix(B, size)

    trace = {}
    start = time.perf_counter()
    full_result = strassen(A_pad, B_pad, trace)
    strassen_time = time.perf_counter() - start

    # Remove any extra padded rows and columns
    result = [row[:n] for row in full_result[:n]]

    st.subheader("3. Result matrix")
    st.table(result)

    st.subheader("4. Algorithm comparison")
    c1, c2, c3 = st.columns(3)
    c1.metric("Normal multiplication", f"{normal_time * 1000:.4f} ms")
    c2.metric("Strassen multiplication", f"{strassen_time * 1000:.4f} ms")
    c3.metric("Results match", "Yes" if result == normal_result else "No")

    st.caption(
        "Timings for small matrices are highly affected by Python overhead. "
        "They are not a reliable benchmark of algorithm performance."
    )

    st.subheader("5. Strassen's seven intermediate products")
    st.write(
        "These are the seven products from the top-level recursive step. "
        "For larger matrices, each product is itself calculated recursively."
    )

    for name, matrix in trace.items():
        with st.expander(f"{name} — Intermediate matrix"):
            st.table(matrix)

    st.success("Calculation completed successfully!")
