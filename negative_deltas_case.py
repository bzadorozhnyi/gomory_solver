from fractions import Fraction

from simplex_number import SimplexNumber


def get_leading_column(deltas, coefficients, f_coefficients):
    min_delta = min(deltas)
    if min_delta >= 0:
        return None

    min_deltas_indeces = []
    for col in range(len(deltas)):
        if deltas[col] == min_delta:
            if any([coefficients[row][col] > 0 for row in range(len(coefficients))]):
                min_deltas_indeces.append(col)

    if len(min_deltas_indeces) == 0:
        return None

    leading_column = min_deltas_indeces[0]
    for index in min_deltas_indeces:
        if f_coefficients[index] > f_coefficients[leading_column]:
            leading_column = index

    return leading_column


def get_leading_row(P0, coefficients, leading_column):
    leading_row, rows = -1, len(P0)

    for row in range(rows):
        if coefficients[row][leading_column] > 0:
            leading_row = row
            break

    if leading_row == -1:
        return None

    leading_ratio = P0[leading_row] / coefficients[leading_row][leading_column]
    for row in range(rows):
        if coefficients[row][leading_column] > 0:
            if leading_ratio > P0[row] / coefficients[row][leading_column]:
                leading_row = row

    return leading_row


def update_data(basic_indeces, P0, coefficients, leading_row, leading_column):
    key_element = Fraction(coefficients[leading_row][leading_column].real)

    basic_indeces[leading_row] = leading_column

    rows, cols = len(coefficients), len(coefficients[0])
    new_coefficients = [[SimplexNumber(0) for col in range(cols)]
                        for row in range(rows)]

    P0[leading_row] /= key_element
    for col in range(cols):
        new_coefficients[leading_row][col] = coefficients[leading_row][col] / key_element

    for row in range(rows):
        if row == leading_row:
            continue

        P0[row] -= P0[leading_row] * coefficients[row][leading_column]
        for col in range(cols):
            new_coefficients[row][col] = coefficients[row][col] - \
                coefficients[row][leading_column] * \
                new_coefficients[leading_row][col]

    return basic_indeces, P0, new_coefficients
