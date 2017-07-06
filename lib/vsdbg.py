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
		self._version = addon.getSetting('version')

s = Settings()

#import ptvsd31 as ptvsd
import sys, os
cur = os.path.dirname(__file__)
path = os.path.join(cur, s._version)
sys.path.insert(0, os.path.normpath(path))

import ptvsd

import subprocess, os

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))

def read_from_clipboard():
    return subprocess.check_output(
        'pbpaste', env={'LANG': 'en_US.UTF-8'}).decode('utf-8')

def get_tb():
	import traceback, xbmc
	st = traceback.extract_stack(limit=5)

	for filename, lineno, name, line in reversed(st):
		if 'vsdbg' not in filename:
			filename = os.path.relpath(filename, xbmc.translatePath('special://home/addons')).replace('\\', '/')
			item = '  File "%s", line %d' % (filename, lineno)
			return item
	return ''

def need_to_debug(cmd=''):
	import xbmcgui
	dlg = xbmcgui.Dialog()

	line = 'Debug Script?'
	if cmd:
		line += ' Qualifier is: {0}.'.format(cmd)

	line += '\n' + get_tb()

	res = dlg.yesno('Python tools for Visual Studio debug', line, yeslabel='Break', nolabel='Continue', autoclose=15000)

	return res

def _attach(wait=True):
	if not s._debug:
		return False

	import random, os
	port = random.randint(6600, 6800)

	cmd = "tcp://vsdbg@%s:%d" % (s._host, port)

	if not need_to_debug(cmd):
		return False

	ptvsd.enable_attach(secret = 'vsdbg', address = ('0.0.0.0', port))

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
		if _attach(wait):
			ptvsd.break_into_debugger()
	else:
		if need_to_debug():
			ptvsd.break_into_debugger()
