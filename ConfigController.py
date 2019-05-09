import json


def write_conf(conf):

    with open('conf.json', 'w') as confifile:
        json.dump(conf, confifile)


def read_conf():

    if file_check('conf.json'):
        with open('conf.json') as json_file:
            data = json.load(json_file)
            return data
    return {}


def file_check(filename):
    try:
        open(filename, "r")
        return 1
    except IOError:
        return 0
