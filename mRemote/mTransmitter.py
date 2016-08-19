# -*- coding:utf-8 -*-

from pymel.core import *
import maya.OpenMaya as api
import maya.OpenMayaUI as apiUI
from datetime import datetime
import socket
import base64
import sys, os


def Singleton(cls):
	instances = {}

	def Instance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return Instance

@Singleton
class MTransmitter(object):
	"""docstring for MTransmitter"""
	def __init__(self):
		self.conn = None
		self.host = ''
		self.port = 0
		self.buff = 4096

	def setAddr(self, port, host= None):
		"""	Set channel address	"""
		self.host = host if host else 'localhost'
		self.port = port

	def connTest(self):
		""" connection test """
		self.cmdSend('print "[ ! ] This is a test."')

	def cmdSend(self, msg, silent= None):
		""" Sending cmd msg """
		try:
			self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.conn.connect((self.host, self.port))
		except socket.error, msg:
			error('Connection Failed. ' \
				+ 'Error code: %s Error Message: %s' % (str(msg[0]),msg[1]))
			return None
		else:
			self._knockknock() if not silent else None
			self.conn.send(msg)
			try:
				recv = self.conn.recv(self.buff)
			except socket.error, msg:
				error('Connection Failed. ' \
					+ 'Error code: %s Error Message: %s' % (str(msg[0]),msg[1]))
				self.conn.close()
				return None
			else:
				print 'yyyyy'
				self.conn.close()
				return recv

	def msgSend(self, msg):
		""" Sending chat msg """
		uid = self._getUser().rjust(8, ' ')
		dtm = self._getTime(1)
		msg = 'print "%s | %s : %s"' % (dtm, uid, msg)
		return self.cmdSend(msg, True)

	def imgSend(self):
		""" Sending viewport snapshot """
		imgPath = os.environ['tmpdir'] + '/mRSnapShot_Send.jpg'
		# take snapshot
		view = apiUI.M3dView.active3dView()
		snapShot = api.MImage()
		view.readColorBuffer(snapShot, True)
		snapShot.writeToFile(imgPath, 'jpg')
		self._fileTrans(imgPath)
		# build cmd for save and open image
		msg = "imgPath = os.environ['tmpdir'] + '/mRSnapShot_Grab.jpg'\n" \
			+ "global mRemote_buffer\n" \
			+ "fh = open(imgPath, 'w')\n" \
			+ "fh.write(mRemote_buffer)\n" \
			+ "fh.close()\n" \
			+ "mel.eval('RenderViewWindow')\n" \
			+ "rview = cmds.getPanel(sty= 'renderWindowPanel')\n" \
			+ "cmds.renderWindowEditor(rview, e= True, li= imgPath)\n" \
			+ "print 'Snapshot send.'"
		return self.cmdSend(msg)

	def _fileTrans(self, filePath):
		""" Send file as string split by 512 """
		msg = "global mRemote_buffer; mRemote_buffer= ''"
		self.cmdSend(msg, True)
		# image to string
		package = open(filePath, 'r')
		while True:
			pString = package.readline(512)
			if not pString:
				break
			pString = base64.b64encode(pString)
			# build cmd for trans string part
			msg = "global mRemote_buffer\n" \
				+ "mRemote_tmp = '%s'\n" % pString \
				+ "mRemote_buffer += mRemote_tmp.decode('base64')"
			self.cmdSend(msg, True)
		package.close()

	def _knockknock(self):
		cid = self._getHost()
		uid = self._getUser()
		pid = self._getPID()
		dtm = self._getTime()
		msg = 'print " \\n" + ' \
			+ '"+ "*20 + "\\n" + ' \
			+ '"%s\\n" + ' % dtm \
			+ '"@ %s\\n" + ' % uid \
			+ '"Sent from %s\\n" + ' % cid \
			+ '"MAYA PID: %s\\n" + ' % pid \
			+ '"- "*20'
		result = self.cmdSend(msg, True)
		cmds.pause(sec= 1)
		return result

	def _getUser(self):
		return os.environ['username']

	def _getHost(self):
		return os.environ['computername']

	def _getPID(self):
		return os.getpid()

	def _getTime(self, sh= None):
		dFormat = '%A, %d. %B %Y %I:%M%p'
		if sh:
			dFormat = '%I:%M%p'
		return datetime.now().strftime(dFormat)
