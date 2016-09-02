# -*- coding:utf-8 -*-

import maya.cmds as cmds
from datetime import datetime
from cStringIO import StringIO
import socket
import marshal
import base64
import types
import json
import sys
import os


def Singleton(cls):
	instances = {}
	def Instance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return Instance

@Singleton
class PointA(object):
	"""docstring for Transmitter"""
	def __init__(self):
		self.host = ''
		self.port = 0
		self.buff = 8192
		self.beam = 'socket object'

	def setCoord(self, port, host= None):
		"""	Set channel address	"""
		self.host = host if host else '127.0.0.1'
		self.port = port

	def connTest(self):
		""" connection test """
		self.cmdSend('print "[ ! ] This is a test."')

	def cmdSend(self, msg, silent= None):
		""" Sending cmd msg """
		if len(msg) <= self.buff:
			if not silent:
				self.profileA(msg)
			try:
				self.beam = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.beam.connect((self.host, self.port))
			except socket.error, er:
				cmds.error('Connection Failed. ' \
					+ 'Error code: %s Error Message: %s' % (str(er[0]),er[1]))
				return None
			else:
				self.beam.send(msg)
				# get recv
				re = self.recvall()
		else:
			self.sendall(longMsg= msg)
			msg = "global mTeleport_buffer\n" \
				+ "exec(mTeleport_buffer)"
			re = self.cmdSend(msg)
		return re

	def funcSend(self, func, *args, **kwargs):
		"""
		@Param
		func : function to send
		args : function input args
		kwargs : [mod] the code string for modules needs to be imported
				 ex: mod = '''
				 			import pymel.core as pm
				 			from datetime import datetime
				 			''' 
		"""
		nam = func.__name__
		doc = func.__doc__
		doc = json.dumps(doc.rstrip('\n\t') if doc else '')
		# because of json made boolean value lowercase,
		# convert args tuple to string before json dumps
		arg = json.dumps(str(args))
		mod = json.dumps(kwargs['mod'].strip()) if kwargs.has_key('mod') else ''
		tf = marshal.dumps(func.func_code)
		tf = base64.b64encode(tf)
		msg = "# Teleporting Python Function\n" \
			+ "print 'Function Name : %s'\n" % nam \
			+ "print 'Function Docs : %%s' %% %s\n" % doc \
			+ "print 'Function Args : %%s' %% %s\n" % arg \
			+ "print '= '*20\n" \
			+ "import marshal, types;import maya.cmds as cmds;" \
			+ "tf= marshal.loads('" + tf + "'.decode('base64'));" \
			+ "teleFunc = types.FunctionType(tf, globals(), 'teleFunc');" \
			+ "exec(%s, globals());" % mod \
			+ "result = teleFunc(%s);" % arg[2:-2] \
			+ "cmds.optionVar(sv= ('teleFuncResult', str(result)))"
		self.cmdSend(msg)
		# retrieve result
		msg = "cmds.optionVar(q= 'teleFuncResult')"
		result = self.cmdSend(msg, True)
		return result

	def sendall(self, filePath= None, longMsg= None, postFunc= None, *args, **kwargs):
		""" Send file as string split by half of buffer size due to encoding
		besause @postFunc is using [funcSend] to send a function after package,
		it's execute result will override the result of the func in package.
		"""
		# a global var as buffer: mTeleport_buffer
		msg = "global mTeleport_buffer; mTeleport_buffer= ''"
		self.cmdSend(msg, True)
		# image to string
		if filePath is not None:
			package = open(filePath, 'r')
		else:
			package = StringIO(longMsg)
		# sending
		try:
			success = False
			fixBuff = max(4, self.buff / 2)
			msg = "global mTeleport_buffer\n" \
				+ "mTeleport_buffer += '%s'.decode('base64')\n"
			while True:
				pString= package.read(fixBuff)
				if not pString:
					break
				# encode segment
				pak = msg % base64.b64encode(pString)
				self.cmdSend(pak, True)
			success = True
		except:
			cmds.error('Failed to send all.')
		package.close()
		# post function
		if postFunc and success:
			result = self.funcSend(postFunc, *args, **kwargs)
			return result
		return None

	def recvall(self):
		"""
		"""
		nextdata = self.beam.recv(self.buff)
		if nextdata is None:
			return None
		re = nextdata.rstrip('\x00')
		if len(re) == 0:
			return None
		oldtimeout = self.beam.gettimeout()
		self.beam.settimeout(1.5)
		while len(nextdata) >= self.buff:
			try:
				nextdata = self.beam.recv(self.buff)
				re += nextdata
			except socket.timeout:
				break
		self.beam.settimeout(oldtimeout)
		self.beam.close()
		if re.endswith('\n\x00'):
			re = re[:-2]
		return re

	def profileA(self, msg):
		msg = 'print " \\n" + ' \
			+ '"+ "*20 + "\\n" + ' \
			+ '"%s\\n" + ' % self.getTime() \
			+ '"@ %s\\n" + ' % os.environ['username'] \
			+ '"Sent from %s\\n" + ' % os.environ['computername'] \
			+ '"MAYA PID: %s\\n" + ' % os.getpid() \
			+ '"CMD:\\n" + ' \
			+ json.dumps(msg) + ' + "\\n" + ' \
			+ '"- "*20'
		self.cmdSend(msg, True)

	def getTime(self, sh= None):
		dFormat_L = '%A, %d. %B %Y %I:%M%p'
		dFormat_S = '%I:%M%p'
		return datetime.now().strftime(dFormat_S if sh else dFormat_L)
