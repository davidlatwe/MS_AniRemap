# -*- coding:utf-8 -*-

import pymel.core as pm
from functools import partial

def switchUI(width, height, lableON, lableOFF, default, parent= None):
	"""
	"""
	switchForm = pm.formLayout(w= width, h= height)
	bBase = pm.button(l= '', w= width, h= height, en= 0)
	tON = pm.text(l= lableON, w= width/2-10, h= height, en= default)
	tOFF = pm.text(l= lableOFF, w= width/2-10, h= height)
	bBody = pm.button(l= '', w= width/2-4, h= height-4)
	pm.setParent('..')
	pm.formLayout(switchForm, e= 1, af= [(bBase, 'top', 0)])
	pm.formLayout(switchForm, e= 1, af= [(tON, 'top', 0), (tON, 'left', 5)])
	pm.formLayout(switchForm, e= 1, af= [(tOFF, 'top', 0), (tOFF, 'right', 5)])
	if default:
		pm.formLayout(switchForm, e= 1, af= [(bBody, 'top', 2), (bBody, 'left', width/2+2), (bBody, 'right', 2)])
		pm.button(bBase, e= 1, bgc= [0.26, 0.51, 0.62])
	else:
		pm.formLayout(switchForm, e= 1, af= [(bBody, 'top', 2), (bBody, 'left', 2), (bBody, 'right', width/2+2)])
		pm.button(bBase, e= 1, bgc= [0.6, 0.32, 0.31])

	def switchCMD(tON, bBase, bBody, switchForm, width, *args):
		if pm.text(tON, q= 1, en= 1):
			pm.formLayout(switchForm, e= 1, af= [(bBody, 'top', 2), (bBody, 'left', 2), (bBody, 'right', width/2+2)])
			pm.button(bBase, e= 1, bgc= [0.6, 0.32, 0.31])
			pm.text(tON, e= 1, en= 0)
		else:
			pm.formLayout(switchForm, e= 1, af= [(bBody, 'top', 2), (bBody, 'left', width/2+2), (bBody, 'right', 2)])
			pm.button(bBase, e= 1, bgc= [0.26, 0.51, 0.62])
			pm.text(tON, e= 1, en= 1)
	pm.button(bBody, e= 1, c= partial(switchCMD, tON, bBase, bBody, switchForm, width))
	if parent:
		pm.formLayout(switchForm, e= 1, p= parent)

	return switchForm


def ui_main():

	windowName = 'msAnimRemap'

	if pm.dockControl(windowName, q= 1, ex= 1):
		pm.deleteUI(windowName)

	main_window = pm.window()
	
	mainForm = pm.formLayout(p= main_window)
	
	staticArea = pm.columnLayout(adj= 1, rs= 5)

	pm.rowLayout(nc= 2, adj= 1, cal= [1, 'right'])
	pm.text('Role : ')
	switchUI(120, 24, 'Source', 'Target', 1)
	pm.setParent('..')
	pm.rowLayout(nc= 2, adj= 1, cal= [1, 'right'])
	pm.text('Machine : ')
	switchUI(120, 24, 'Remote', 'Local', 0)
	pm.setParent('..')
	pm.rowLayout(nc= 2, adj= 1, cal= [1, 'right'])
	pm.text('Maya : ')
	switchUI(120, 24, 'Cross', 'Alone', 1)
	pm.setParent('..')
	

	#paneArea = pm.paneLayout(cn= 'horizontal2', shp= 1, ps= [1, 100, 1])
	

	pm.formLayout(mainForm, e= 1, af= [(staticArea, 'top', 0)])
	#pm.formLayout(mainForm, e= 1, af= [(paneArea, 'top', 90), (paneArea, 'bottom', 0)])


	# pySide
	

	pm.dockControl(windowName, area= 'right', content= main_window, allowedArea= ['right', 'left'], vis= 1, s= 0, w= 380)