"""
Utilities for speaking with MinoTour
"""
import time

import toml
from grpc import RpcError
from minknow_api.manager import Manager
import logging
import sys

from rich.logging import RichHandler

# formatter = logging.Formatter(
#         "[%(asctime)s] %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
#     )
handler = RichHandler()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def print_args(args, logger=None, exclude=None):
    """Print and format all arguments from the command line"""
    if exclude is None:
        exclude = []
    dirs = dir(args)
    for attr in dirs:
        if attr[0] != "_" and attr not in exclude and attr.lower() == attr:
            record = "{a}={b}".format(a=attr, b=getattr(args, attr))
            if logger is not None:
                logger.info(record)
            else:
                print(record)


def write_toml_file(data, toml_file_path):
    """

    Parameters
    ----------
    data: dict
        the returned toml data from minoTour
    toml_file_path: pathlib.Path
        The file path to the Toml file to overwrite

    Returns
    -------
    None
    """
    if not str(toml_file_path).endswith("_live"):
        toml_file_path = f"{toml_file_path}_live"
    with open(toml_file_path, "w") as fh:
        toml.dump(data, fh)
    logger.info(f"Successfully updated toml file at {toml_file_path}")


def get_device(device, **kws):
    """Get gRPC device"""
    manager = Manager(**kws)
    for position in manager.flow_cell_positions():
        if position.name == device:
            return position
    raise RuntimeError(f"Could not find device {device}")


def get_barcode_kits(address, timeout=10000, names=False):
    """

    Parameters
    ----------
    address: address for guppy
    timeout: timeout in milliseconds
    names: bool
        Name the barcoding kit
    Returns
    -------

    """
    # Lazy load GuppyClient for now, we don't want to break this whole module if
    # it's unavailable
    try:
        from pyguppy_client_lib.client_lib import GuppyClient
        res, status = GuppyClient.get_barcode_kits(address, timeout)
        if status != GuppyClient.success:
            raise RuntimeError(f"{status}")
        if names:
            res = [barcode["kit_name"] for barcode in res]
        return res
    except RuntimeError as e:
        logger.error(f"Error fetching barcode kits for validation! {repr(e)} Proceeding with"
                     f" the provided kit without validation.")
        return []