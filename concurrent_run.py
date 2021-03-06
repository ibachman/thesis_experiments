from runnables import run_test, add_edges
#import create_phys_nets as cpn
import multiprocessing
import argparse
import queue
import connection_manager as cm
import sys
import data_proc.thesis_figures as pps


def worker_run(worker_queue):
    process_name = multiprocessing.current_process().name

    print('{} -- worker running'.format(process_name))
    while True:
        try:
            task = worker_queue.get(timeout=60)
        except queue.Empty:
            break
        print('{} -- borking'.format(process_name))

        # avisar que job_start (task["job_id"])
        if task["job_id"] > -1:
            task["server_connection"].set_job_doing(task["job_id"])
            print("[STARTING] worker {} starting Job {} ".format(process_name, task["job_id"]))

        #if task['args.createnetworks']:
        #    cpn.create_physical_network(task['model'], v=task['version'])
        if task['make_edges']:
            add_edges(task['x_coordinate'], task['y_coordinate'], task['exp'], task['n_inter'],
                      task['n_logic_suppliers'], task['version'], task['n_logic'], task['n_phys'],
                      task['iter'], task['model'], task['phys_iteration'], task['strategy'])
        else:
            run_test(task['x_coordinate'], task['y_coordinate'], task['exp'], task['n_inter'],
                     task['n_logic_suppliers'], task['version'], task['n_logic'], task['n_phys'],
                     task['iter'], task['READ_flag'], task['attack_type'], task['model'], task['logic'],
                     task['physical'], task['phys_iteration'], task['strategy'],
                     localized_attack_data=task['localized_attacks'],
                     process_name=process_name,
                     seismic_data=task['seismic_data'],
                     legacy=task['legacy'],
                     debug=task['debug'],
                     logic_file_name=task['logic_file_name'],
                     interlink_type=task['interlink_type'],
                     interlink_version=task['interlink_version'],
                     capped_random=task['capped_random'],
                     logical_directed_network=task['logical_directed_network'])
        # avisar que job_done (task["job_id"])
        if task["job_id"] > -1:
            task["server_connection"].set_job_done(task["job_id"])
            print("[COMPLETED] Job {} completed - {} --".format(task["job_id"], process_name))
        worker_queue.task_done()
        if worker_queue.empty():
            break
    print('[FINISHED] Finished batch')


def run_from_static_params(max_workers):
    print('Running from static parameters')
    work_queue = multiprocessing.JoinableQueue()
    the_pool = multiprocessing.Pool(max_workers,
                                    worker_run,
                                    (work_queue,))  # <-- The trailing comma is necessary!
    the_pool.close()

    n_logic = 10
    n_phys = 20
    n_inter = 3
    n_logic_suppliers = 3
    x_dim = 400
    y_dim = 400
    exp = 2.5
    at_type = 'physical'
    for i in range(5):
        new_task = {}
        new_task['x_coordinate'] = x_dim
        new_task['y_coordinate'] = y_dim
        new_task['exp'] = exp
        new_task['n_inter'] = n_inter
        new_task['n_logic_suppliers'] = n_logic_suppliers
        new_task['version'] = i
        new_task['n_logic'] = n_logic
        new_task['n_phys'] = n_phys
        new_task['attack_type'] = at_type
        new_task['READ_flag'] = False
        work_queue.put(new_task)
    work_queue.close()
    work_queue.join()


