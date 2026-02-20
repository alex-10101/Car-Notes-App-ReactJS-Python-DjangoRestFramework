import nh3

def sanitize_user_input(data):
    for key in data:
        if type(data[key]) == str:
            data[key]=nh3.clean(data[key])
    return data