import concurrent_run as cr
import argparse
import multiprocessing
import time
import numpy


def run_forever_from_server(server_name, number_of_workers, machine_name, is_parallel=True, allow_loop=True,
                            check_abandoned=False):
    all_times = []
    while True:
        start_time = time.time()
        print("-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-")
        if post_process_scatter:
            no_more_jobs = cr.run_post_process_scatter_from_server(get_lines_from, machine_name)
        else:
            no_more_jobs = cr.run_batch_from_server(server_name, number_of_workers, machine_name, parallel=is_parallel,
                                                check_abandoned=check_abandoned)
        print("-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-++-+-+-+-+-+-+-+-+-+-+-+-+-+-")
        finish_time = time.time()
        total_time = finish_time-start_time
        all_times.append(total_time)
        print("[BATCH TIME] Current total time {}".format(parse_seconds_to_time(total_time)))
        print("[BATCH TIME] Current average time {}".format(parse_seconds_to_time(numpy.mean(all_times))))
        if no_more_jobs:
            print("[NO MORE JOBS] - Batches done {}".format(len(all_times)-1))
            print("[AVERAGE TIME] {}".format(parse_seconds_to_time(numpy.mean(all_times))))
            break
        if not allow_loop:
            print("[AVERAGE TIME] {}".format(parse_seconds_to_time(numpy.mean(all_times))))
            break


def run_from_server_for(server_name, number_of_workers, machine_name, max_time):
    all_times = []
    while True:
        start_time = time.time()
        if post_process_scatter:
            cr.run_post_process_scatter_from_server(get_lines_from, machine_name)
        else:
            cr.run_batch_from_server(server_name, number_of_workers, machine_name)
        finish_time = time.time()
        total_time = finish_time - start_time
        all_times.append(total_time)
        print("[BATCH TIME] Current total time ".format(parse_seconds_to_time(total_time)))
        print("[BATCH TIME] Current average time ".format(parse_seconds_to_time(numpy.mean(all_times))))

        time_left = max_time*3600 - int(numpy.sum(all_times))
        if (time_left - int(numpy.mean(all_times))) < 0:
            print("[TIMEOUT] - Batches done {}".format(len(all_times)))
            print("[AVERAGE TIME] ".format(parse_seconds_to_time(numpy.mean(all_times))))
            break


def parse_seconds_to_time(time_in_seconds):
    hours = int(time_in_seconds//3600)
    minutes = int((time_in_seconds - hours*3600)//60)
    seconds = int(time_in_seconds-hours*3600-minutes*60)
    return str("{}:{}:{}".format(hours, minutes, seconds))


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(description="Run experiments concurrently")
    argument_parser.add_argument('-w', '--workers', type=int,
                                 help='amount of concurrent workers, if empty will default to number of cpus')
    argument_parser.add_argument('-f', '--from_file', type=str,
                                 help='filename containing the tasks parameters, if empty will use static parameters')
    argument_parser.add_argument('-l', '--line', type=str,
                                 help='line containing the instruction to run', default=-1)
    argument_parser.add_argument('-g', '--getlinesfrom', type=str,
                                 help='receives url to retreive lines', default=None)
    argument_parser.add_argument('-m', '--machinename', type=str,
                                 help='machine name', default="")
    argument_parser.add_argument('-t', '--timelimit', type=str,
                                 help='time limit to run things', default=None)
    argument_parser.add_argument('-nt', '--nothread', action='store_true', help='do not use thread, set --workers to 1')
    argument_parser.add_argument('-ca', '--checkabandoned', action='store_true', help='check abandoned jobs on server')

    argument_parser.add_argument('-pps', '--postprocscatter', action='store_true', help='check abandoned jobs on server')
    args = argument_parser.parse_args()
    # arguments
    n_workers = args.workers
    arg_file = args.from_file
    file_line = args.line
    get_lines_from = args.getlinesfrom
    machine_name = args.machinename
    max_time = args.timelimit
    no_thread = args.nothread
    check_abandoned = args.checkabandoned
    post_process_scatter = args.postprocscatter

    # use only a set of lines as commands
    if file_line > 0:
        file_lines = ((file_line.replace("(", "")).replace(")", "")).split(",")

    # if worker number not specified then set amount of workers as the maximum possible
    if n_workers is None:
        n_workers = multiprocessing.cpu_count()

    # run jobs from file
    if arg_file is not None:
        cr.run_from_file(n_workers, arg_file)

    if no_thread:
        n_workers = 1
        parallel = False
        allow_loop = True
        check_abandoned = False
    elif check_abandoned:
        n_workers = 1
        parallel = False
        allow_loop = True
    else:
        check_abandoned = False
        parallel = True
        allow_loop = True

    # get jobs from a server
    if get_lines_from is not None:
        if max_time:
            run_from_server_for(get_lines_from, n_workers, machine_name, max_time)
        else:
            run_forever_from_server(get_lines_from, n_workers, machine_name, is_parallel=parallel,
                                    allow_loop=allow_loop, check_abandoned=check_abandoned)