def parse_task_args(line):
    task = {}
    args = parser.parse_args(line.split())
    task['args.createnetworks'] = args.createnetworks
    task['x_coordinate'] = args.xcoordinate
    task['y_coordinate'] = args.ycoordinate
    task['logic_file_version'] = args.logic_file_version
    task['logic_file_name'] = None
    task['interlink_type'] = args.interlink_type
    task['interlink_version'] = args.interlink_version
    task['legacy'] = args.legacy
    task['debug'] = args.debug
    task['exp'] = args.exponentpg
    task['n_inter'] = args.interdependenceamount
    task['n_logic_suppliers'] = args.logicsuppliers
    task['version'] = args.version
    task['n_logic'] = args.logicnodes
    task['n_phys'] = args.physicalnodes
    task['iter'] = args.iterations
    task['attack_type'] = args.attack_types
    task['READ_flag'] = args.read
    task['model'] = args.model
    task['logic'] = args.logic
    task['physical'] = args.physical
    task['phys_iteration'] = args.physiteration
    task['strategy'] = args.strategy
    task['make_edges'] = args.makeedges
    task['logical_directed_network'] = args.logical_directed_network
    capped_random = args.capped_random
    if len(capped_random) > 0:
        task['capped_random'] = "cap{}".format(capped_random)
    else:
        task['capped_random'] = ""
    task['localized_attacks_radius'] = args.localizedattacksradius
    task['localized_attacks_center'] = args.localizedattackscenter
    task['localized_attacks_file'] = args.localizedattacksfile

    task['seismic_data_file'] = args.seismicdatafile

    localized_attack_data = {}
    if task['localized_attacks_center']:
        x_center = float(task['localized_attacks'][0])
        y_center = float(task['localized_attacks'][1])
        localized_attack_data["x_center"] = x_center
        localized_attack_data["y_center"] = y_center
    if task['localized_attacks_radius']:
        localized_attack_data["radius"] = [int(x) for x in task['localized_attacks_radius']]
    if task['localized_attacks_file']:
        localized_attack_data["file"] = task['localized_attacks_file']
    task['localized_attacks'] = localized_attack_data

    seismic_data = {}
    if task['logic_file_version']:
        task['logic_file_name'] = "logic_exp_{}_v{}.csv".format(task['exp'], task['logic_file_version'])

    if task['seismic_data_file']:
        print(task['seismic_data_file'])
        seismic_data["file"] = task['seismic_data_file']
    task['seismic_data'] = seismic_data

    if len(localized_attack_data) > 0:
        task['attack_type'] = ['localized']

    if len(seismic_data) > 0:
        task['attack_type'] = ['seismic']

    return task


def run_from_file(max_workers, filename, file_lines=[]):
    file_lines = [int(l) for l in file_lines]
    with open(filename) as f:
        lines = [line.rstrip('\n') for line in f.readlines()]
        if len(file_lines) > 0:
            lines = [lines[i] for i in file_lines]
    run_command_lines(max_workers, lines)


def run_command_lines(max_workers, command_lines, from_server=None, parallel=True, process_name=""):
    if parallel:
        job_id = -1
        work_queue = multiprocessing.JoinableQueue()
        the_pool = multiprocessing.Pool(max_workers,
                                        worker_run,
                                        (work_queue,))  # <-- The trailing comma is necessary!
        the_pool.close()
        for job in command_lines:
            if from_server:
                line = job["line"]
                job_id = job["job_id"]
            else:
                line = job
            new_task = parse_task_args(line)

            new_task["job_id"] = job_id
            new_task["server_connection"] = from_server
            work_queue.put(new_task)
        work_queue.close()
        # the_pool.join()
        work_queue.join()
        return work_queue
    else:
        for job in command_lines:
            if from_server:
                line = job["line"]
                job_id = job["job_id"]
            else:
                line = job
            task = parse_task_args(line)
            task["job_id"] = job_id
            task["server_connection"] = from_server

            print('{} -- borking'.format(process_name))
            # avisar que job_start (task["job_id"])
            if task["job_id"] > -1:
                task["server_connection"].set_job_doing(task["job_id"])
                print("[STARTING] worker {} starting Job {} ".format(process_name, task["job_id"]))

            #if task['args.createnetworks']:
                #cpn.create_physical_network(task['model'], v=task['version'])
            if task['make_edges']:
                add_edges(task['x_coordinate'], task['y_coordinate'], task['exp'], task['n_inter'],
                          task['n_logic_suppliers'], task['version'], task['n_logic'], task['n_phys'],
                          task['iter'], task['model'], task['phys_iteration'], task['strategy'])
            else:
                run_test(task['x_coordinate'], task['y_coordinate'], task['exp'], task['n_inter'],
                         task['n_logic_suppliers'], task['version'], task['n_logic'], task['n_phys'],
                         task['iter'], task['READ_flag'], task['attack_type'], task['model'], task['logic'],
                         task['physical'], task['phys_iteration'], task['strategy'],
                         localized_attack_data=task['localized_attacks'],
                         process_name=process_name,
                         seismic_data=task['seismic_data'],
                         legacy=task['legacy'],
                         debug=task['debug'],
                         logic_file_name=task['logic_file_name'],
                         interlink_type=task['interlink_type'],
                         interlink_version=task['interlink_version'],
                         capped_random=task['capped_random'],
                         logical_directed_network=task['logical_directed_network'])
            # avisar que job_done (task["job_id"])
            if task["job_id"] > -1:
                task["server_connection"].set_job_done(task["job_id"])
                print("[COMPLETED] Job {} completed - {} --".format(task["job_id"], process_name))

        print('[FINISHED] Finished batch')


