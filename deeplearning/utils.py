def invert_dictionary(dictionary):
    new_dict = {}
    for key in dictionary:
        value = dictionary[key]
        if value in new_dict:
            new_dict[value].append(key)
        else:
            new_dict[value] = [key]
    return new_dict
