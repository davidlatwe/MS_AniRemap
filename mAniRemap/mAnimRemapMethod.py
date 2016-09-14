# -*- coding:utf-8 -*-

import pymel.core as pm
import re
import mAnimCurveGen as cg; reload(cg)


def lsController(sel= None):
	"""
	回傳所選取物件底下的所有 nurbsCurve 清單，
	或只回傳所選取的 nurbsCurve
	"""
	ad = False if sel else True
	searchRange = pm.listRelatives(pm.ls(sl= 1), ad= ad, typ= 'nurbsCurve')
	ctrlList = [str(c.getParent().name()) for c in searchRange]

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


def remapNameMatch(src, dis):
	"""
	"""
	def rmNS(dagPath):
		''' clean up src namespace and leave basename '''
		return '|'.join([ dag.split(':')[-1] for dag in dagPath.split('|') ])

	keyMap = {}
	for ctrl in src:
		ctrlBN = rmNS(ctrl)
		reNS = '.*:' + ctrlBN.replace('|', '\|.*:')
		reBN = ctrlBN.replace('|', '\|')
		regex = re.compile(reNS + '|' + reBN)
		found = [m.group(0) for d in dis for m in [regex.search(d)] if m]
		if found:
			if len(found) == 1:
				# found only one match - great!
				keyMap[ctrl] = found[0]
			else:
				# found more than one match
				pass
		else:
			# no match found
			pass

	return keyMap


def remapSelectOrder(src, dis):
	"""
	"""
	keyMap = {}
	for i, ctrl in enumerate(src):
		if i < len(dis):
			keyMap[ctrl] = dis[i]
		else:
			# dis traget number is less than src, key lose
			pass

	return keyMap


def packup(ctrlAttr, tirm):
	"""
	"""
	cvp = {}
	for cat in ctrlAttr:
		cvp[cat] = cg.amcveProfile(ctrlAttr[cat], tirm)

	return cvp


def wireup(cvp, ctrl):
	"""
	"""
	for cat in cvp:
		attr = cat.split('.')[1]
		if pm.attributeQuery(attr, node= ctrl, exists= True):
			disCat = ctrl + '.' + attr
			if not pm.connectionInfo(disCat, id= True):
				if pm.getAttr(disCat, l= True):
					pm.setAttr(disCat, l= False)
				cvNew = cg.amcveRebuild(cat.replace('.', '_'), cvp[cat])
				pm.connectAttr(cvNew.output, disCat)
			else:
				pass