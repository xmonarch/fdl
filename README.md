# fdl

fdl (`f`ollow `d`ocker `l`ogs) is a rather simple python application that allows a user to tail logs of a docker container by executing `docker logs -f`. 
It however continues to run when the container is stopped/restarted/re-created - once the container is back online 
new log entries are printed to the screen.

## Installation

```shell
$ git clone https://github.com/xmonarch/fdl.git
$ cd fdl
$ sudo pip install .
```

## Usage

As simple as:
```shell
$ fdl my_docker_container_name
```

Or instead tail specific files in the container (requires `tail` to be available in the container):
```shell
$ fdl my_docker_container_name /var/log/somelogfile.log /var/log/someotherlogfile.log
``` 

For more details run:
```shell
$ fdl --help
```
