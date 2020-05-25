![Python package](https://github.com/sensein/cmixf/workflows/Python%20package/badge.svg?branch=master)

# cmixf

A library to parse [CMIXF-12](https://people.csail.mit.edu/jaffer/MIXF/CMIXF-12).

This will install a CLI `cmixf` when installed.

At present this assumes that a number is provided before any unit.

## For users:

```
$ pip install cmixf # requires a python 3 environment 
$ cmixf
cmixf > 1mV
type='REAL', value='1'
type='SUBMULTIB', value='mV'
1mV
cmixf > 1oC
type='REAL', value='1'
type='UNITC', value='oC'
1oC
cmixf > <Ctrl+D to exit>
```

If it fails it will raise an error and exit. 

```
$ cmixf
cmixf > 1mM
type='REAL', value='1'
type='UNITC', value='m'
Traceback (most recent call last):
  File "/Users/satra/software/miniconda3/envs/mixf/bin/cmixf", line 11, in <module>
    load_entry_point('cmixf', 'console_scripts', 'cmixf')()
  File "/Users/satra/software/sensein/cmixf/cmixf/parser.py", line 217, in main
    for tok in lexer.tokenize(text):
  File "/Users/satra/software/miniconda3/envs/mixf/lib/python3.8/site-packages/sly/lex.py", line 443, in tokenize
    tok = self.error(tok)
  File "/Users/satra/software/sensein/cmixf/cmixf/parser.py", line 54, in error
    raise ValueError("Line %d: Bad character %r" % (self.lineno, t.value[0]))
ValueError: Line 1: Bad character 'M'
```

## For developers:

After cloning the repo do:

1. pip install -e .[dev]
2. pre-commit install
