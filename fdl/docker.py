import os
import subprocess
import sys
import textwrap
import threading
import time
import argparse
from typing import List

import pkg_resources


def check(container_name: str) -> str:
    """
    Check if docker container is running and return container ID if it is
    :param container_name: name of the docker container
    :return: container ID or empty string if container with this name is not running
    """
    return subprocess.run(
        ["docker", "ps", "--no-trunc", "--filter", f'name=^/{container_name}$', "--format", "{{.ID}}"],
        capture_output=True).stdout.decode().strip()


def follow(container_name: str, file: List[str] = None):
    """
    Issue a 'docker logs -f' for our container and continue yielding lines of output until the container is running
    :param container_name: name of the docker container
    :param file: optionally a list of files to tail instead of docker logs
    """
    if file:
        command = ["docker", "exec", container_name, "tail", "-q", "-n", "0", "-F", *file]
    else:
        command = ["docker", "logs", "-f", container_name, "-n", "0"]
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        return_code = p.poll()
        line = p.stdout.readline()
        yield line
        if return_code is not None:
            break


def monitor_container(interval: int, name: str, alias: str, separator: str, files: List[str] = None):
    """
    Continuously display logs from the selected docker container.
    - When the container is running the output is printed to the terminal.
    - When container is stopped the script will wait until it's back online.
    - When the container is restarted the script will hide the lines of output that were already displayed.
    :param interval: live check interval
    :param name: container name
    :param alias: alias to display in logs
    :param separator: alias/output separator
    :param files: optionally files to tail in the container
    """
    waiting_for_online = False
    container_id: str = ''
    while True:
        new_container_id = check(name)
        if new_container_id:
            if container_id:
                if new_container_id == container_id:
                    print(f'{alias}{separator}(Debug) re-connected to container {container_id[:12]}', file=sys.stdout,
                          flush=True)
                else:
                    print(f'{alias}{separator}(Debug) id change: [{container_id[:12]}] -> [{new_container_id[:12]}]',
                          file=sys.stdout, flush=True)
            container_id = new_container_id

            waiting_for_online = False
            if files and len(files) > 0:
                print(f'{alias}{separator}(Debug) tailing {":".join(files)} [{container_id[:12]}]', file=sys.stdout,
                      flush=True)
            else:
                print(f'{alias}{separator}(Debug) following [{container_id[:12]}]', file=sys.stdout, flush=True)

            for line in follow(name, files):
                line_d = line.decode()
                if len(line_d.strip()) > 0:
                    print(f'{alias}{separator}{line_d}', file=sys.stdout, flush=True, end='')
        else:
            if not waiting_for_online:
                print(f'{alias}{separator}(Error) container not running', file=sys.stdout, flush=True)
            waiting_for_online = True
            time.sleep(interval)


def monitor(args):
    """
    Start monitoring containers specified via CLI
    - figure out what to tail and aliases
    - start separate thread to monitor each container
    :param args: CLI arguments
    """
    containers = []
    max_alias_length: int = 0
    for container_name in args.container:
        files: List[str] = []
        if ':' in container_name:
            split = container_name.split(':')
            container_name = split[0]
            files = split[1:]
        alias = container_name

        if '/' in container_name:
            split = container_name.split('/')
            alias = split[0]
            container_name = split[1]
        containers.append(
            [container_name, alias.rjust(max_alias_length, ' ') if not args.no_labels else '',
             ' \u226b ' if not args.no_labels else '', files])

        if len(alias) > max_alias_length:
            max_alias_length = len(alias)

    threads: List[threading.Thread] = []
    try:
        for container in containers:
            thread = threading.Thread(target=monitor_container,
                                      args=(args.interval, container[0], container[1], container[2]))
            threads.append(thread)
            thread.start()
    except KeyboardInterrupt:
        sys.exit(0)


def run():
    """
    Parse CLI arguments and start monitoring for docker container logs
    """
    parser = argparse.ArgumentParser(description="Follow docker container logs and survive restarts")
    parser.add_argument('-v', '--version', action='version', version=pkg_resources.require("fdl")[0].version)
    parser.add_argument("-i",
                        "--interval",
                        dest="interval",
                        help="interval used for waiting for container to become active",
                        action="store",
                        type=int,
                        default=1)
    parser.add_argument("--no-labels",
                        dest="no_labels",
                        help="disable container labels in the output",
                        action="store",
                        type=bool,
                        default=False)
    parser.add_argument("container",
                        nargs="*",
                        help="name of the docker container to obtain logs from")

    monitor(parser.parse_args(sys.argv[1:]))
