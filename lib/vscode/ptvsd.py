# ptvsd wrapper for debugpy

import os
from os.path import expanduser, join
home = expanduser("~")

def find_all_dirs(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for d in sorted(dirs):
            if pattern in d:
                result.append(join(root, d))
    return result

def find_python_libs_directory():
    # .vscode/extensions/ms-python.python-2020.8.101144/pythonFiles/lib/python/debugpy
    result = join(home, '.vscode', 'extensions')
    candidates = find_all_dirs('ms-python.python', result)
    if candidates:
        result = join(result, candidates[-1], 'pythonFiles', 'lib', 'python')
    return result

sys.path.insert(0, find_python_libs_directory())
import debugpy

break_into_debugger = debugpy.breakpoint
debug_this_thread = debugpy.debug_this_thread
is_attached = debugpy.is_client_connected

def enable_attach(address, *args, **kwargs):
    debugpy.listen(address)

wait_for_attach = debugpy.wait_for_client