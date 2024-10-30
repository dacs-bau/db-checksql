import sys
import uvicorn
import argparse

import importlib.util
import logging

from typing import Union
from pathlib import Path
from .app import app, CHECKERS

LOGGER = logging.getLogger(__file__)

LOG_LEVEL = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}

def import_path(name: str, file_path: Union[str, Path]):
    if isinstance(file_path, Path):
       file_path = str(file_path)
    spec = importlib.util.spec_from_file_location(name, file_path)
    if spec is None:
        raise ModuleNotFoundError()

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if __name__ == "__main__":
    parser = argparse.ArgumentParser(Path(__file__).name)
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--log-level", choices=["debug", "info", "warning", "error"], default="info")
    parser.add_argument("checkers", type=Path, nargs="+")
    args = parser.parse_args()

    # Configure logging before anything else.
    logging.basicConfig(format='{levelname:7} {message}', style='{', level=LOG_LEVEL[args.log_level])

    for i, check_path in enumerate(args.checkers):
        check_path = check_path.absolute()

        # Load checks as module
        try:
            m = import_path(f"check{i:03}", check_path)
        except ModuleNotFoundError:
            LOGGER.error(f"Failed to load file '{check_path}.")
            sys.exit(-1)

        # Register checkers
        for pset, pid, checker in m.get_checkers():
            key = (pset, pid)
            if key in CHECKERS:
                LOGGER.warning(f"[pset={pset}, pid={pid}] Replacing checker with one found in '{check_path}'.")
            else:
                LOGGER.info(f"[pset={pset}, pid={pid}] Registering checker found in '{check_path}'.")
            CHECKERS[key] = checker

    config = uvicorn.Config(app, host=args.host, port=args.port, log_config=None)
    server = uvicorn.Server(config)
    server.run()
