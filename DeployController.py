import subprocess
import os
from ConfigController import *


def deploy_functions(args):
    serverless_provider = args.deploy[0].lower()
    test_number = args.deploy[1]

    if test_number == "1" or test_number == "2" or test_number == "3" or test_number == "4" or test_number == "7":

        if serverless_provider == 'ow':
            print('Deploying in OpenWhisk/IBM Cloud Functions')

            function_path = get_function_path(serverless_provider, test_number)

            if function_path == None or function_path == "":
                print("No function(s) for test T" + test_number + " of provider " + serverless_provider)
                return None

            serverless_deploy_response = deploy(function_path, serverless_provider)
            function_url = get_ow_function_url(serverless_deploy_response,
                                               get_ow_function_name_and_package(test_number))

            if function_url is not None:
                save_function_url(serverless_provider, test_number, function_url)
                print(
                    'Function(s) for specified test is deployed with success on OpenWhisk!\nThe url of function is: ' + function_url)
            else:
                print('Error deploying:\n' + str(serverless_deploy_response.decode('UTF-8')))

        elif serverless_provider == 'aws':
            print('Deploying in AWS')

            function_path = get_function_path(serverless_provider, test_number)

            if function_path == None or function_path == "":
                print("No function(s) for test T" + test_number + " of provider " + serverless_provider)
                return None

            serverless_deploy_response = deploy(function_path, serverless_provider)
            function_url = get_aws_function_url(serverless_deploy_response,
                                                get_aws_function_name_and_package(test_number))

            if function_url is not None:
                save_function_url(serverless_provider, test_number, function_url)
                print(
                    'Function(s) for specified test is deployed with success on AWS!\nThe url of function is: ' + function_url)
            else:
                print('Error deploying:\n' + str(serverless_deploy_response.decode('UTF-8')))

        elif serverless_provider == 'azure':
            print('Deploying in Azure')

            function_path = get_function_path(serverless_provider, test_number)


            if function_path == None or function_path == "":
                print("No function(s) for test T" + test_number + " of provider " + serverless_provider)
                return None

            serverless_deploy_response = deploy(function_path, serverless_provider)
            function_url = get_azure_function_url(serverless_deploy_response,
                                                  get_azure_function_name_and_package(test_number), test_number)

            if function_url is not None:
                save_function_url(serverless_provider, test_number, function_url)
                print(
                    'Function(s) for specified test is deployed with success on Azure!\nThe url of function is: ' + function_url)
            else:
                print('Error deploying:\n' + str(serverless_deploy_response.decode('UTF-8')))

        elif serverless_provider == 'google':
            print('Deploying in google')

            function_path = get_function_path(serverless_provider, test_number)

            if function_path == None or function_path == "":
                print("No function(s) for test T" + test_number + " of provider " + serverless_provider)
                return None

            serverless_deploy_response = deploy(function_path, serverless_provider)
            function_url = get_google_function_url(serverless_deploy_response,
                                                   get_google_function_name_and_package(test_number))

            if function_url is not None:
                save_function_url(serverless_provider, test_number, function_url)
                print(
                    'Function(s) for specified test is deployed with success on Google!\nThe url of function is: ' + function_url)
            else:
                print('Error deploying:\n' + str(serverless_deploy_response.decode('UTF-8')))

        else:
            print(
                'Unknown provider!\nPlease use one of the following providers: \'aws\', \'ow\', \'azure\', \'google\'')

    elif (test_number == "5"):

        if serverless_provider == 'ow':

            function_path = get_function_path(serverless_provider, test_number)

            for prog_lang, path in function_path.items():

                if path == None or path == "":
                    print(
                        "No function(s) with " + prog_lang + " for test T" + test_number + " of provider " + serverless_provider)
                else:

                    print('Deploying in OpenWhisk/IBM Cloud Functions')

                    serverless_deploy_response = deploy(path, serverless_provider)

                    function_url = get_ow_function_url(serverless_deploy_response,
                                                       get_ow_function_language_name_and_package(test_number, prog_lang))

                    if function_url is not None:
                        save_function_language_url(serverless_provider, test_number, function_url, prog_lang)
                        print(
                            'Function in ' + prog_lang + ' for specified test is deployed with success on OW!\n'
                                                         'The url of function is: ' + function_url)
                    else:
                        print('Error deploying:\n' + str(serverless_deploy_response.decode('UTF-8')))

        elif serverless_provider == 'aws':

            function_path = get_function_path(serverless_provider, test_number)

            for prog_lang, path in function_path.items():

                if path == None or path == "":
                    print(
                        "No function(s) with " + prog_lang + " for test T" + test_number + " of provider " + serverless_provider)
                else:

                    print('Deploying in AWS')

                    serverless_deploy_response = deploy(path, serverless_provider)

                    function_url = get_aws_function_url(serverless_deploy_response,
                                                        get_aws_function_language_name_and_package(test_number, prog_lang))

                    if function_url is not None:
                        save_function_language_url(serverless_provider, test_number, function_url, prog_lang)
                        print(
                            'Function in ' + prog_lang + ' for specified test is deployed with success on AWS!\n'
                                                         'The url of function is: ' + function_url)
                    else:
                        print('Error deploying:\n' + str(serverless_deploy_response.decode('UTF-8')))
        else:
            print("The current test can't be deployed on the provider")


    elif (test_number == "6"):

        if serverless_provider == 'ow':

            function_path = get_function_path(serverless_provider, test_number)

            for prog_memory, path in function_path.items():

                if path == None or path == "":
                    print(
                        "No function(s) with " + prog_memory + " for test T" + test_number + " of provider " + serverless_provider)
                else:

                    print('Deploying in OpenWhisk/IBM Cloud Functions')

                    serverless_deploy_response = deploy(path, serverless_provider)

                    function_url = get_ow_function_url(serverless_deploy_response,
                                                       get_ow_function_language_name_and_package(test_number, prog_memory))

                    if function_url is not None:
                        save_function_language_url(serverless_provider, test_number, function_url, prog_memory)
                        print(
                            'Function with ' + prog_memory + ' MB of memory for specified test is deployed with success '
                                                             'on OW!\nThe url of function is: ' + function_url)
                    else:
                        print('Error deploying:\n' + str(serverless_deploy_response.decode('UTF-8')))

        elif serverless_provider == 'aws':


            function_path = get_function_path(serverless_provider, test_number)

            for prog_memory, path in function_path.items():

                if path == None or path == "":
                    print(
                        "No function(s) with " + prog_memory + " for test T" + test_number + " of provider " + serverless_provider)
                else:

                    print('Deploying in AWS')

                    serverless_deploy_response = deploy(path, serverless_provider)

                    function_url = get_aws_function_url(serverless_deploy_response,
                                                        get_aws_function_language_name_and_package(test_number, prog_memory))

                    if function_url is not None:
                        save_function_language_url(serverless_provider, test_number, function_url, prog_memory)
                        print(
                            'Function with ' + prog_memory + ' MB of memory for specified test is deployed with success '
                                                             'on AWS!\nThe url of function is: ' + function_url)
                    else:
                        print('Error deploying:\n' + str(serverless_deploy_response.decode('UTF-8')))

        elif serverless_provider == 'google':

            function_path = get_function_path(serverless_provider, test_number)

            for prog_memory, path in function_path.items():

                if path == None or path == "":
                    print(
                        "No function(s) with " + prog_memory + " for test T" + test_number + " of provider " + serverless_provider)
                else:

                    print('Deploying in Google')

                    serverless_deploy_response = deploy(path, serverless_provider)

                    function_url = get_google_function_url(serverless_deploy_response,
                                                        get_google_function_language_name_and_package(test_number, prog_memory))

                    if function_url is not None:
                        save_function_language_url(serverless_provider, test_number, function_url, prog_memory)
                        print(
                            'Function with ' + prog_memory + ' MB of memory for specified test is deployed with success '
                                                             'on Google!\nThe url of function is: ' + function_url)
                    else:
                        print('Error deploying:\n' + str(serverless_deploy_response.decode('UTF-8')))
        else:
            print("The current test can't be deployed on the provider")

    else:
        print('Unknown test')


