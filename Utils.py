import os
import random
import string


def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


'''def random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))'''


def get_path(file):
    path = os.path.dirname(os.path.abspath(__file__))
    file_path = path + os.path.sep + file
    print(file_path)
    return file_path


def get_conf_path(conf):
    path = os.path.dirname(os.path.abspath(__file__))
    conf_path = path + os.path.sep + "conf" + os.path.sep + conf + ".conf"
    print(conf_path)
    return conf_path
