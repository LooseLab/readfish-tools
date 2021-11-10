"""Command line entry point into RF tools"""
import sys
import argparse
import logging
import signal
from pathlib import Path
import pkg_resources  # part of setuptools

from rich.logging import RichHandler

from rf_tools.toml_setup import barcoding_adventure, update_barcoding_adventure
from rf_tools.utils import print_args

version = pkg_resources.require("rf_tools")[0].version
parser = argparse.ArgumentParser(description="rf_tools suite")

subparsers = parser.add_subparsers(dest='subparser_name', title='subcommands', help='additional help')

parser_setup = subparsers.add_parser("setup", help="create a simple barcode based deplete/enrich experiment TOML.")
parser_setup.set_defaults(func=barcoding_adventure)
parser_setup.add_argument("--toml", type=Path, help="Path to the TOML file.", required=True)
parser_setup.add_argument("--no-minknow", action="store_true", default=False, help="Do not attempt to use the minknow API")
parser_setup.add_argument(
    "--mk-host", default="localhost", help="Address for connecting to MinKNOW",
)
parser_setup.add_argument(
    "--mk-port", default=9501, help="Port for connecting to MinKNOW",
)
parser_setup.add_argument(
    "--use_tls", action="store_true", help="Use TLS for connecting to MinKNOW",
)
parser_setup.add_argument(
    "--adventure", action="store_true", help="How about a little light role play?", default=False
)

parser_update = subparsers.add_parser("update", help="Update an existing simple toml file by removing or adding barcodes.")
parser_update.set_defaults(func=update_barcoding_adventure)
parser_update.add_argument("--toml", required=True, type=Path)


def signal_handler(signal, frame):
    print(" Caught Ctrl+C, exiting.", file=sys.stderr)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main(args=None):
    args = parser.parse_args(args=args)
    handler = RichHandler()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info(f"Welcome to rf_tools version {version}. How may we help you today?")
    print_args(args, logger=logger, exclude={"mt_key"})
    # Check TOML file
    # Call monitor module
    if args.subparser_name:
        args.func(args, version)
    else:
        parser.parse_args("--help")


