import json
import os
import fastapi
import threading
import multiprocessing
import requests

import scan

app = fastapi.FastAPI()

if os.path.exists("machines.json"):
    machines = json.load(open("machines.json", "r"))
else:
    machines = []
    print(
        "machines.json not found, fallback to empty list, please add machines manually, or run python3 scan.py to scan for machines")


def _multiprocessor_get_status(machine):
    answer = requests.get(f"http://{machine['ip_address']}/api/v1/print_job/state", timeout=5).json()
    print(answer)
    if type(answer) == dict: answer = answer["message"]
    if answer == "Not found": answer = "Idle"
    return answer


def _multiprocessor_printer(machine):
    return requests.get(f"http://{machine['ip_address']}/api/v1/printer", timeout=5).json()


def _multiprocessor_get_name(machine):
    return requests.get(f"http://{machine['ip_address']}/api/v1/system/name", timeout=5).json()


@app.get("/")
def root():
    """
    Root endpoint, return a welcome message
    :return: a welcome message
    :return type: json
    """
    return fastapi.responses.RedirectResponse("/index.html", status_code=302)
    # return {
    #     "message": "This is a 3D printer status monitor server, using fast-api, please use the API(/docs) to check the api endpoints"}


@app.get("/machines")
def get_machines():
    """
    Get all machines
    Warning: This endpoint will return all machines, which could be a large amount of data
    Warning: This is not an update endpoint, it will return the machines.json file, which may not be up to date
    Warning: If you want to update the machines.json file, please visit /update_machine endpoint
    :return: a list of machines
    :return type: json
    """
    return machines


@app.get("/update_machines?base_ip={base_ip}&mask={mask}")
def update_machines(base_ip="192.168.0.0", mask=16):
    """
    Update machines.json file
    :return: a list of machines
    :return type: json
    """

    def run_update():
        global machines
        machines = scan.update_machines(base_ip, mask, "machines.json")

    threading.Thread(target=run_update).start()

    return {"message": "Update job submitted, please check /machines, it should be updated in a few seconds"}


@app.get("/relay?ip={ip}&path={path}")
def relay(ip, path):
    """
    Relay a request to a machine
    Warning: This could be abused to attack the machine, please use with caution or disable this endpoint
    :return: relayed response
    :return type: json
    """
    return requests.get(f"http://{ip}/{path}").json()


@app.get("/status")
def get_all_status():
    """
    Get all machines' status
    :return: a list of machines' status
    :return type: json
    """
    # return [{machine['ip_address']: requests.get(f"http://{machine['ip_address']}/api/v1/print_job/status", timeout=1).json()} for
    #         machine in machines]
    # multi processing version
    with multiprocessing.Pool(processes=len(machines)) as pool:
        results = pool.map(_multiprocessor_get_status, machines)
    with multiprocessing.Pool(processes=len(machines)) as pool:
        names = pool.map(_multiprocessor_get_name, machines)
    return [{"status": result, "name": name, "ip": machine["ip_address"]} for result, name, machine in
            zip(results, names, machines)]


@app.get("/status?ip={ip}")
def get_status(ip):
    """
    Get a machine's status
    :return: a machine's status
    :return type: json
    """
    return {"status": requests.get(f"http://{ip}/api/v1/print_job/status").json(),
            "name": requests.get(f"http://{ip}/api/v1/system/name").json()}


@app.get("/printer")
def get_all_status():
    """
    Get all machines' status
    Warning: This could return a large amount of data
    :return: a list of machines' status
    :return type: json
    """
    # return [{machine['ip_address']:requests.get(f"http://{machine['ip_address']}/api/v1/printer").json()} for machine in machines]
    # multi processing version
    with multiprocessing.Pool(processes=len(machines)) as pool:
        results = pool.map(_multiprocessor_printer, machines)
    return results


@app.get("/printer?ip={ip}")
def get_status(ip):
    """
    Get a machine's status
    :return: a machine's status
    :return type: json
    """
    return requests.get(f"http://{ip}/api/v1/print_job/status").json()


@app.get("/index.html")
def index_html():
    """
    Send the index.html file
    :return: a machine's status
    :return type: json
    """
    return fastapi.responses.FileResponse("index.html")


@app.get("/printer_ips")
def return_printer_ip_simplified():
    """
    Return a list of printer ips
    :return: a list of printer ips
    :return type: json
    """
    return [machine['ip_address'] for machine in machines]


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
