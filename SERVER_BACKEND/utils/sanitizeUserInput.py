import nh3

def sanitize_user_input(data):
    for key in data:
        data[key]=nh3.clean(data[key])
    return data
