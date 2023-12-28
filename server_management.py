import os
import signal
import subprocess
import time

PYTHON_PATH = '/usr/bin/python3'
BASE_PATH = '/home/hendrik/Trainex-aber-besser'
APP_PATH = f'{BASE_PATH}/app.py'
PID_FILE = f'{BASE_PATH}/server_management/pid/server.pid'
ERROR_LOG = f'{BASE_PATH}/server_management/error.log'


def start_server():
    if os.path.isfile(PID_FILE):
        print("Server is already running.")
        return

    try:
        server_process = subprocess.Popen(
            [PYTHON_PATH, APP_PATH], stderr=subprocess.PIPE)
        with open(PID_FILE, 'w') as f:
            f.write(str(server_process.pid))
    except Exception as e:
        with open(ERROR_LOG, 'a') as f:
            f.write(f"Error starting server: {str(e)}\n")
        raise


def stop_server():
    if os.path.isfile(PID_FILE):
        with open(PID_FILE, 'r') as f:
            pid = int(f.read())

        try:
            os.kill(pid, signal.SIGINT)
            time.sleep(5)  # Wait for the process to exit gracefully
        except ProcessLookupError:
            pass  # Process already exited

        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

        if os.path.exists('/proc/' + str(pid)):
            os.kill(pid, signal.SIGKILL)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'start':
            start_server()
        elif command == 'stop':
            stop_server()
        else:
            print(f"Unbekannter Befehl: {command}")
    else:
        print("Bitte gib einen Befehl an: 'start' oder 'stop'")
