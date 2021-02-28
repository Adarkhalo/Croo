import datetime
import re


def validate_email(email: str):
    regex = '[^@]+@[^@]+\.[^@]+'
    # pass the regular expression
    # and the string in search() method
    if re.search(regex, email):
        return True
    else:
        return False


def list_to_mysql_parameters(parameters: list):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in parameters:
        str1 += ele + ','
        # return string
    return str1[:-1]


def list_to_mysql_parameters_values(parameters_values: list):
    # initialize an empty string
    str1 = ""
    # traverse in the string
    for ele in parameters_values:
        str1 += ele + ' = %s and '
        # return string
    return str1[:-5]


def bind_mysql_values(values: list):
    values_str = ""
    for i in range(0, len(values)):
        values_str += '%s,'
    values_str = values_str[:-1]
    return values_str


def bind_mysql_update(parameters: list):
    update_str = ""
    for i in range(0, len(parameters)):
        update_str += parameters[i] + ' = %s, '
    update_str = update_str[:-2]
    return update_str


def format_date(date):
    return date.strftime('%d %B %Y')


def prepare_parameters_values_mysql(obj):
    parameters = []
    values = []
    for key in vars(obj).items():
        if key[1] is not None:
            parameters.append(key[0])
            values.append(key[1])
    return {
        'parameters': parameters,
        'values': values
    }
