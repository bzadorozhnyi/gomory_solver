import re

def get_coefficient(objective_function: str):
    pattern = r'([+-]?\s*\d*)\s*(x\d+)'
    matches = re.findall(pattern, objective_function)

    coefficients = {}
    for match in matches:
        coefficient, variable = match

        coefficient = coefficient.replace(' ', '')

        if coefficient == '+' or coefficient == '':
            coefficients[variable] = 1
        elif coefficient == '-':
            coefficients[variable] = -1
        else:
            coefficients[variable] = int(coefficient)

    number_of_variables = max([int(variable[1:])
                              for variable in coefficients.keys()])

    list_of_coefficients = []
    for i in range(1, number_of_variables + 1):
        variable = f'x{i}'

        list_of_coefficients.append(
            coefficients[variable] if variable in coefficients else 0)

    return list_of_coefficients


def parse_comparison_string(s):
    lt_index = s.find("<=")
    gt_index = s.find(">=")
    eq_index = s.find("=")

    if lt_index != -1:
        comparison_type = "<="
        number_index = lt_index + 2
    elif gt_index != -1:
        comparison_type = ">="
        number_index = gt_index + 2
    elif eq_index != -1:
        comparison_type = "="
        number_index = eq_index + 1
    else:
        raise ValueError("The string does not contain valid comparison characters.")

    number = float(s[number_index:])
    return comparison_type, number


def add_column_to_matrix(matrix):
    for row in matrix:
        row += [0]


def list_to_size(a: list[int], size: int):
    a += [0] * (size - len(a))


def matrix_rows_to_same_size(objective_function: list[int], coefficients: list[int]):
    max_size = max(len(objective_function), max([len(coefficient)
                   for coefficient in coefficients]))

    list_to_size(objective_function, max_size)
    for coefficient in coefficients:
        list_to_size(coefficient, max_size)


def is_unit_vector(vector):
    return vector.count(1) == 1 and vector.count(0) == len(vector) - 1


def is_negative_unit_vector(vector):
    return vector.count(-1) == 1 and vector.count(0) == len(vector) - 1


def get_column(matrix, col):
    return [row[col] for row in matrix]


def get_unit_vector_indeces(coefficients):
    cols, indeces = len(coefficients[0]), []
    for col in range(cols):
        if is_unit_vector(get_column(coefficients, col)):
            indeces.append(col)

    unit_vector_indeces = []
    for row in coefficients:
        for index in indeces:
            if row[index] == 1:
                unit_vector_indeces.append(index)

    return unit_vector_indeces


def canonical_form(objective_function: str, constraints: list[str]):
    max_or_min = 'min' if objective_function.find('min') != -1 else 'max'
    objective_function = get_coefficient(objective_function)

    if max_or_min == 'min':
        objective_function = [-element for element in objective_function]

    coefficients = [get_coefficient(constraint) for constraint in constraints]
    P0 = []

    matrix_rows_to_same_size(objective_function, coefficients)

    for index, constraint in enumerate(constraints):
        comparison_type, number = parse_comparison_string(constraint)
        if comparison_type == '<=':
            add_column_to_matrix(coefficients)
            coefficients[index][-1] = 1
        elif comparison_type == '>=':
            add_column_to_matrix(coefficients)
            coefficients[index][-1] = -1

        P0.append(number)

    unit_vector_indeces = get_unit_vector_indeces(coefficients)

    if len(unit_vector_indeces) != len(constraints):
        cols = len(coefficients[0])
        for col in range(cols):
            if is_negative_unit_vector(get_column(coefficients, col)):
                row_with_negative_value = 0
                for row in range(len(coefficients)):
                    if coefficients[row][col] == -1:
                        row_with_negative_value = row
                        break

                is_possible_to_invert = True
                for index in unit_vector_indeces:
                    if coefficients[row_with_negative_value][index] == 1:
                        is_possible_to_invert = False
                        break

                if is_possible_to_invert:
                    coefficients[row_with_negative_value] = [
                        -element for element in coefficients[row_with_negative_value]]
                    P0[row_with_negative_value] = -P0[row_with_negative_value]
                    unit_vector_indeces.append(col)

            if len(unit_vector_indeces) == len(constraints):
                break

        if len(unit_vector_indeces) != len(constraints):
            constraints_without_artificial_variables = []
            for row in range(len(coefficients)):
                if not any(coefficients[row][index] == 1 for index in unit_vector_indeces):
                    constraints_without_artificial_variables.append(row)

            list_to_size(objective_function, len(coefficients[0]))
            for row in constraints_without_artificial_variables:
                add_column_to_matrix(coefficients)
                objective_function.append(0)
                coefficients[row][-1] = 1
                unit_vector_indeces.append(len(coefficients[row]) - 1)
                objective_function[unit_vector_indeces[-1]] = '-M'

                if len(unit_vector_indeces) == len(constraints):
                    break

    unit_vector_indeces = get_unit_vector_indeces(coefficients)

    list_to_size(objective_function, len(coefficients[0]))

    return objective_function, max_or_min, coefficients, P0, unit_vector_indeces
