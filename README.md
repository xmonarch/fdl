# fdl

fdl (`f`ollow `d`ocker `l`ogs) is a rather simple python application that allows a user to tail logs of a docker container by executing `docker logs -f`. 
It however continues to run when the container is stopped/restarted/re-created - once the container is back online 
new log entries are printed to the screen.

## Installation

```shell
$ git clone https://github.com/xmonarch/fdl.git
$ cd fdl
$ pip install --user .
```

## Usage

As simple as:
```shell
$ fdl my_docker_container_name
```

Or instead tail specific files in the container (requires `tail` to be available in the container):
```shell
$ fdl my_docker_container_name:/var/log/somelogfile.log:/var/log/someotherlogfile.log
``` 

It's possible to follow logs from multiple containers (also combined with files from those containers):
```shell
$ fdl my_docker_container_name1 my_docker_container_name2:/var/log/somelogfile.log:/var/log/someotherlogfile.log my_docker_container_name3
```

In order to add a custom alias for container use the following syntax:
```shell
$ fdl alias/my_docker_container_name1:/var/log/somelogfile.log:/var/log/someotherlogfile.log
```

For more details run:
```shell
$ fdl --help
```
