# fdlogs

fdlogs (`f`ollow `d`ocker `logs`) is a rather simple python application that allows a user to tail logs of a docker container by executing `docker logs -f`. 
It however continues to run when the container is stopped/restarted/re-created - once the container is back online 
new log entries are printed to the screen.

## Installation

`$ git clone https://github.com/xmonarch/fdlogs.git`

`$ cd fdlogs`

`$ sudo pip install .`

## Usage

As simple as:

`$ fdlogs my_docker_container_name`

For more details run:

`$ fdlogs --help`
