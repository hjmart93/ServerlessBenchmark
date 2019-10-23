#Overview

Expandable command-line software tool to benchmark serverless platforms from Amazon, Google, Microsoft and IBM.

The seven deﬁned tests cover scalability (latency and throughput), the effect of allocated memory, the performance for CPU-bound cases, the impact of payload size, the inﬂuence of the programming language, resource management (e.g., reuse of containers), and overall platform overhead.



#Commands to run the tests

##Test T1

ServerlessBenchmarkAppInterface.py -t serverless_provider 1 execution_time
where serverless_provider is the provider;
and execution_time is the amount of time the test should last.

##Test T2

ServerlessBenchmarkAppInterface.py -t serverless_provider 2 min_concurrency max_concurrency concurrency_step level_concurrency_execution_time
where min_concurrency is the starting level of concurrency;
max_concurrency is the final level;
concurrency_step is the step, e.g., from 1 to 30 step 2, would run the test with concurrence 1, 3, 5, etc. up to 29;
and level_concurrency_execution_time is the time the tool spends on each concurrency level.

##Test T3

ServerlessBenchmarkAppInterface.py -t serverless_provider 3 min_wait_time max_wait_time time_step pre_execution_time
where min_wait_time is the first interval of waiting time between invocations;
max_wait_time is the last interval;
time_step is the step increment from the minimum to the maximum;
and re_execution_time is a warm-up time with invocations before the actual test, to enable the platform to prepare containers.

##Test T4

ServerlessBenchmarkAppInterface.py -t serverless_provider 4 execution_time
where the meaning of the parameters is the same as in Test T1.

##Test T5

ServerlessBenchmarkAppInterface.py -t serverless_provider 5 execution_time
where the meaning of the parameters is the same as in Test T1.

##Test T6

ServerlessBenchmarkAppInterface.py -t serverless_provider 6 execution_time
where the meaning of the parameters is the same as in Test T1.

##Test T7

ServerlessBenchmarkAppInterface.py -t serverless_provider 7 execution_time
where the meaning of the parameters is the same as in Test T1.
       
