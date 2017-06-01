# Removes the file extension from a filename
def remove_extension(file_name):
    i = len(file_name) -1
    return_string = ""
    f_dot = False
    while i >= 0:
        if not f_dot:
            if file_name[i] == ".":
                f_dot = True
        else:
            return_string += file_name[i]

        i -= 1

    if return_string == "":
        return_string = reverse_string(file_name)
    return reverse_string(return_string)


# Reverses a string
def reverse_string(string_original):
    return string_original[::-1]
