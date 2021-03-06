import logging
import subprocess
import sys
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


def monitor(args):
    """
    Continuously display logs from the selected docker container.
    - When the container is running the output is printed to the terminal.
    - When container is stopped the script will wait until it's back online.
    - When the container is restarted the script will hide the lines of output that were already displayed.
    :param args: CLI arguments
    """
    logging.basicConfig(level=args.log_level, stream=sys.stdout, datefmt="%Y-%m-%d %H:%M:%S",
                        format="[%(asctime)s] %(levelname)s %(name)s %(message)s")
    log = logging.getLogger("fdl")

    try:
        waiting_for_online = False
        container_id: str = ''
        while True:
            new_container_id = check(args.container_name)
            if new_container_id:
                if container_id:
                    if new_container_id == container_id:
                        log.log(logging.INFO,
                                f"re-connected to container: [{container_id[:12]}]")
                    else:
                        log.log(logging.INFO,
                                f"observed container id change: [{container_id[:12]}] -> [{new_container_id[:12]}]")
                container_id = new_container_id

                waiting_for_online = False

                if len(args.file) > 0:
                    log.log(logging.INFO,
                            f"tailing {':'.join(args.file)} in \"{args.container_name}\" [{container_id[:12]}]")
                else:
                    log.log(logging.INFO, f"following container \"{args.container_name}\" [{container_id[:12]}]")

                for line in follow(args.container_name, args.file):
                    print(line.decode(), file=sys.stdout, flush=True, end='')
            else:
                if not waiting_for_online:
                    log.log(logging.WARNING, f"waiting for container \"{args.container_name}\" to become active...")
                waiting_for_online = True
                time.sleep(args.interval)
    except KeyboardInterrupt:
        sys.exit(0)


def run():
    """
    Parse CLI arguments and start monitoring for docker container logs
    """
    parser = argparse.ArgumentParser(description="Follow docker container logs and survive restarts")
    parser.add_argument('-v', '--version', action='version', version=pkg_resources.require("fdl")[0].version)
    parser.add_argument("-q",
                        "--quiet",
                        dest="log_level",
                        help="disable logging",
                        action="store_const",
                        default=logging.INFO,
                        const=logging.CRITICAL)
    parser.add_argument("-i",
                        "--interval",
                        dest="interval",
                        help="interval used for waiting for container to become active",
                        action="store",
                        type=int,
                        default=1)
    parser.add_argument("container_name",
                        help="name of the docker container to obtain logs from")
    parser.add_argument("file",
                        nargs="*",
                        help="optionally a list of files to tail in the container")

    monitor(parser.parse_args(sys.argv[1:]))
