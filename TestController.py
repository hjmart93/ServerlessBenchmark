from ConfigController import *
from ResultController import *
from ConfigController import *

import subprocess
import os
import time

import xml.etree.ElementTree as ET


def run_test(args):
    test_number = args[1]

    if test_number == '1':
        run_overhead_test(args)
    elif test_number == '2':
        run_concurrency_test(args)
    elif test_number == '3':
        run_container_reuse_test(args)
    elif test_number == '4':
        run_payload_test(args)
    elif test_number == '5':
        run_overhead_languages_test(args)
    elif test_number == '6':
        run_memory_test(args)
    elif test_number == '7':
        run_weight_test(args)


def run_overhead_test(args):
    serverless_provider = args[0].lower()
    test_number = args[1]
    execution_time = args[2]

    print('Getting JMeter template...')
    template = get_template(test_number)

    if template == None:
        print('No template for test founded!')
        return None

    ts = int(time.time())

    if serverless_provider == 'all':

        files = []
        for provider in get_all_providers(test_number):
            serverless_provider = provider

            if test_number == '1':
                print('Updating Template for test...')

                function_url = get_function_url(serverless_provider, test_number)

                if function_url is None or function_url =="":
                    print("No function deployed for test T" + test_number + " on " + serverless_provider + " provider")
                else:
                    update_t1_template(function_url, execution_time, template, test_number)
                    file_name = get_output_file_name(ts, serverless_provider)
                    jmeter_result = run_jmeter(get_template_path(test_number), get_output_file(test_number, file_name),
                                           get_jmeter_path(), serverless_provider, 'T' + test_number)
                    #print(str(jmeter_result.decode('UTF-8')))

                    file = (file_name, serverless_provider)
                    files.append(file)

        print('Calculate the result...')
        result_controller(test_number, files, ts, 'all', execution_time)

    else:

        if not verify_test_provider(test_number, serverless_provider):
            print("The test is not specified for that provider")
            return None;

        if test_number == '1':
            print('Updating Template for test...')
            files = []

            function_url = get_function_url(serverless_provider, test_number)

            if function_url is None or function_url == "":
                print("No function deployed for test T" + test_number + " on " + serverless_provider + " provider")
            else:
                update_t1_template(function_url, execution_time, template, test_number)
                file_name = get_output_file_name(ts, serverless_provider)
                jmeter_result = run_jmeter(get_template_path(test_number), get_output_file(test_number, file_name),
                                       get_jmeter_path(), serverless_provider, 'T' + test_number)
                #print(str(jmeter_result.decode('UTF-8')))

                file = (file_name, serverless_provider)
                files.append(file)

                print('Calculate the result...')
                result_controller(test_number, files, ts, serverless_provider, execution_time)


def run_concurrency_test(args):
    serverless_provider = args[0].lower()
    test_number = args[1]
    min_concurrency = int(args[2])
    max_concurrency = int(args[3])
    concurrency_step = int(args[4])
    execution_time = args[5]

    print('Getting JMeter template...')
    template = get_template(test_number)

    if template == None:
        print('No template for test founded!')
        return None

    ts = int(time.time())

    if serverless_provider == 'all' and test_number == "2":

        files = []

        for provider in get_all_providers(test_number):
            serverless_provider = provider
            files_provider = []
            for num_threads in range(min_concurrency, max_concurrency + 1, concurrency_step):

                function_url = get_function_url(serverless_provider, test_number)

                if function_url is None or function_url =="":
                    print("No function deployed for test T" + test_number + " on " + serverless_provider + " provider")
                else:
                    update_t2_template(function_url, execution_time, template, test_number, num_threads)
                    file_name = get_output_file_name(ts, serverless_provider)
                    file_name_aux = file_name.split('.')
                    file_name_final = file_name_aux[0] + '-concurrency_' + str(num_threads) + '.' + file_name_aux[1]
                    jmeter_result = run_jmeter(get_template_path(test_number),
                                           get_output_file(test_number, file_name_final),
                                           get_jmeter_path(), serverless_provider, 'T' + test_number)
                    #print(str(jmeter_result.decode('UTF-8')))

                    throughput = get_running_data(str(jmeter_result.decode('UTF-8')))

                    file = (file_name_final, serverless_provider, num_threads, throughput)
                    files_provider.append(file)

            files.append(files_provider)

        print('Calculate the result...')
        result_controller(test_number, files, ts, "all", execution_time)

    else:

        if not verify_test_provider(test_number, serverless_provider):
            print("The test is not specified for that provider")
            return None;

        if test_number == '2':
            print('Updating Template for test...')
            files = []
            files_provider = []
            for num_threads in range(min_concurrency, max_concurrency + 1, concurrency_step):

                function_url = get_function_url(serverless_provider, test_number)

                if function_url is None or function_url =="":
                    print("No function for test T" + test_number + " on " + serverless_provider + " provider")
                else:
                    update_t2_template(function_url, execution_time, template, test_number, num_threads)
                    file_name = get_output_file_name(ts, serverless_provider)
                    file_name_aux = file_name.split('.')
                    file_name_final = file_name_aux[0] + '-concurrency_' + str(num_threads) + '.' + file_name_aux[1]
                    jmeter_result = run_jmeter(get_template_path(test_number),
                                           get_output_file(test_number, file_name_final),
                                           get_jmeter_path(), serverless_provider, 'T' + test_number)
                    #print(str(jmeter_result.decode('UTF-8')))

                    throughput = get_running_data(str(jmeter_result.decode('UTF-8')))

                    file = (file_name_final, serverless_provider, num_threads, throughput)
                    files_provider.append(file)

            # print (files)
            files.append(files_provider)
            print('Calculate the result...')
            result_controller(test_number, files, ts, serverless_provider, execution_time)


