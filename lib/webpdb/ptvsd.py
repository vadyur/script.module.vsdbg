# ptvsd wrapper for webpdb

import web_pdb

break_into_debugger = web_pdb.set_trace
def is_attached():
    return True

def enable_attach(address, *args, **kwargs):
    pass

def wait_for_attach():
    pass