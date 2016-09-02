# -*- coding:utf-8 -*-

import pymel.core as pm
import maya.cmds as cmds
import maya.OpenMaya as api
import maya.OpenMayaUI as apiUI
import sys
import os

def imgSend(pointA):
	""" Sending viewport snapshot """
	imgPath = os.environ['tmpdir'] + '/mRSnapShot_Send.jpg'
	# take snapshot
	view = apiUI.M3dView.active3dView()
	snapShot = api.MImage()
	view.readColorBuffer(snapShot, True)
	snapShot.writeToFile(imgPath, 'jpg')
	# function for unpack to renderview
	mod = '''
	import os
	'''
	def unpackImg():
		'''Write string to image and open in renderview'''
		imgPath = os.environ['tmpdir'] + '/mRSnapShot_Grab.jpg'
		global mTeleport_buffer
		fh = open(imgPath, 'w')
		fh.write(mTeleport_buffer)
		fh.close()
		mel.eval('RenderViewWindow')
		rview = cmds.getPanel(sty= 'renderWindowPanel')
		cmds.renderWindowEditor(rview, e= True, li= imgPath)
		print 'Snapshot send.'
		return 0
	# start sending
	return pointA.sendall(filePath= imgPath, postFunc= unpackImg, mod= mod)

def msgSend(pointA, msg):
	""" Sending chat msg """
	uid = os.environ['username'].rjust(8, ' ')
	dtm = pointA.getTime(1)
	msg = 'print "%s | %s : %s"' % (dtm, uid, msg)
	return pointA.cmdSend(msg, True)
