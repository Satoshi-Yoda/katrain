import os
import sys
from typing import List, Tuple, TypeVar

try:
    import importlib.resources as pkg_resources
except:
    import importlib_resources as pkg_resources

T = TypeVar("T")


def var_to_grid(array_var: List[T], size: Tuple[int, int]) -> List[List[T]]:
    """convert ownership/policy to grid format such that grid[y][x] is for move with coords x,y"""
    ix = 0
    grid = [[]] * size[1]
    for y in range(size[1] - 1, -1, -1):
        grid[y] = array_var[ix : ix + size[0]]
        ix += size[0]
    return grid


def evaluation_class(points_lost: float, eval_thresholds: List[float]):
    i = 0
    while i < len(eval_thresholds) - 1 and points_lost < eval_thresholds[i]:
        i += 1
    return i


def check_thread(tb=False):  # for checking if draws occur in correct thread
    import threading

    print("build in ", threading.current_thread().ident)
    if tb:
        import traceback

        traceback.print_stack()


PACKAGE_PATH = None


def find_package_resource(path, silent_errors=False):
    global PACKAGE_PATH
    if path.startswith("katrain"):
        if PACKAGE_PATH is None:
            try:
                with pkg_resources.path("katrain", "__init__.py") as p:
                    PACKAGE_PATH = os.path.split(str(p))[0]
            except (ModuleNotFoundError, FileNotFoundError, ValueError) as e:
                print(f"Package file {path} not found, installation possibly broken", file=sys.stderr)
                return f"FILENOTFOUND/{path}"
        return os.path.join(PACKAGE_PATH, path.replace("katrain\\", "katrain/").replace("katrain/", ""))
    else:
        return os.path.abspath(os.path.expanduser(path))  # absolute path
