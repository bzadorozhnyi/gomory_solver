from fractions import Fraction

from openpyxl import Workbook

import negative_deltas_case as negative_deltas_case
import negative_P0_case as negative_P0_case
import sheet as sheet
from canonical_form import canonical_form
from simplex_number import *

NUMBER_OF_ADDITIONAL_COLS = 3
NUMBER_OF_ADDITIONAL_ROWS = 1


def to_simplex_number(x):
    if x == '-M':
        return SimplexNumber(0, -1)
    return SimplexNumber(x)


def list_to_simplex_number(a):
    return [to_simplex_number(i) for i in a]


def list_to_fractions(a):
    return [Fraction(i) for i in a]


def matrix_to_fractions(matrix):
    return [list_to_fractions(row) for row in matrix]


def get_deltas(basic_indeces, f_coefficients, coefficients):
    deltas = []
    for col in range(len(f_coefficients)):
        delta = SimplexNumber(0)
        for row, basic_index in enumerate(basic_indeces):
            delta += f_coefficients[basic_index] * coefficients[row][col]
        deltas.append(delta - f_coefficients[col])

    return deltas


def F(ratio):
    if type(ratio) == SimplexNumber:
        numerator, denominator = ratio.real.numerator, ratio.real.denominator
    else:
        numerator, denominator = ratio.numerator, ratio.denominator
    return Fraction(numerator % denominator, denominator)


def find_new_constraint_index(P0):
    index, rows = 0, len(P0)
    ratio = F(P0[0])

    for row in range(rows):
        row_ratio = F(P0[row])
        if ratio < row_ratio:
            index, ratio = row, row_ratio

    return index


def create_new_constraint(P0, coefficients):
    new_constraint_index = find_new_constraint_index(P0)
    constraint = list(map(F, coefficients[new_constraint_index]))
    constraint.append(Fraction(-1))

    constraint = [-c for c in constraint]

    new_P0_element = -F(P0[new_constraint_index])

    return new_P0_element, constraint


def add_new_constraint(basic_indeces, P0, coefficients, f_coefficients, new_P0_element, constraint):
    basic_indeces.append(len(coefficients[0]))
    P0.append(new_P0_element)

    for c in coefficients:
        c.append(Fraction(0))

    coefficients.append(constraint)

    f_coefficients.append(Fraction(0))


def calc_f(basic_indeces, f_coefficients, P0):
    return sum(f_coefficients[basic_indeces[i]] * P0[i] for i in range(len(basic_indeces)))


def get_optimal_plan(basic_indeces, P0):
    x = [0 for i in range(max(basic_indeces) + 1)]
    for index, frac in zip(basic_indeces, P0):
        x[index] = frac.real.numerator
    return x


def print_step(ws, basic_indeces, P0, f_coefficients, coefficients):
    global table_row, table_col

    number_of_rows = len(basic_indeces)
    number_of_variables = len(coefficients[0])

    deltas = get_deltas(basic_indeces, f_coefficients, coefficients)
    sheet.append_row(ws, (table_row, table_col), [
                     'Б', 'С', 'P0'] + ['P'+str(i) for i in range(1, number_of_variables + 1)])
    table_row += 1

    for row in range(number_of_rows):
        sheet.append_row(ws, (table_row, table_col), [
                         f'P{basic_indeces[row] + 1}',  f_coefficients[basic_indeces[row]], P0[row]] + coefficients[row])
        table_row += 1

    sheet.append_row(ws, (table_row, table_col), [' ', ' ', str(
        calc_f(basic_indeces, f_coefficients, P0))] + deltas)
    table_row += 3


table_row, table_col = 2, 2


def main(objective_function, constraints):
    wb = Workbook()
    ws = wb.active
    f_coefficients, max_or_min, coefficients, P0, basic_indeces = canonical_form(
        objective_function, constraints)

    f_coefficients = list_to_simplex_number(f_coefficients)
    coefficients = matrix_to_fractions(coefficients)
    P0 = list_to_simplex_number(P0)

    global table_row, table_col

    is_valid_step = True
    step = 1
    while is_valid_step:
        while True:
            deltas = get_deltas(basic_indeces, f_coefficients, coefficients)

            sheet.append_row(ws, (table_row, table_col), ['STEP', step])
            table_row += 1

            print_step(ws, basic_indeces, P0, f_coefficients, coefficients)
            step += 1

            if min(deltas) < 0:
                leading_column = negative_deltas_case.get_leading_column(
                    deltas, coefficients, f_coefficients)

                if leading_column == None:
                    is_valid_step = False
                    break

                leading_row = negative_deltas_case.get_leading_row(
                    P0, coefficients, leading_column)

                sheet.colorize_table(ws, coefficients, leading_row, leading_column, table_row, table_col, NUMBER_OF_ADDITIONAL_ROWS, NUMBER_OF_ADDITIONAL_COLS)

                basic_indeces, P0, coefficients = negative_deltas_case.update_data(
                    basic_indeces, P0, coefficients, leading_row, leading_column)
            elif min(P0) < 0:
                leading_row = negative_P0_case.get_leading_row(P0)
                leading_column = negative_P0_case.get_leading_column(
                    deltas, coefficients, leading_row)

                sheet.colorize_table(ws, coefficients, leading_row, leading_column, table_row, table_col, NUMBER_OF_ADDITIONAL_ROWS, NUMBER_OF_ADDITIONAL_COLS)

                basic_indeces, P0, coefficients = negative_P0_case.update_data(
                    basic_indeces, P0, coefficients, leading_row, leading_column)
            else:
                break

        if any(p.real.denominator != 1 for p in P0):
            new_P0_element, constraint = create_new_constraint(
                P0, coefficients)
            add_new_constraint(basic_indeces, P0, coefficients,
                               f_coefficients, new_P0_element, constraint)
            is_valid_step = True
        else:
            break

    print('TOTAL NUMBER OF STEPS:', step - 1)

    if max_or_min == 'max':
        print(f'F_max={calc_f(basic_indeces, f_coefficients, P0)}')
    else:
        print(f'F_min={calc_f(basic_indeces, [-element for element in f_coefficients], P0)}')

    optimal_X_str = ', '.join(str(x)
                              for x in get_optimal_plan(basic_indeces, P0))
    print(f'X*=({optimal_X_str})')

    wb.save("gomory.xlsx")


objective_function = input('Objective function: ')
number_of_constraints = int(input('Number of constraints: '))
constraints = []
for _ in range(number_of_constraints):
    constraints.append(input())

main(objective_function, constraints)
