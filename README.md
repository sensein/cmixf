![Python package](https://github.com/sensein/cmixf/workflows/Python%20package/badge.svg?branch=master)

# cmixf

A library to parse [CMIXF-12](https://people.csail.mit.edu/jaffer/MIXF/CMIXF-12).

## For users:

To install from PyPi.

```
$ pip install cmixf 
```

This will install a command line interface called `cmixf`.

```
$ cmixf --help
Usage: cmixf [OPTIONS] [TEXT]...

Options:
  -d, --debug  Turn on token debugging
  --help       Show this message and exit.
```

At present this assumes that a number is provided before any unit. To better 
understand which characters are erroneous you can turn on the debug flag.

1. Without debugging on:

```
$ cmixf
cmixf (Ctrl+d to quit) > 1mV
1mV
cmixf (Ctrl+d to quit) > 1oC
1oC
cmixf (Ctrl+d to quit) > 1mM
FAILED:  Line 1: Bad character 'M'
cmixf (Ctrl+d to quit) > 
```

2. With debugging turned on:

```
$ cmixf --debug
cmixf (Ctrl+d to quit) > 1mM
type='REAL', value='1'
type='UNITC', value='m'
FAILED:  Line 1: Bad character 'M'
cmixf (Ctrl+d to quit) > 
```

## For developers:

After cloning the repo do:

1. pip install -e .[dev]
2. pre-commit install
