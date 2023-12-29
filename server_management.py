"""
    This file contains the implementation of a ServerManagement class for managing the server process.
    It provides methods for starting and stopping the server.

    Author: Hendrik Siemens
    Date: December 29, 2023
"""

import argparse
import os
import sys
import signal
import subprocess
import time

PYTHON_PATH = '/usr/bin/python3'
BASE_PATH = '/home/hendrik/Trainex-aber-besser'
APP_PATH = f'{BASE_PATH}/app.py'
PID_FILE = f'{BASE_PATH}/server_management/pid/server.pid'
ERROR_LOG = f'{BASE_PATH}/server_management/error.log'


class ServerManagement:
    """
    Class for managing the server process.

    Methods:
    - start_server: Starts the server process.
    - stop_server: Stops the server process.
    """
    def __init__(self) -> None:
        pass

    def start_server() -> None:
        """
        Starts the server if it is not already running.

        This function checks if the server is already running by checking the existence of a PID file.
        If the server is not running, it starts the server process and writes the process ID to the PID file.

        Raises:
            Exception: If there is an error starting the server.

        """
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

    def stop_server() -> None:
        """
        Stops the server if it is running.
        
        This function checks if the server is running by checking the existence of a PID file.
        If the server is running, it stops the server process and deletes the PID file.
        
        Raises:
            Exception: If there is an error stopping the server.
        
        """
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


def parse_arguments() -> argparse.Namespace:
    """
    Parses the command line arguments for the Server Management Tool.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description='Server Management Tool',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-s', '--start', nargs='?', const='server', metavar='SERVICE',
                        default=None, help=('Starts a specified service.\n'
                                            'Usage:\n'
                                            '-s [service_name] or --start [service_name]\n'
                                            'If no service name is provided, defaults to "server".\n'
                                            'Example: --start server'))

    parser.add_argument('-st', '--stop', nargs='?', const='server', metavar='SERVICE',
                        default=None, help=('Stops a specified service.\n'
                                            'Usage:\n'
                                            '-st [service_name] or --stop [service_name]\n'
                                            'If no service name is provided, defaults to "server".\n'
                                            'Example: --stop server'))

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    if args.start == 'server':
        ServerManagement.start_server()
    elif args.stop == 'server':
        ServerManagement.stop_server()
    else:
        print(parse_arguments().format_help())