import importlib.util
import logging

from typing import Union
from pathlib import Path
from .app import app, CHECKERS

LOGGER = logging.getLogger(__file__)

def import_path(name: str, file_path: Union[str, Path]):
    if isinstance(file_path, Path):
       file_path = str(file_path)
    spec = importlib.util.spec_from_file_location(name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if __name__ == "__main__":
    import uvicorn
    import argparse

    parser = argparse.ArgumentParser(Path(__file__).name)
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--log-level", choices=["debug", "info", "warning", "error"], default="info")
    parser.add_argument("--check", action="append", required=True)
    args = parser.parse_args()

    for i, check_path in enumerate(args.check):
        m = import_path(f"check{i:03}", check_path)
        try:
            m.register_checkers(CHECKERS)
        except AttributeError:
            try:
                m.registerCheckers(CHECKERS)
            except AttributeError:
                raise Exception(f"Failed to register checkers for '{check_path}'.")

    config = uvicorn.Config(app, host=args.host, port=args.port, log_level=args.log_level)
    for checker in CHECKERS:
        LOGGER.info(f"{checker}")
    server = uvicorn.Server(config)
    server.run()
