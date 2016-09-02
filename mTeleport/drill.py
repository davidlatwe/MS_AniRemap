# -*- coding:utf-8 -*-

import maya.cmds as cmds
import os
import missions as ms; reload(ms)

class MrDrill():
	""" """
	def __init__(self):
		self.abort = False

	def checkNext(self, subject):
		if not self.abort:
			result = cmds.confirmDialog(t= 'Teleportation Test',
						m= subject + '\nDone.',	b= ['Stop', 'Next'],
						db= 'Next', cb= 'Stop', ds= 'Stop', icn= 'info')
			self.abort = False if result == 'Next' else True
		return self.abort

def drill(pointA):
	"""
	"""
	mrDrill = MrDrill()
	# start Drill
	if True:
		test = '''
		Connection test
		'''
		pointA.connTest()
	
	if not mrDrill.checkNext(test):
		test = 'Simple one line python command test'
		print pointA.cmdSend('cmds.polyCube()')
	
	if not mrDrill.checkNext(test):
		test = '''
		Simple return function with var
		'''
		def myFarm(a, b):
			''' calling my animals, and calls me back.'''
			print a; return b
		print pointA.funcSend(myFarm, 'Hey, pig.', 'oink!oink!')
	
	if not mrDrill.checkNext(test):
		test = '''
		Long return function with var
		'''
		mass = '!start!' + 'x' * 100000 + '!end!'
		func = 'def printMassive(x):\n\tmass = "' + mass \
			 + '"\n\tprint mass.replace("x", x)\n\treturn mass.replace("x", x)'
		exec func in globals(), locals()
		print pointA.funcSend(printMassive, 'm')
	
	if not mrDrill.checkNext(test):
		test = '''
		Sending viewPort snapshot
		'''
		print ms.imgSend(pointA)
	
	if not mrDrill.checkNext(test):
		test = '''
		Open file command and return transform list
		'''
		multipleFilters = "Maya Files (*.ma *.mb)"
		filePath = cmds.fileDialog2(ff= multipleFilters, ds= 2, fm= 1)[0]
		def openAndReturn(filePath):
			try:
				cmds.file(filePath, f= 1, o= 1)
				return cmds.ls(tr= 1)
			except:
				print 'error'
		resList = eval(pointA.funcSend(openAndReturn, filePath))
		print resList
		if type(resList) == type(list()):
			for dag in resList:
				print dag
	
	if not mrDrill.checkNext(test):
		test = '''
		End drill
		'''
		print ms.msgSend(pointA, 'Goodbye, My name is ' + os.environ['username'])