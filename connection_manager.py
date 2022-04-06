import http.client
import json
import datetime


def get_lines_from_json(json_data, check_status=None):
    data = json.load(json_data)
    lines = []
    for index in data:
        if check_status:
            if data[index]["status"] == check_status:
                lines.append({"job_id": data[index]["id"],
                              "line": data[index]["instruction"],
                              "last_modified": data[index]["last_modified"],
                              "machine_id": data[index]["machine_id"]})
        else:
            lines.append({"job_id": data[index]["id"], "line": data[index]["instruction"]})
    return lines


class ConnectionManager:
    server_name = ""
    connection = None
    machine_name = None

    def __init__(self, server_name, machine_name=""):
        self.server_name = server_name
        self.machine_name = machine_name

    def set_machine_name(self, machine_name):
        self.machine_name = machine_name

    def set_job_done(self, job_id):
        self.connection = http.client.HTTPSConnection(self.server_name)
        uri = "/job_done/{}".format(job_id)
        self.connection.request("GET", uri)
        json_data = self.connection.getresponse()

    def set_job_doing(self, job_id, machine_name=None):
        # job_start/4849
        self.connection = http.client.HTTPSConnection(self.server_name)
        uri = "/job_start/{}".format(job_id)
        if machine_name:
            uri += "?machine={}".format(machine_name)
        elif self.machine_name:
            uri += "?machine={}".format(self.machine_name)
        self.connection.request("GET", uri)
        json_data = self.connection.getresponse()

    def restart_abandoned_job(self, machine_name=None):
        line = self.get_lines_for_repeated_machine_id_with_status_doing()

        if line:
            self.set_job_doing(line["job_id"], machine_name=machine_name)
            return [line]
        else:
            return self.get_jobs_from_server(1)

    def get_jobs_from_server(self, n_workers):
        self.connection = http.client.HTTPSConnection(self.server_name)
        uri = "/get_jobs/{}".format(n_workers)
        if self.machine_name:
            uri += "?machine={}".format(self.machine_name)
        self.connection.request("GET", uri)
        json_data = self.connection.getresponse()
        return get_lines_from_json(json_data)

    def get_all_jobs_from_server(self, check_status):
        self.connection = http.client.HTTPSConnection(self.server_name)
        uri = "/status/"
        self.connection.request("GET", uri)
        json_data = self.connection.getresponse()
        return get_lines_from_json(json_data, check_status=check_status)

    def get_lines_for_repeated_machine_id_with_status_doing(self):
        jobs_doing = self.get_all_jobs_from_server("DOING")
        jobs_by_machine_name = {}

        for job in jobs_doing:
            current_machine_name_split = (job["machine_id"]).split("-cmm-")
            if len(current_machine_name_split) > 1:
                current_machine_id = current_machine_name_split[1]
            else:
                continue
            if current_machine_id in jobs_by_machine_name.keys():
                (jobs_by_machine_name[current_machine_id]).append(job)
            else:
                jobs_by_machine_name[current_machine_id] = [job]

        for machine_id in jobs_by_machine_name.keys():
            job_repetition_threshold = 1
            if machine_id == "1":
                job_repetition_threshold = 2

            if len(jobs_by_machine_name[machine_id]) > job_repetition_threshold:
                # sort by oldest
                print("Machine id: {}".format(machine_id))
                oldest_date = datetime.datetime.strptime('18/09/21 01:55:19', '%d/%m/%y %H:%M:%S')
                oldest_job = None
                for job in jobs_by_machine_name[machine_id]:
                    d = job["last_modified"]
                    d = d.split(",")[1]
                    d = d.replace("May", "05")
                    date_str = ' %d %m 20%y %H:%M:%S GMT'
                    parsed_date = datetime.datetime.strptime(d, date_str)
                    if parsed_date < oldest_date:
                        oldest_date = parsed_date
                        oldest_job = job

                return oldest_job
        return None

