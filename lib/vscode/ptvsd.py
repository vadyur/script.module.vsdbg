# ptvsd wrapper for debugpy

import os, sys
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

def launch_server(argv):
    #import web_pdb
    #web_pdb.set_trace()

    import os
    os.name = 'kodi'

    from debugpy.adapter.__main__ import main, _parse_argv
    main(_parse_argv(argv))

    os.name = name


class MyPopen:
    def __init__(self, *args, **kwargs):
        import json
        from debugpy.adapter.__main__ import main, _parse_argv
        argv = args[0][1:]
        import xbmc
        this_script = 'special://home/addons/script.module.vsdbg/lib/vscode/ptvsd.py'
        params = ','.join(argv)
        xbmc.executebuiltin('RunScript({},launch_server,{})'.format(this_script, params))

    def wait(self):
        #import web_pdb
        #web_pdb.set_trace()
        import time
        time.sleep(1)

def enable_attach(address, *args, **kwargs):
    #import web_pdb
    #web_pdb.set_trace()

    import xbmc
    xbmc.log('enable_attach!!!')

    import subprocess

    _Popen = subprocess.Popen

    subprocess.Popen = MyPopen

    #debugpy.configure(subProcess=False)
    debugpy.listen(address)

    subprocess.Popen = _Popen

wait_for_attach = debugpy.wait_for_client

if __name__ == '__main__':
    if 'launch_server' in sys.argv:
        import xbmc
        xbmc.log(str(sys.argv))
        pos = sys.argv.index('launch_server')
        argv = sys.argv[pos+1:]
        xbmc.log(str(argv))

        launch_server(argv)