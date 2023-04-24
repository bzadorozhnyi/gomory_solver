from fractions import Fraction

def get_leading_row(P0):
    leading_row, rows = 0, len(P0)
    for row in range(rows):
        if P0[leading_row] > P0[row]:
            leading_row = row

    if P0[leading_row] > 0:
        return None
    return leading_row


def get_leading_column(deltas, coefficients, leading_row):
    leading_column, cols = -1, len(coefficients[0])

    for col in range(cols):
        if coefficients[leading_row][col] < 0:
            leading_column = col
            break

    if leading_column == -1:
        return None

    ratio = -deltas[col] / coefficients[leading_row][col]
    for col in range(cols):
        if coefficients[leading_row][col] < 0:
            current_ratio = -deltas[col] / coefficients[leading_row][col]
            if ratio > current_ratio:
                leading_column, ratio = col, current_ratio

    return leading_column


def update_data(basic_indeces, P0, coefficients, leading_row, leading_column):
    basic_indeces[leading_row] = leading_column

    key_element = coefficients[leading_row][leading_column]

    rows, cols = len(coefficients), len(coefficients[0])
    new_coefficients = [[Fraction(0) for col in range(cols)]
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
