
def convert_string_to_list(my_str):
    if my_str == '':
        return []
    my_list = my_str.split(',')
    my_list = [int(i) for i in my_list]
    return my_list

def convert_list_to_string(my_list):
    for i in range(len(my_list)):
        my_list[i] = str(my_list[i])
    my_str = ','.join(my_list)
    return my_str

def check_two_list(new_list, old_list):
    if new_list.sort().copy() == old_list.sort().copy():
        return [None, 'not_change']
