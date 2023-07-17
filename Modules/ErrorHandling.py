import sys
import re

# Global error dictionary
ERROR_STR = {"code": 0, "message": "", "description": "", "line": "", "file": ""}

# Global list to store error dictionaries
ERROR_LIST = []


class ASErr(Exception):
    """Custom exception class."""
    pass


def set_error(code=-1000, message="Unexpected error", description="", line=None, filename=None):
    """
    Set the error information.

    Args:
        code (int): Error code (default: -1000).
        message (str): Error message (default: "Unexpected error").
        description (str): Error description.
        line (int): Line number where the error occurred.
        filename (str): Name of the file where the error occurred.

    Returns:
        dict: Error dictionary containing code, message, description, line, and file.

    """
    exc_type, exc_message, tb = sys.exc_info()

    if tb:
        frame = tb.tb_frame
        s_filename = filename if filename else frame.f_code.co_filename
        s_line = line if line else tb.tb_lineno
    else:
        s_filename = filename if filename else "Not defined"
        s_line = line if line else "Not defined"

    # Set description by combining s_description, raised error message, or a default if none is passed
    s_description = description + str(exc_message) if exc_message else ""
    if not s_description:
        s_description = "Error set or raised without description"

    ERROR_STR["code"] = code
    ERROR_STR["message"] = message
    ERROR_STR["description"] = s_description
    ERROR_STR["line"] = s_line
    ERROR_STR["file"] = s_filename

    ERROR_LIST.append(ERROR_STR)
    return ERROR_STR


def set_error_list(error_list_data):
    """
    Set the error list.

    Args:
        error_list_data (list): List of error dictionaries.

    """
    global ERROR_LIST
    ERROR_LIST = error_list_data


def clear_error():
    """Clear the error information."""
    global ERROR_STR, ERROR_LIST
    ERROR_STR = {"code": 0, "message": "", "description": "", "line": "", "file": ""}
    ERROR_LIST = []


def remove_error(error_dict):
    """
    Remove the specified error dictionary from the error list.

    Args:
        error_dict (dict): Error dictionary to be removed.

    """
    global ERROR_LIST
    updated_error_list = []

    for error in ERROR_LIST:
        if not error == error_dict:
            updated_error_list.append(error)

    ERROR_LIST = updated_error_list


def get_error(field_name: str, regex: str):
    """
    Retrieve a list of error dictionaries based on the specified field name and regular expression.

    Args:
        field_name (str): Field name in the error dictionaries.
        regex (str): Regular expression to match against the field value.

    Returns:
        list: List of error dictionaries matching the specified criteria.

    """
    global ERROR_LIST
    filtered_error_list = []

    for error in ERROR_LIST:
        temp = re.findall(regex, error[field_name])
        if temp:
            filtered_error_list.append(error)

    return filtered_error_list
