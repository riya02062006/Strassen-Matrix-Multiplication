# Strassen Matrix Multiplication

A Python-based GUI implementation of the **Strassen Matrix Multiplication Algorithm** using **CustomTkinter**.

This project demonstrates how Strassen's algorithm reduces the number of recursive matrix multiplications from 8 to 7, while providing a visual representation of the calculations.

## Features

- Modern graphical user interface using CustomTkinter
- Supports different matrix sizes
- Matrix A and Matrix B input through GUI
- Normal matrix multiplication
- Strassen matrix multiplication
- Automatic padding for non-power-of-two matrix sizes
- Displays the final result as a matrix grid
- Displays important intermediate calculations M1–M7
- Displays C11, C12, C21 and C22 calculations
- Performance comparison between normal multiplication and Strassen multiplication
- Automatic verification of the results

## Technologies Used

- Python
- CustomTkinter
- Tkinter
- Strassen Matrix Multiplication Algorithm

## Strassen Algorithm

For two matrices divided into four submatrices:

```text
A = | A11  A12 |       B = | B11  B12 |
    | A21  A22 |           | B21  B22 |