def run_container_reuse_test(args):
    serverless_provider = args[0].lower()
    test_number = args[1]
    min_wait_time = int(args[2])
    max_wait_time = int(args[3])
    time_step = int(args[4])
    execution_time = args[5]

    print('Getting JMeter template...')
    template = get_template(test_number+'_0')

    if template == None:
        print('No template for test founded!')
        return None

    ts = int(time.time())

    if serverless_provider == 'all' and test_number == "3":

        files = []

        for provider in get_all_providers(test_number):
            serverless_provider = provider
            files_provider = []

            print('Getting JMeter template...')
            template = get_template(test_number + '_0')

            if template == None:
                print('No template for test founded!')
                return None

            print('Updating Template for test...')

            function_url = get_function_url(serverless_provider, test_number)

            if function_url is None or function_url == "":
                print("No function for test T" + test_number + " on " + serverless_provider + " provider")

            else:
                update_t1_template(function_url, execution_time, template, test_number + '_0')
                file_name = get_output_file_name(ts, serverless_provider)
                file_name_aux = file_name.split('.')
                file_name_final = file_name_aux[0] + '-preexecution' + '.' + file_name_aux[1]

                jmeter_result = run_jmeter(get_template_path(test_number + '_0'),
                                       get_output_file(test_number, file_name_final),
                                       get_jmeter_path(), serverless_provider, 'T' + test_number)

                print('Pre executions:')
                #print(str(jmeter_result.decode('UTF-8')))

                template = get_template(test_number + '_1')

                if template == None:
                    print('No template for test founded!')
                    return None

                print('Updating Template for test...')

                for wait_time in range(min_wait_time, max_wait_time + 1, time_step):
                    print('\nRun test in ' + serverless_provider + ' after waiting ' + str(wait_time) + 'seconds!\n')

                    time.sleep(wait_time)


                    update_t3_template(get_function_url(serverless_provider, test_number), template,
                                       test_number + '_1')

                    file_name = get_output_file_name(ts, serverless_provider)
                    file_name_aux = file_name.split('.')
                    file_name_final = file_name_aux[0] + '-waittime_' + str(wait_time) + '.' + file_name_aux[1]

                    jmeter_result = run_jmeter(get_template_path(test_number + '_1'),
                                               get_output_file(test_number, file_name_final),
                                               get_jmeter_path(), serverless_provider, 'T' + test_number)

                    #print(str(jmeter_result.decode('UTF-8')))

                    file = (file_name_final, serverless_provider, wait_time)
                    files_provider.append(file)

                files.append(files_provider)

        #print(files)
        print('Calculate the result...')
        result_controller(test_number, files, ts, "all", execution_time)

    else:

        if not verify_test_provider(test_number, serverless_provider):
            print("The test is not specified for that provider")
            return None;

        if test_number == '3':
            print('Updating Template for test...')

            function_url = get_function_url(serverless_provider, test_number)

            if function_url is None or function_url == "":
                print("No function for test T" + test_number + " on " + serverless_provider + " provider")

            else:
                update_t1_template(function_url, execution_time, template, test_number+'_0')
                file_name = get_output_file_name(ts, serverless_provider)
                file_name_aux = file_name.split('.')
                file_name_final = file_name_aux[0] + '-preexecution' + '.' + file_name_aux[1]

                jmeter_result = run_jmeter(get_template_path(test_number+'_0'), get_output_file(test_number, file_name_final),
                                           get_jmeter_path(), serverless_provider, 'T' + test_number)

                print('Pre executions:')
                #print(str(jmeter_result.decode('UTF-8')))

                template = get_template(test_number + '_1')

                if template == None:
                    print('No template for test founded!')
                    return None

                print('Updating Template for test...')
                files = []
                files_provider = []

                for wait_time in range(min_wait_time, max_wait_time + 1, time_step):
                    print('\nRun test in ' + serverless_provider + ' after waiting ' + str(wait_time) + ' seconds!\n')

                    time.sleep(wait_time)


                    update_t3_template(get_function_url(serverless_provider, test_number), template,
                                       test_number+'_1')

                    file_name = get_output_file_name(ts, serverless_provider)
                    file_name_aux = file_name.split('.')
                    file_name_final = file_name_aux[0] + '-waittime_' + str(wait_time) + '.' + file_name_aux[1]

                    jmeter_result = run_jmeter(get_template_path(test_number+'_1'),
                                               get_output_file(test_number, file_name_final),
                                               get_jmeter_path(), serverless_provider, 'T' + test_number)



                    #print(str(jmeter_result.decode('UTF-8')))


                    file = (file_name_final, serverless_provider, wait_time)
                    files_provider.append(file)

                files.append(files_provider)
                #print(files)

                print('Calculate the result...')
                result_controller(test_number, files, ts, serverless_provider, execution_time)

