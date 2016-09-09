# -*- coding:utf-8 -*-

import pymel.core as pm


def lsController(sel= None):
	"""
	回傳所選取物件底下的所有 nurbsCurve 清單，
	或只回傳所選取的 nurbsCurve
	"""
	ad = False if sel else True
	searchRange = pm.listRelatives(pm.ls(sl= 1), ad= ad, typ= 'nurbsCurve')
	
	return [c.getParent().name() for c in searchRange]


def keyController(ctrlList):
	"""
	回傳有 keyframe 的 controller 字典
	{ ctrl : { ctrl.attr : animCurveNode } }
	"""
	ctrlKey = {}
	for ctrl in ctrlList:
		hasKey = False
		driven = pm.setDrivenKeyframe(ctrl, q= 1, dn= 1)
		keyNum = pm.keyframe(ctrl, q= 1, kc= 1)
		drnNum = 0
		if keyNum:
			if driven[0] == 'No driven attributes found on the selected item.':
				# has key
				hasKey = True
			else:
				# has drivenKey
				for dn in driven:
					drnNum += pm.keyframe(dn, q= 1, kc= 1)
				if drnNum < keyNum:
					# has key
					hasKey = True
		if hasKey:
			atKey = {}
			ats = pm.listConnections(ctrl, d= 0, c= 1, scn= 1, t= 'animCurve')
			for at in ats:
				at = at[0]
				# skip driven
				if drnNum and at in driven:
					continue
				at = at.name()
				ac = pm.listConnections(at, d= 0, scn= 1, t= 'animCurve')
				atKey[str(at)] = str(ac[0].name())
			ctrlKey[str(ctrl)] = atKey

	return ctrlKey


def ctrlRemap(src, dis):
	"""
	"""
	def noNS(dagPath):
		return '|'.join([ dag.split(':')[-1] for dag in dagPath.split('|') ])

	remap = {}
	for ctrl in src:
		bCtrl = noNS(ctrl)
