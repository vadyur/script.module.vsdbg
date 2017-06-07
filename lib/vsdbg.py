class Settings(object):
	_debug = True
	_host='localhost'
	_copy_to_clip=True
	_save_to_file=False
	_path = None

	def __init__(self, addon=None):
		try:
			import xbmcaddon
		except ImportError:
			return

		if not addon:
			addon = xbmcaddon.Addon(id='script.module.vsdbg')
		self._debug = addon.getSetting('enable') != 'false'

		self._copy_to_clip = addon.getSetting('copy_to_clipboard') != 'false'
		self._save_to_file = addon.getSetting('save_to_file') != 'false'
		if self._save_to_file:
			self._path = addon.getSetting('file_path')

		self._host = addon.getSetting('host')

s = Settings()

import ptvsd
import subprocess

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

def read_from_clipboard():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

def _attach(wait=True):
	if not s._debug:
		return False

	import random, os
	port = random.randint(6600, 6800)

	ptvsd.enable_attach(secret = None, address = ('0.0.0.0', port))

	cmd = "tcp://%s:%d" % (s._host, port)

	if s._copy_to_clip:
		import platform

		if platform.system() == 'Windows':
			os.system('echo ' + cmd + '| clip')
		elif platform.system() == 'Darwin':
			write_to_clipboard(cmd)
		else:
			print platform.system() + ' no detect, cmd = ' + cmd

	if s._save_to_file:
		import xbmcvfs
		f = xbmcvfs.File(os.path.join(s._path, 'qualifier.txt'), 'w')
		f.write(cmd)
		f.close()

	if wait:
		ptvsd.wait_for_attach()

	return True


def _bp(wait=True):
	if not ptvsd.is_attached():
		_attach(wait)

	ptvsd.break_into_debugger()