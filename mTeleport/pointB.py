# -*- coding:utf-8 -*-

import maya.cmds as cmds
import socket


def Singleton(cls):
	instances = {}
	def Instance():
		if cls not in instances:
			instances[cls] = cls()
		return instances[cls]
	return Instance

@Singleton
class PointB(object):
	"""docstring for Receiver"""
	def __init__(self):
		self.host = ''
		self.port = 0
		self.buff = 8192
		self.maps = {}

	def portOpen(self, mode, langue, port= None):
		self._setDomain(mode)
		self._setPortal(port)
		ipaddr = '%s:%d' % (self.host, self.port)
		cmds.commandPort(n= ipaddr, stp= langue, eo= 0, bs= self.buff)
		self.maps[str(self.port)] = {'ipaddr' : ipaddr,
									 'langue' : langue,
									 'status' : True}
		return ipaddr

	def portClose(self, port):
		if port == 0:
			for p in self.maps:
				if self.maps[p]['status']:
					self.portClose(p)
			return None
		ipaddr = self.maps[str(port)]['ipaddr']
		self.maps[str(port)]['status'] = False
		cmds.commandPort(n= ipaddr, cl= 1)

	def listPorts(self):
		def _printPort(portDict, s):
			for p in portDict:
				l = portDict[p]['langue']
				m = portDict[p]['ipaddr'].rjust(22, ' ')
				p = p.rjust(6, ' ')
				print '%s %s %s @ %s' % (p, s, m, l)
		port_on, port_off = self._portStatus()
		print '\n' + '> '*25
		print 'commandPort ON\n' + '- '*25
		_printPort(port_on, '|')
		print '. '*25
		print 'commandPort OFF\n' + '- '*25
		_printPort(port_off, 'X')
		print '< '*25

	def _portStatus(self):
		port_on = {}
		port_off= {}
		for p in self.maps:
			if self.maps[p]['status']:
				port_on[p] = self.maps[p]
			else:
				port_off[p]= self.maps[p]
		return port_on, port_off

	def _setDomain(self, mode= None):
		if mode == 'LAN':
			self.host = socket.gethostbyname(socket.gethostname())
		else:
			self.host = ''

	def _setPortal(self, port= None):
		""" get free port """
		if port:
			self.port = port
			return None
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('',0))
		s.listen(1)
		self.port = s.getsockname()[1]
		s.close()
