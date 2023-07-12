import sys
import re
gd_error = {"code": 0, "message": "", "description": "", "line": "", "File": ""}
gld_errorlist = []


class ASErr(Exception):
    pass


def set_error(n_code=-1000, s_message="Unexpected error", s_description="",
              s_line=None, s_filename=None):
    __err_type, __err_message, __tb = sys.exc_info()

    if __tb:
        __f = __tb.tb_frame
        __s_filename = s_filename if s_filename else __f.f_code.co_filename
        __s_line = s_line if s_line else __tb.tb_lineno
    else:
        __s_filename = s_filename if s_filename else "Not defined"
        __s_line = s_line if s_line else "Not defined"

    # Set description with the s_description + message of the raised error + set a default if none passed
    __s_description = s_description + str(__err_message) if __err_message else ""
    if not __s_description:
        __s_description = "Error set or raise without description"

    gd_error["code"] = n_code
    gd_error["message"] = s_message
    gd_error["description"] = __s_description
    gd_error["line"] = __s_line
    gd_error["File"] = __s_filename

    gld_errorlist.append(gd_error)
    return gd_error


def set_error_list(ld_errlist):
    global gld_errorlist
    gld_errorlist = ld_errlist


def clear_error():
    global gd_error, gld_errorlist
    gd_error = {"code": 0, "message": "", "description": "", "line": "", "File": ""}
    gld_errorlist = []


def remove_error(d_err: dict):
    global gld_errorlist
    __ld_errlist = []

    for x in gld_errorlist:
        if not x == d_err:
            __ld_errlist.append(x)
    gld_errorlist = __ld_errlist


def get_error(s_field_name: str, s_regex: str):
    global gld_errorlist
    __ld_errlist = []

    for x in gld_errorlist:
        __temp = re.findall(s_regex, x[s_field_name])
        if __temp:
            __ld_errlist.append(x)

    return __ld_errlist
