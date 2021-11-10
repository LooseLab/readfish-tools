readfish-tools
--------

[![Build](https://github.com/LooseLab/swordfish/actions/workflows/main.yml/badge.svg)](https://github.com/LooseLab/swordfish/actions/workflows/main.yml/badge.svg)
<!-- [![PyPI](https://img.shields.io/pypi/v/swordfish)](https://pypi.org/p/swordfish) -->

readfish-tools is a suite of command line utilities to ease the set up and analysis of readFish experiments.


Installation
===

```bash
pip install rf_tools
```

or

```bash
git clone https://github.com/LooseLab/rf_tools
cd rf_tools
python3 -m venv venv
source venv/bin/activate
pip install -U pip setuptools wheel
pip install -e .
```

Usage
===
```bash
usage: rf_tools [-h] {setup,update} ...

rf_tools suite

optional arguments:
  -h, --help      show this help message and exit

subcommands:
  {setup,update}  additional help
    setup         create a simple barcode based deplete/enrich experiment TOML.
    update        Update an existing simple toml file by removing or adding barcodes.
```

##Subcommands
###Setup - Interactively create a TOML file for running a read fish barcoding experiment. 


    usage: rf_tools setup [-h] --toml TOML [--no-minknow] [--mk-host MK_HOST] [--mk-port MK_PORT] [--use_tls]
                      [--adventure]

    optional arguments:
      -h, --help         show this help message and exit
      --toml TOML        Path to the TOML file.
      --no-minknow       Do not attempt to use the minknow API, default False.
      --mk-host MK_HOST  Address for connecting to MinKNOW, default localhost.
      --mk-port MK_PORT  Port for connecting to MinKNOW, default 9501.
      --use_tls          Use TLS for connecting to MinKNOW, default False.
      --adventure        How about a little light role play?

The toml argument is required, as this is the path to write the toml file to. An example command would be:

    rf_tools setup --toml example_test.toml

###Update - Interactively update an existing toml file to create a .toml_live file, to update a readfish barcoding experiment mid run.

    usage: rf_tools update [-h] --toml TOML

    optional arguments:
      -h, --help   show this help message and exit
      --toml TOML

Toml argument is required, as this is the TOML file to update.
An example command would be 
   
    rf_tools update --toml example_test.toml