def run_payload_test(args):

    serverless_provider = args[0].lower()
    test_number = args[1]
    execution_time = args[2]

    payloadsize = get_payload_size(test_number)

    print('Getting JMeter template...')
    template = get_template(test_number)

    if template == None:
        print('No template for test founded!')
        return None

    ts = int(time.time())

    if serverless_provider == 'all' and test_number == "4":

        files = []

        for provider in get_all_providers(test_number):
            serverless_provider = provider
            files_provider = []

            for pay_size in payloadsize:
                function_url = get_function_url(serverless_provider, test_number)
                if function_url is None or function_url == "":
                    print("No function for test T" + test_number + " on " + serverless_provider + " provider")

                else:
                    function_url = function_url + '?n='+str(pay_size)
                    update_t1_template(function_url, execution_time, template,test_number)
                    file_name = get_output_file_name(ts, serverless_provider)
                    file_name_aux = file_name.split('.')
                    file_name_final = file_name_aux[0] + '-payloadSize_' + str(pay_size) + '.' + file_name_aux[1]
                    jmeter_result = run_jmeter(get_template_path(test_number),
                                               get_output_file(test_number, file_name_final),
                                               get_jmeter_path(), serverless_provider, 'T' + test_number)
                    #print(str(jmeter_result.decode('UTF-8')))


                    file = (file_name_final, serverless_provider, pay_size)
                    files_provider.append(file)

            files.append(files_provider)

        #print(files)
        print('Calculate the result...')
        result_controller(test_number, files, ts, "all", execution_time)

    else:

        if not verify_test_provider(test_number, serverless_provider):
            print("The test is not specified for that provider")
            return None;

        if test_number == '4':
            print('Updating Template for test...')
            files = []
            files_provider = []
            for pay_size in payloadsize:
                function_url = get_function_url(serverless_provider, test_number)
                if function_url is None or function_url == "":
                    print("No function for test T" + test_number + " on " + serverless_provider + " provider")

                else:
                    function_url = function_url + '?n='+str(pay_size)
                    update_t1_template(function_url, execution_time, template,test_number)
                    file_name = get_output_file_name(ts, serverless_provider)
                    file_name_aux = file_name.split('.')
                    file_name_final = file_name_aux[0] + '-payloadSize_' + str(pay_size) + '.' + file_name_aux[1]
                    jmeter_result = run_jmeter(get_template_path(test_number),
                                               get_output_file(test_number, file_name_final),
                                               get_jmeter_path(), serverless_provider, 'T' + test_number)
                    #print(str(jmeter_result.decode('UTF-8')))


                    file = (file_name_final, serverless_provider, pay_size)
                    files_provider.append(file)

            files.append(files_provider)

            #print(files)
            print('Calculate the result...')
            result_controller(test_number, files, ts, serverless_provider, execution_time)


