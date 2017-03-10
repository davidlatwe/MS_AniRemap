# -*- coding:utf-8 -*-

import pymel.core as pm
import mAnimCurveGen as cg; reload(cg)
import mAnimRemapType as mt; reload(mt)


def lsController(sel, localDis= None):
	"""
	回傳所選取物件底下的所有 nurbsCurve 清單，
	或只回傳所選取的 nurbsCurve
	"""
	ad = not sel
	dag = localDis if localDis else pm.ls(sl= 1)
	searchRange = pm.listRelatives(dag, ad= ad, s= 1, f= 1, typ= 'nurbsCurve')
	ctrlList = list(set([str(c.getParent().fullPath()) for c in searchRange]))

	return ctrlList


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


def drawKeyMap(remapType, src, dis):
	"""
	"""
	if remapType == 'name':
		keyMap = mt.remapNameMatch(src, dis)
	if remapType == 'order':
		keyMap = mt.remapSelectOrder(src, dis)

	return keyMap


def packup(ctrlAttr, tirm):
	"""
	"""
	cvp = {}
	for cat in ctrlAttr:
		cvp[cat] = cg.amcveProfile(ctrlAttr[cat], tirm)

	return cvp


def wireup(cvp, ctrl, scale, mirror):
	"""
	"""
	def spaceScale(attr, cvNew, scale):
		"""
		"""
		# Translate
		if attr.startswith('translate'):
			pm.scaleKey(cvNew, vs= scale, vp= 0, ssk= False)
		# Scale
		if attr.startswith('scale'):
			pm.scaleKey(cvNew, vs= scale, vp= 1, ssk= False)

	def keyMirror(attr, cvNew, mirror):
		"""
		"""
		for axis in mirror:
			# Translate
			if axis.startswith('t') and attr.startswith('translate' + axis[-1].upper()):
				pm.scaleKey(cvNew, vs= -1, vp= 0, ssk= False)
			# Rotation
			if axis.startswith('r') and attr.startswith('rotate' + axis[-1].upper()):
				pm.scaleKey(cvNew, vs= -1, vp= 0, ssk= False)


	for cat in cvp:
		attr = cat.split('.')[1]
		if pm.attributeQuery(attr, node= ctrl, exists= True):
			disCat = ctrl + '.' + attr
			if not pm.connectionInfo(disCat, id= True):
				lock = False
				if pm.getAttr(disCat, l= True):
					lock = True
					pm.setAttr(disCat, l= False)
				cvNew = cg.amcveRebuild(cat.replace('.', '_'), cvp[cat])
				pm.connectAttr(cvNew.output, disCat)
				if scale:
					spaceScale(attr, cvNew, scale)
				if mirror:
					keyMirror(attr, cvNew, mirror)
				if lock:
					pm.setAttr(disCat, l= True)
			else:
				pass

	return 0