def remove_functions(args):
    serverless_provider = args[0].lower()
    test_number = args[1]
    print("Removing function(s) for test T" + test_number + " of provider " + serverless_provider)

    if test_number == "1" or test_number == "2" or test_number == "3" or test_number == "4" or test_number == "7":
        if serverless_provider == "all":
            print('Remove from one provider at a time')
            return None
        function_path = get_function_path(serverless_provider, test_number)
        if function_path == None or function_path == "":
            print("No function(s) for test T" + test_number + " of provider " + serverless_provider)
            return None

        response = remove(function_path)

        print(str(response.decode('UTF-8')))

        save_function_url(serverless_provider, test_number, "")

        print('Remove done with success!')

    if test_number == "5" or test_number == "6":

        if serverless_provider == "all":
            print('Remove from one provider at a time')
            return None

        function_path = get_function_path(serverless_provider, test_number)

        for prog_lang, path in function_path.items():
            if function_path == None or function_path == "":
                print("No function(s) with " + prog_lang + " for test T" + test_number + " of provider " + serverless_provider)
            else:
                response = remove(function_path)

                print(str(response.decode('UTF-8')))

                save_function_language_url(serverless_provider,test_number, "", prog_lang)

        print('Remove done with success!')


def get_function_path(provider, test_number):
    conf = read_conf()
    path = conf['functionsPath'][provider]['T' + test_number]

    return path


