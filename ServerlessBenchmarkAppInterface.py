import argparse

from DeployController import *
from TestController import *


def main():
    parser = argparse.ArgumentParser(description="Serverless Benchmark Interface!")

    # defining arguments for parser object
    parser.add_argument("-d", "--deploy", type=str, nargs=2,
                        metavar=('serverless_provider', 'test_number'),
                        help="Deploy in the provider all the functions that are needed for a specified test")

    parser.add_argument("-o", "--overhead", type=str, nargs=3,
                        metavar=('serverless_provider', 'test_number', 'execution_time'),
                        help="Run in the provider all the functions that are needed for a overhead(latency) "
                             "specified test")

    parser.add_argument("-c", "--concurrency", type=str, nargs=6,
                        metavar=('serverless_provider', 'test_number', 'min_concurrency', 'max_concurrency',
                                 'concurrency_step', 'level_concurrency_execution_time'),
                        help="Run in the provider all the functions that are needed for a concurrency"
                             " specified test")

    parser.add_argument("-b", "--backoff", type=str, nargs=6,
                        metavar=('serverless_provider', 'test_number', 'min_wait_time', 'max_wait_time',
                                 'time_step', 'pre_exec_time'),
                        help="Run in the provider all the functions that are needed for a container reuse"
                             " specified test")

    parser.add_argument("-p", "--payload", type=str, nargs=3,
                        metavar=('serverless_provider', 'test_number', 'execution_time'),
                        help="Run in the provider all the functions that are needed for payload size test")

    parser.add_argument("-l", "--language", type=str, nargs=3,
                        metavar=('serverless_provider', 'test_number', 'execution_time'),
                        help="Run in the provider all the functions that are needed for test  with different "
                             "programming languages")

    parser.add_argument("-m", "--memory", type=str, nargs=3,
                        metavar=('serverless_provider', 'test_number', 'execution_time'),
                        help="Run in the provider all the functions that are needed for test  with different "
                             "memory levels")

    parser.add_argument("-w", "--weightcomputacional", type=str, nargs=3,
                        metavar=('serverless_provider', 'test_number', 'execution_time'),
                        help="Run in the provider all the functions that are needed for test  with different "
                             "computational weight levels")

    parser.add_argument("-r", "--remove", type=str, nargs=2,
                        metavar=('serverless_provider', 'test_number'),
                        help="Remove from the provider all the functions that are needed for a specified test")

    args = parser.parse_args()

    if args.deploy != None:
        deploy_functions(args)

    if args.overhead != None:
        run_test(args.overhead)

    if args.concurrency!=None:
        run_test(args.concurrency)

    if args.backoff!=None:
        run_test(args.backoff)

    if args.payload!=None:
        run_test(args.payload)

    if args.language != None:
        run_test(args.language)

    if args.memory != None:
        run_test(args.memory)

    if args.weightcomputacional != None:
        run_test(args.weightcomputacional)

    if args.remove != None:
        remove_functions(args.remove)


if __name__ == "__main__":
    # calling the main function
    main()