def run_batch_from_server(server_name, n_workers, machine_name, parallel=True, check_abandoned=False):
    server_connection = cm.ConnectionManager(server_name)
    if machine_name:
        server_connection.set_machine_name(machine_name)
    if parallel:
        lines = server_connection.get_all_jobs_from_server("PENDING")
    elif check_abandoned:
        lines = server_connection.restart_abandoned_job()
    else:
        lines = server_connection.get_jobs_from_server(1)
        n_workers = 1
    n_lines = len(lines)
    if n_lines > 0:
        if n_lines < n_workers:
            rest = n_workers - n_lines
            print("[FREE CORES] received {} jobs for {} cores, {} cores available".format(n_lines, n_workers, rest))
            n_workers = len(lines)
        run_command_lines(n_workers, lines, from_server=server_connection, parallel=parallel,
                              process_name=machine_name)
    else:
        print("[EMPTY ANSWER] No lines received")
        return True


def run_post_process_scatter_from_server(server_name, machine_name):
    server_connection = cm.ConnectionManager(server_name)
    server_connection.set_machine_name(machine_name)
    lines = server_connection.get_jobs_from_server(1)
    n_lines = len(lines)
    if n_lines > 0:
        line = lines[0]["line"]
        job_id = lines[0]["job_id"]
        server_connection.set_job_doing(job_id)
        split_line = line.split(" ")
        model = split_line[0]
        strategy = split_line[1]
        imax = split_line[2]
        if strategy == "simple_graphs":
            strategy = strategy.replace("_", " ")
        pps.pre_process_seismic_scatter_data(model, ndep=imax, strategy=[strategy])
        server_connection.set_job_done(job_id)
        return False
    else:
        print("[EMPTY ANSWER] No line received")
        return True


parser = argparse.ArgumentParser(description="Run experiments with the given variables")
parser.add_argument('-ln', '--logicnodes', type=int, help='amount of nodes in the logic network')
parser.add_argument('-pn', '--physicalnodes', type=int, help='amount of nodes in the physical network')
parser.add_argument('-ia', '--interdependenceamount', type=int, help='maximum amount of interconnections')
parser.add_argument('-ls', '--logicsuppliers', type=int, help='amount of suppliers in the logic network')
parser.add_argument('-e', '--exponentpg', type=float, help='lambda exponent for logic network Power-Law')
parser.add_argument('-x', '--xcoordinate', type=int, help='width of the physical space for the physical network')
parser.add_argument('-y', '--ycoordinate', type=int, help='length of the physical space for the physical network')
parser.add_argument('-v', '--version', type=int, help='version for this kind of interdependent systems')
parser.add_argument('-i', '--iterations', type=int, help='Number of iterations to perform')
parser.add_argument('-r', '--read', action='store_true', help='If this is specified will read the networks from file')
parser.add_argument('-at', '--attack_types', type=str, nargs='?', const='', default='physical,logic,both',
                    help='Optional argument. Type of attack to simulate, valid values are physical, logic and both')
parser.add_argument('-m', '--model', type=str, nargs='?', const='', default='RNG,GG,5NN',
                    help='Optional argument. Type of Physical Network to simulate, valid values are MRN, GG and 5NN')
parser.add_argument('-l', '--logic', action='store_true', help='If this is specified will create logic layer')
parser.add_argument('-p', '--physical', action='store_true', help='If this is specified will create physical network')
parser.add_argument('-it', '--physiteration', type=int, help='Number of iteration when creating set of edges', default=0)
parser.add_argument('-st', '--strategy', type=str, help='Strategy for adding new edges', default='')
parser.add_argument('-me', '--makeedges', action='store_true', help='Create extra edges for strategy')
parser.add_argument('-lar', '--localizedattacksradius',  nargs='*', help='Test localized attacks. Receives [radius1, ...]')
parser.add_argument('-lac', '--localizedattackscenter',  nargs=2, help='Test localized attacks. Receives [x_center, y_center]')
parser.add_argument('-laf', '--localizedattacksfile',  nargs=1, help='Test localized attacks. Receives filename]')

parser.add_argument('-sf', '--seismicdatafile', type=str, help='Test seismic attacks. Receives filename]')

parser.add_argument('-cn', '--createnetworks', action='store_true', help='Create networks from debug function')
parser.add_argument('-leg', '--legacy', action='store_true', help='use legacy files')
parser.add_argument('-d', '--debug', action='store_true', help='save as debug results')
parser.add_argument('-lfv', '--logic_file_version', type=int, help='logic file version', default=None)
parser.add_argument('-intt', '--interlink_type', type=str, help='type of interlink used', default=None)
parser.add_argument('-intv', '--interlink_version', type=int, help='type of interlink used', default=1)

parser.add_argument('-crand', '--capped_random', type=str, help='type of interlink used', default="")

parser.add_argument('-ld', '--logical_directed_network', type=str, help='use a directed graph for the logical network', default="")


if __name__ == "__main__":
    line = " ".join(sys.argv[1::])
    run_command_lines(1, [line])