def deploy(function_path, provider):
    if provider == 'google':
        aux = subprocess.check_output(['serverless', 'deploy', '-v', '--region', 'europe-west1'],
                                      cwd=str(os.getcwd()) + '/' + str(function_path))
    else:
        aux = subprocess.check_output(['serverless', 'deploy', '-v'], cwd=str(os.getcwd()) + '/' + str(function_path))


    return aux

def remove(function_path):
    aux = subprocess.check_output(['serverless', 'remove'], cwd=str(os.getcwd()) + '/' + str(function_path))
    return aux


def get_ow_function_url(serverless_response, package_and_name):

    aux2 = str(serverless_response.decode('UTF-8')).split('\n')

    for line in aux2:
        if package_and_name in line:
            return line.split()[1]

    return None


def get_aws_function_url(serverless_response, package_and_name):
    # print('------try getting url-------')

    aux2 = str(serverless_response.decode('UTF-8')).split('\n')

    for line in aux2:
        if package_and_name in line:
            return line.split()[2]

    return None


def get_google_function_url(serverless_response, package_and_name):

    aux2 = str(serverless_response.decode('UTF-8')).split('\n')

    for line in aux2:
        if package_and_name in line:
            return line.split()[0]

    return None


def get_azure_function_url(serverless_response, package_and_name, test_number):

    aux2 = str(serverless_response.decode('UTF-8')).split('\n')

    for line in aux2:
        if 'Error' in aux2:
            return None

    config = read_conf()
    function_name = config['azureFunctions']['T' + test_number]['function'].lower()
    return 'https://' + function_name + '.azurewebsites.net/api/' + package_and_name


def get_ow_function_name_and_package(test_number):
    config = read_conf()

    pack_name = config['owFunctions']['T' + test_number]['service'] + '/' + config['owFunctions']['T' + test_number][
        'function']

    return pack_name


def get_ow_function_language_name_and_package(test_number, prog_lang):
    config = read_conf()

    pack_name = config['owFunctions']['T' + test_number][prog_lang]['service'] + '/' + config['owFunctions']['T' + test_number][prog_lang][
        'function']

    return pack_name


def get_aws_function_name_and_package(test_number):
    config = read_conf()

    pack_name = '/' + config['awsFunctions']['T' + test_number]['function']

    return pack_name


def get_aws_function_language_name_and_package(test_number, prog_lang):
    config = read_conf()

    pack_name = '/' + config['awsFunctions']['T' + test_number][prog_lang]['function']

    return pack_name


def get_google_function_name_and_package(test_number):
    config = read_conf()

    pack_name = '/' + config['googleFunctions']['T' + test_number]['function']

    return pack_name


def get_google_function_language_name_and_package(test_number, prog_lang):
    config = read_conf()

    pack_name = '/' + config['googleFunctions']['T' + test_number][prog_lang]['function']

    return pack_name

def get_azure_function_name_and_package(test_number):
    config = read_conf()

    pack_name = config['azureFunctions']['T' + test_number]['service'] + '/' + \
                config['azureFunctions']['T' + test_number]['function']

    return pack_name


def save_function_url(provider, test_number, url):
    config = read_conf()
    config['functionsURL'][provider]['T' + test_number] = url
    write_conf(config)


def save_function_language_url(provider, test_number, url, prog_lang):
    config = read_conf()
    config['functionsURL'][provider]['T' + test_number][prog_lang] = url
    write_conf(config)
