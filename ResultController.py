from ConfigController import *




from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 14})
plt.rcParams["font.family"] = "Arial"


def result_controller(test_number, files, ts, serverless_provider, execution_time):
    colors = ['red', 'green', 'blue', 'orange', 'yellow', 'pink', 'grey', 'brown', 'olive', 'cyan', 'purple',
              'darksalmon', 'lime', 'dodgerblue', 'springgreen', 'hotpink']
    result_path = benchmark_result_path(test_number)
    # antes do teste dois : ax = plt.gca()
    color_n = 0
    if test_number == '1':
        ax = plt.gca()
        for file in files:
            df = None

            provider = file[1]
            print('\n\n\n')
            print('Result for test T'+test_number+' in the '+provider+' provider during ' + str(execution_time) + ' seconds:')
            jmeter_file = get_jmeter_result_path(test_number) + '/' + str(file[0])
            df = pd.read_csv(jmeter_file)
            df['RealLatency'] = df['Latency'] - df['Connect']
            print('Max Latency:', df['RealLatency'].max())
            print('Min Latency: ', df['RealLatency'].min())
            print('Avg Latency:', df['RealLatency'].mean())
            print('Std Latency', df['RealLatency'].std())
            print('10th percentile: ', df['RealLatency'].quantile(0.1))
            print('90th percentile: ', df['RealLatency'].quantile(0.9))
            print('% of Success', len(df[df['responseCode'] == 200]) / df['RealLatency'].count() * 100)
            print('% of Failure', len(df[df['responseCode'] != 200]) / df['RealLatency'].count() * 100)
            print('Number executions', df['RealLatency'].count())

            if provider == 'ow':
                provider = 'ibm bluemix'


            df.reset_index().plot(kind='line', y='RealLatency', x='index', color=colors[color_n], label=provider, ax=ax)
            color_n += 1

        plt.xlabel('Function Invocation Sequence Number')
        plt.ylabel('Latency (ms)')
        plt.title('Latency of a sequence of invocations during '+execution_time+' seconds')

        fig1 = plt.gcf()
        plt.show()

        fig1.savefig(str(result_path)+'/'+str(serverless_provider)+'-'+str(ts)+'.png', transparent=False)

    if test_number == '2':
        fig = plt.figure()
        ax1 = fig.gca()
        ax2 = ax1.twinx()

        data = []
        provider = ''
        data_frame = None
        for file in files:
            data_frame = None
            data = []
            df = None
            for file_provider in file:

                provider = file_provider[1]
                n_threads = file_provider[2]
                throughput = file_provider[3]
                print('\n\n\n')
                print('Result for test T'+test_number+' in the '+provider+' provider with ' + str(n_threads) + ' concurrent requests during ' + str(execution_time) +' seconds')
                jmeter_file = get_jmeter_result_path(test_number) + '/' + str(file_provider[0])
                df = pd.read_csv(jmeter_file)
                df['RealLatency'] = df['Latency'] - df['Connect']
                print('Max Latency:', df['RealLatency'].max())
                print('Min Latency: ', df['RealLatency'].min())
                print('Avg Latency:', df['RealLatency'].mean())
                print('Std Latency', df['RealLatency'].std())
                print('10th percentile: ', df['RealLatency'].quantile(0.1))
                print('90th percentile: ', df['RealLatency'].quantile(0.9))
                print('% of Success', len(df[df['responseCode'] == 200]) / df['RealLatency'].count() * 100)
                print('% of Failure', len(df[df['responseCode'] != 200]) / df['RealLatency'].count() * 100)
                print('Number executions', df['RealLatency'].count())
                throughput = (df['RealLatency'].count()-1)/900
                print('Throughput ' + str(throughput) + '/s')
                data.append({'concurrency': n_threads, 'avg': df['RealLatency'].mean(), 'throughput': float(throughput)})

            data_frame = pd.DataFrame(data)
            # print(pd.DataFrame(data))
            if provider == 'ow':
                provider = 'ibm bluemix'
            data_frame.plot(marker='o', kind='line', y='avg', x='concurrency', color=colors[color_n], label=provider + ' Latency', ax=ax1)
            color_n += 1
            data_frame.plot(marker='o', kind='line', y='throughput', x='concurrency', color=colors[color_n], label=provider + ' Throughput', ax=ax2)
            color_n += 1

        ax1.set_ylabel('Average Latency (ms)')
        ax2.set_ylabel('Throughput (1/s)')
        ax1.set_xlabel('Number of concurrent requests')


        #plt.title('Average latency and throughput for concurrency level during '+str(execution_time)+' seconds')
        ax1.legend(frameon=True, loc='best', ncol=1)
        ax2.legend(frameon=True, loc='center left', ncol=1)
        #plt.legend()

        fig1 = plt.gcf()
        plt.show()

        fig1.savefig(str(result_path)+'/'+str(serverless_provider)+'-'+str(ts)+'.png', transparent=False)
        fig1.savefig(str(result_path) + '/' + str(serverless_provider) + '-' + str(ts) + '.pdf', transparent=False)

    if test_number == "3":
        ax = plt.gca()
        data = []
        provider = ''

        for file in files:
            data_frame = None
            data = []

            for file_provider in file:
                df = None
                provider = file_provider[1]
                wait_time = file_provider[2]

                print('\n\n')

                print('Result for test T' + test_number + ' in the ' + provider +
                      ' provider with time since last execution = ' + str(wait_time))

                jmeter_file = get_jmeter_result_path(test_number) + '/' + str(file_provider[0])
                df = pd.read_csv(jmeter_file)

                df['RealLatency'] = df['Latency'] - df['Connect']

                print('Max Latency:', df['RealLatency'].max())
                print('Min Latency: ', df['RealLatency'].min())
                print('Avg Latency:', df['RealLatency'].mean())
                print('Std Latency', df['RealLatency'].std())
                print('10th percentile: ', df['RealLatency'].quantile(0.1))
                print('90th percentile: ', df['RealLatency'].quantile(0.9))
                print('% of Success', len(df[df['responseCode'] == 200]) / df['RealLatency'].count() * 100)
                print('% of Failure', len(df[df['responseCode'] != 200]) / df['RealLatency'].count() * 100)
                print('Number executions', df['RealLatency'].count())

                data.append({'waittime': int(wait_time)/60, 'avg': df['RealLatency'].mean()})


            data_frame = pd.DataFrame(data)
            ax.set_xticks(data_frame['waittime'])
            if provider == 'ow':
                provider = 'ibm bluemix'
            data_frame.reset_index().plot(marker='o', kind='line', y='avg', x='waittime', color=colors[color_n], label=provider, ax=ax)
            color_n += 1


        plt.xlabel('Time Since Last Execution (min)')
        plt.ylabel('Latency (ms)')
        #plt.title('Container Reuse Latency')

        fig1 = plt.gcf()
        plt.show()

        fig1.savefig(str(result_path) + '/' + str(serverless_provider) + '-' + str(ts) + '.png', transparent=False)
        fig1.savefig(str(result_path) + '/' + str(serverless_provider) + '-' + str(ts) + '.pdf', transparent=False)

    if test_number == "4":
        ax = plt.gca()
        data = []
        provider = ''

        for file in files:
            data_frame = None
            data = []

            for file_provider in file:
                df = None
                provider = file_provider[1]
                payload_size = file_provider[2]

                print('\n\n')

                print('Result for test T' + test_number + ' in the ' + provider +
                      ' provider with payload size = ' + str(payload_size) + 'Kb')

                jmeter_file = get_jmeter_result_path(test_number) + '/' + str(file_provider[0])
                df = pd.read_csv(jmeter_file)

                df['RealLatency'] = df['elapsed'] - df['Connect']

                print('Max Latency:', df['RealLatency'].max())
                print('Min Latency: ', df['RealLatency'].min())
                print('Avg Latency:', df['RealLatency'].mean())
                print('Std Latency', df['RealLatency'].std())
                print('10th percentile: ', df['RealLatency'].quantile(0.1))
                print('90th percentile: ', df['RealLatency'].quantile(0.9))
                print('% of Success', len(df[df['responseCode'] == 200]) / df['RealLatency'].count() * 100)
                print('% of Failure', len(df[df['responseCode'] != 200]) / df['RealLatency'].count() * 100)
                print('Number executions', df['RealLatency'].count())

                data.append({'payloadsize': payload_size, 'avg': df['RealLatency'].mean()})


            data_frame = pd.DataFrame(data)
            #ax.set_xticks(data_frame['payloadsize'])
            if provider == 'ow':
                provider = 'ibm bluemix'
            data_frame.reset_index().plot(marker='o', kind='line', y='avg', x='payloadsize', color=colors[color_n], label=provider, ax=ax)
            color_n += 1

        execution_time = 900
        plt.xlabel('Payload Size (KBytes)')
        plt.ylabel('Latency (ms)')
        #plt.title('Average latency for payload size during '+str(execution_time)+' seconds')

        fig1 = plt.gcf()
        plt.show()

        fig1.savefig(str(result_path) + '/' + str(serverless_provider) + '-' + str(ts) + '.png', transparent=False)
        fig1.savefig(str(result_path) + '/' + str(serverless_provider) + '-' + str(ts) + '.pdf', transparent=False)

    if test_number == '5':
        ax = plt.gca()
        for file in files:
            df = None

            language = file[1]
            print('\n\n\n')
            print('Result for test T'+test_number+' in the '+serverless_provider+' provider during ' + str(execution_time) + ' seconds, with ' +language+ ' as programming language of function:')
            jmeter_file = get_jmeter_result_path(test_number) + '/' + str(file[0])
            df = pd.read_csv(jmeter_file)

            df['RealLatency'] = df['Latency'] - df['Connect']
            print('Max Latency:', df['RealLatency'].max())
            print('Min Latency: ', df['RealLatency'].min())
            print('Avg Latency:', df['RealLatency'].mean())
            print('Std Latency', df['RealLatency'].std())
            print('10th percentile: ', df['RealLatency'].quantile(0.1))
            print('90th percentile: ', df['RealLatency'].quantile(0.9))
            print('% of Success', len(df[df['responseCode'] == 200]) / df['RealLatency'].count() * 100)
            print('% of Failure', len(df[df['responseCode'] != 200]) / df['RealLatency'].count() * 100)
            print('Number executions', df['RealLatency'].count())


            df.reset_index().plot(kind='line', y='RealLatency', x='index', color=colors[color_n], label=language, ax=ax)
            color_n += 1

        plt.xlabel('Function Invocation Sequence Number')
        plt.ylabel('Latency (ms)')
        plt.title('Latency of a sequence of invocations of different programming languages during '+execution_time+' seconds')

        fig1 = plt.gcf()
        plt.show()

        fig1.savefig(str(result_path)+'/'+str(serverless_provider)+'-'+str(ts)+'.png', transparent=False)
        fig1.savefig(str(result_path) + '/' + str(serverless_provider) + '-' + str(ts) + '.pdf', transparent=False)

    if test_number == '6':
        ax = plt.gca()
        for file in files:
            df = None

            memory = file[1]
            print('\n\n\n')
            print('Result for test T'+test_number+' in the '+serverless_provider+' provider during ' + str(execution_time) + ' seconds, with ' +memory+ ' of memory of function:')
            jmeter_file = get_jmeter_result_path(test_number) + '/' + str(file[0])
            df = pd.read_csv(jmeter_file)

            df['RealLatency'] = df['Latency'] - df['Connect']
            print('Max Latency:', df['RealLatency'].max())
            print('Min Latency: ', df['RealLatency'].min())
            print('Avg Latency:', df['RealLatency'].mean())
            print('Std Latency', df['RealLatency'].std())
            print('10th percentile: ', df['RealLatency'].quantile(0.1))
            print('90th percentile: ', df['RealLatency'].quantile(0.9))
            print('% of Success', len(df[df['responseCode'] == 200]) / df['RealLatency'].count() * 100)
            print('% of Failure', len(df[df['responseCode'] != 200]) / df['RealLatency'].count() * 100)
            print('Number executions', df['RealLatency'].count())


            df.reset_index().plot(kind='line', y='RealLatency', x='index', color=colors[color_n], label=memory, ax=ax)
            color_n += 1

        plt.xlabel('Function Invocation Sequence Number')
        plt.ylabel('Latency (ms)')
        plt.title('Latency of a sequence of invocations with different memory levels during '+execution_time+' seconds')

        fig1 = plt.gcf()
        plt.show()

        fig1.savefig(str(result_path)+'/'+str(serverless_provider)+'-'+str(ts)+'.png', transparent=False)
        fig1.savefig(str(result_path) + '/' + str(serverless_provider) + '-' + str(ts) + '.pdf', transparent=False)

    if test_number == "7":
        ax = plt.gca()
        data = []
        provider = ''

        for file in files:
            data_frame = None
            data = []

            for file_provider in file:
                df = None
                provider = file_provider[1]
                weight = file_provider[2]

                print('\n\n')

                print('Result for test T' + test_number + ' in the ' + provider +
                      ' provider with N of Fibonacci = ' + str(weight) + ':')

                jmeter_file = get_jmeter_result_path(test_number) + '/' + str(file_provider[0])
                df = pd.read_csv(jmeter_file)

                df['RealLatency'] = df['elapsed'] - df['Connect']

                print('Max Latency:', df['RealLatency'].max())
                print('Min Latency: ', df['RealLatency'].min())
                print('Avg Latency:', df['RealLatency'].mean())
                print('Std Latency', df['RealLatency'].std())
                print('10th percentile: ', df['RealLatency'].quantile(0.1))
                print('90th percentile: ', df['RealLatency'].quantile(0.9))
                print('% of Success', len(df[df['responseCode'] == 200]) / df['RealLatency'].count() * 100)
                print('% of Failure', len(df[df['responseCode'] != 200]) / df['RealLatency'].count() * 100)
                print('Number executions', df['RealLatency'].count())

                data.append({'n_of_fib': weight, 'avg': df['RealLatency'].mean()})


            data_frame = pd.DataFrame(data)

            if provider == 'ow':
                provider = 'ibm bluemix'
            data_frame.reset_index().plot(marker='o', kind='line', y='avg', x='n_of_fib', color=colors[color_n], label=provider, ax=ax)
            color_n += 1


        plt.xlabel('N of sequence of fibonacci ')
        plt.ylabel('Latency (ms)')
        plt.title('Average latency for Fibonacci recursive during '+str(execution_time)+' seconds')



        fig1 = plt.gcf()
        plt.show()

        fig1.savefig(str(result_path) + '/' + str(serverless_provider) + '-' + str(ts) + '.png', transparent=False)
        fig1.savefig(str(result_path) + '/' + str(serverless_provider) + '-' + str(ts) + '.pdf', transparent=False)

def get_jmeter_result_path(test_number):
    config = read_conf()
    file_path = str(config['jMeterResultsPath']['T' + test_number])
    return file_path


def benchmark_result_path(test_number):
    config = read_conf()
    return str(config['benchmarkResultsPath']['T' + test_number])
