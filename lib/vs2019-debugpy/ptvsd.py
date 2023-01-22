# ptvsd wrapper for debugpy

import os, sys
from os.path import join

home = r'{PF86}\Microsoft Visual Studio\2019\Community\Common7\IDE\Extensions\Microsoft\Python\Core' \
        .format(PF86=os.environ['ProgramFiles(x86)'])

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

sys.path.insert(0, home)
import debugpy

break_into_debugger = debugpy.breakpoint
debug_this_thread = debugpy.debug_this_thread
is_attached = debugpy.is_client_connected

def enable_attach(address, *args, **kwargs):
    # import web_pdb
    # web_pdb.set_trace()

    import xbmc
    xbmc.log('enable_attach!!!')

    debugpy.configure(subProcess=False, python=r"{LAD}\Microsoft\WindowsApps\python.exe".format(LAD=os.environ['LOCALAPPDATA']))
    debugpy.listen(address)

wait_for_attach = debugpy.wait_for_client