def run_overhead_languages_test(args):
    serverless_provider = args[0].lower()
    test_number = args[1]
    execution_time = args[2]

    print('Getting JMeter template...')
    template = get_template(test_number)

    if template == None:
        print('No template for test founded!')
        return None

    ts = int(time.time())

    if serverless_provider == 'all':

        print('Run the test for one provider at a time')

    else:

        if not verify_test_provider(test_number, serverless_provider):
            print("The test is not specified for that provider")
            return None;

        if test_number == '5':
            print('Updating Template for test...')

            functions = get_function_url(serverless_provider, test_number)
            files = []
            for prog_lang, url in functions.items():
                if url is None or url == "":
                    print("No function in " + prog_lang + " for test T" + test_number + " on " + serverless_provider + " provider")

                else:

                    update_t1_template(url, execution_time, template, test_number)
                    file_name = get_output_file_name(ts, serverless_provider)
                    file_name_aux = file_name.split('.')

                    file_name_final = file_name_aux[0] + '-Pro_Language_' + str(prog_lang) + '.' + file_name_aux[1]

                    jmeter_result = run_jmeter(get_template_path(test_number), get_output_file(test_number, file_name_final),
                                           get_jmeter_path(), serverless_provider, 'T' + test_number)
                    #print(str(jmeter_result.decode('UTF-8')))



                    file = (file_name_final, prog_lang)
                    files.append(file)

            print('Calculate the result...')
            result_controller(test_number, files, ts, serverless_provider, execution_time)


def run_memory_test(args):
    serverless_provider = args[0].lower()
    test_number = args[1]
    execution_time = args[2]

    print('Getting JMeter template...')
    template = get_template(test_number)

    if template == None:
        print('No template for test founded!')
        return None

    ts = int(time.time())

    if serverless_provider == 'all':

        print('Run the test for one provider at a time')

    else:

        if not verify_test_provider(test_number, serverless_provider):
            print("The test is not specified for that provider")
            return None;

        if test_number == '6':
            print('Updating Template for test...')

            functions = get_function_url(serverless_provider, test_number)
            files = []
            for func_mem, url in functions.items():
                if url is None or url == "":
                    print("No function with " + func_mem + "Mb of memory for test T" + test_number + " on " + serverless_provider + " provider")
                else:
                    update_t1_template(url, execution_time, template, test_number)
                    file_name = get_output_file_name(ts, serverless_provider)
                    file_name_aux = file_name.split('.')

                    file_name_final = file_name_aux[0] + '-Memory_' + str(func_mem) + '.' + file_name_aux[1]

                    jmeter_result = run_jmeter(get_template_path(test_number), get_output_file(test_number, file_name_final),
                                           get_jmeter_path(), serverless_provider, 'T' + test_number)
                    #print(str(jmeter_result.decode('UTF-8')))



                    file = (file_name_final, func_mem)
                    files.append(file)

            print('Calculate the result...')
            result_controller(test_number, files, ts, serverless_provider, execution_time)



def run_weight_test(args):

    serverless_provider = args[0].lower()
    test_number = args[1]
    execution_time = args[2]

    weights = get_computacional_weights(test_number)

    print('Getting JMeter template...')
    template = get_template(test_number)

    if template == None:
        print('No template for test founded!')
        return None

    ts = int(time.time())

    if serverless_provider == 'all' and test_number == "7":

        files = []

        for provider in get_all_providers(test_number):
            serverless_provider = provider
            files_provider = []

            for weight in weights:
                function_url = get_function_url(serverless_provider, test_number)
                if function_url is None or function_url == "":
                    print("No function for test T" + test_number + " on " + serverless_provider + " provider")
                else:
                    function_url = function_url + '?n='+str(weight)
                    update_t1_template(function_url, execution_time, template,test_number)
                    file_name = get_output_file_name(ts, serverless_provider)
                    file_name_aux = file_name.split('.')
                    file_name_final = file_name_aux[0] + '-fib_' + str(weight) + '.' + file_name_aux[1]
                    jmeter_result = run_jmeter(get_template_path(test_number),
                                               get_output_file(test_number, file_name_final),
                                               get_jmeter_path(), serverless_provider, 'T' + test_number)
                    #print(str(jmeter_result.decode('UTF-8')))

                    file = (file_name_final, serverless_provider, weight)
                    files_provider.append(file)

            files.append(files_provider)

        #print(files)

        print('Calculate the result...')
        result_controller(test_number, files, ts, "all", execution_time)

    else:

        if not verify_test_provider(test_number, serverless_provider):
            print("The test is not specified for that provider")
            return None;

        if test_number == '7':
            print('Updating Template for test...')
            files = []
            files_provider = []
            for weight in weights:
                function_url = get_function_url(serverless_provider, test_number)
                if function_url is None or function_url == "":
                    print("No function for test T" + test_number + " on " + serverless_provider + " provider")
                else:
                    function_url = function_url + '?n='+str(weight)
                    update_t1_template(function_url, execution_time, template,test_number)
                    file_name = get_output_file_name(ts, serverless_provider)
                    file_name_aux = file_name.split('.')
                    file_name_final = file_name_aux[0] + '-fib_' + str(weight) + '.' + file_name_aux[1]
                    jmeter_result = run_jmeter(get_template_path(test_number),
                                               get_output_file(test_number, file_name_final),
                                               get_jmeter_path(), serverless_provider, 'T' + test_number)
                    #print(str(jmeter_result.decode('UTF-8')))


                    file = (file_name_final, serverless_provider, weight)
                    files_provider.append(file)
            files.append(files_provider)

            #print(files)

            print('Calculate the result...')
            result_controller(test_number, files, ts, serverless_provider, execution_time)



