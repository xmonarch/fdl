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
$ fdl con1
```

Or instead tail specific files in the container (requires `tail` to be available in the container):
```shell
$ fdl con1:~/log1.log:/tmp/log2.log
``` 

It's possible to follow logs from multiple containers (also combined with files from those containers):
```shell
$ fdl con1 con2:~/log1.log:/tmp/log2.log con3
```

In order to add a custom alias for container use the following syntax:
```shell
$ fdl a/con1 b/con2 c/con3
```

For more details run:
```shell
$ fdl --help
```
