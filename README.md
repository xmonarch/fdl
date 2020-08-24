# fdl

fdl (`f`ollow `d`ocker `l`ogs) is a rather simple python application that allows a user to tail logs of a docker container by executing `docker logs -f`. 
It however continues to run when the container is stopped/restarted/re-created - once the container is back online 
new log entries are printed to the screen.

## Installation

`$ git clone https://github.com/xmonarch/fdl.git`

`$ cd fdl`

`$ sudo pip install .`

## Usage

As simple as:

`$ fdl my_docker_container_name`

For more details run:

`$ fdl --help`

## TODO

- provide docker name autocomplete bash/zsh/fish