def get_template(test_number):
    tree = ET.ElementTree(file=get_template_path(test_number))
    return tree


def get_template_path(test_number):
    config = read_conf()
    return config['jMeterTemplates']['T' + test_number]


def get_function_url(serverless_provider, test_number):
    config = read_conf()
    return config['functionsURL'][serverless_provider]['T' + test_number]


def update_t1_template(url, execution_time, template, test_number):
    root = template.getroot()

    for elem in template.iter():
        if elem.attrib.get('name') == 'ThreadGroup.duration':
            elem.text = execution_time
        if elem.attrib.get('name') == 'HTTPSampler.path':
            elem.text = url

    tree = ET.ElementTree(root)
    tree.write(get_template_path(test_number))


def update_t2_template(url, execution_time, template, test_number, n_treads):
    root = template.getroot()

    for elem in template.iter():
        if elem.attrib.get('name') == 'ThreadGroup.duration':
            elem.text = execution_time
        if elem.attrib.get('name') == 'HTTPSampler.path':
            elem.text = url
        if elem.attrib.get('name') == 'ThreadGroup.num_threads':
            elem.text = str(n_treads)

    tree = ET.ElementTree(root)
    tree.write(get_template_path(test_number))

def update_t3_template(url, template, test_number):
    root = template.getroot()

    for elem in template.iter():
        if elem.attrib.get('name') == 'HTTPSampler.path':
            elem.text = url

    tree = ET.ElementTree(root)
    tree.write(get_template_path(test_number))


def get_output_file_name(ts, serverless_provider):
    return str(serverless_provider) + str(ts) + '.jtl'


def get_output_file(test_number, file_name):
    config = read_conf()
    file_path = str(os.getcwd()) + '/' + str(config['jMeterResultsPath']['T' + test_number]) + '/' + str(file_name)
    print('Generated file with results:' + file_path)
    return file_path


def get_jmeter_path():
    config = read_conf()
    return config['jMeterPath']


def run_jmeter(template_path, output_file, jmeter_path, serverless_provider, test):
    print('Running test ' + test + ' in the ' + serverless_provider + ' on JMeter...')
    final_telmplate_path = str(os.getcwd()) + '/' + str(template_path)
    # print(final_telmplate_path, output_file, jmeter_path)
    aux = subprocess.check_output(['sh', 'jmeter', '-n', '-t', final_telmplate_path, '-l', output_file, '-f'],
                                  cwd=str(jmeter_path))
    return aux


def get_all_providers(test_number):
    config = read_conf()
    providers = []

    test_number_f = "T"+str(test_number)
    providers = config['providers'][test_number_f]
    #print('-----------', providers)
    return providers

def get_payload_size(test_number):
    config = read_conf()
    payloadsize=[]

    test_number_f = "T" + str(test_number) + "PayloadSize"
    payloadsize = config[test_number_f]

    return payloadsize


def get_computacional_weights(test_number):
    config = read_conf()
    weights=[]

    test_number_f = "T" + str(test_number) + "Weights"
    weights = config[test_number_f]

    return weights


def verify_test_provider(test_number, provider):
    config = read_conf()
    providers = []

    test_number_f = "T" + str(test_number)
    providers = config['providers'][test_number_f]

    if provider in providers:
        return True
    return False



def get_running_data(result_data):
    aux = str(result_data).split('\n')

    for line in aux:
        if 'summary =' in line:
            info = line.split('/')
            return info[0].split(' ')[-1]
