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
		self.wrap = True

	def cmdSend(self, msg):
		""" Sending cmd msg """
		result = self._connect()
		if result == 0:
			if self.wrap:
				msg = self._msgWrap(msg)
			self.conn.send(msg)
			recv = self.conn.recv(1024)
			self.conn.close()
			return recv
		else:
			return result

	def msgSend(self, msg):
		""" Sending chat msg """
		wrap = self.wrap
		self.wrap = False
		uid = self._getUser().rjust(8, ' ')
		dtm = self._getTime(1)
		msg = 'print "%s | %s : %s"' % (dtm, uid, msg)
		self.cmdSend(msg)
		self.wrap = wrap

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

	def conTest(self):
		wrap = self.wrap
		self.wrap = True
		self.cmdSend('print "[ ! ] This is a test."')
		self.wrap = wrap
		
	def setAddr(self, port, host= None):
		"""	Set channel address	"""
		self.host = host if host else 'localhost'
		self.port = port

	def setWrap(self, doWrap= None):
		if doWrap:
			self.wrap = doWrap

	def _connect(self):
		try:
			self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.conn.connect((self.host, self.port))
		except socket.error, msg:
			error('Connection Failed. ' \
				+ 'Error code: %s Error Message: %s' % (str(msg[0]),msg[1]))
			return 1
		else:
			return 0

	def _fileTrans(self, filePath):
		""" Send file as string split by 512 """
		self.wrap = False
		msg = "global mRemote_buffer; mRemote_buffer= ''"
		self.cmdSend(msg)
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
			self.cmdSend(msg)
		package.close()
		self.wrap = True

	def _msgWrap(self, msg):
		cid = self._getHost()
		uid = self._getUser()
		pid = self._getPID()
		dtm = self._getTime()
		msg = 'print " "\n' \
			+ 'print "+ "*20\n' \
			+ 'print "%s"\n' % dtm \
			+ 'print ". "*20\n' \
			+ msg + '\n' \
			+ 'print ". "*20\n' \
			+ 'print "@ %s"\n' % uid \
			+ 'print "Sent from %s"\n' % cid \
			+ 'print "MAYA PID: %s"\n' % pid \
			+ 'print "- "*20'
		return msg

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
