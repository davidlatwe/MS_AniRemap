# -*- coding:utf-8 -*-

import pymel.core as pm
import mAnimRemapMethod as md; reload(md)
import json


def remoteRemap(tel, remapType, tirm, sel_src, sel_dis, scale= None, mirror= None):
	"""
	rd = pA.PointA()
	rd.setCoord(3855)
	mr.remoteRemap(rd, 'name', True, False, False, 0.1)
	"""
	# src ctrl keys
	ctrlList_src = md.lsController(sel_src)
	src = md.keyController(ctrlList_src)
	# dis ctrl list
	mod = '''
	from __main__ import *
	import pymel.core as pm
	'''
	dis = eval(tel.funcSend(md.lsController, sel_dis, None, mod= mod))
	# gen map
	keyMap = md.drawKeyMap(remapType, src, dis)
	# mirror map
	mirrorMap = {}
	if mirror:
		mirrorMapPath = 'O:/201609_MaydayMv/Maya/assets/crowd/soldierA_OA/soldierA_mirrorMap.json'
		with open(mirrorMapPath) as mirrorMapJson:
			mirrorMap = json.load(mirrorMapJson)
	# link up
	mod = '''
	from __main__ import *
	import pymel.core as pm
	import MS_AniRemap.mAniRemap.mAnimCurveGen as cg; reload(cg)
	'''
	tel.cmdSend('cmds.undoInfo(ock= 1)')
	for ctrl in keyMap:
		cvp = md.packup(src[ctrl], tirm)
		ctb = ctrl.split('|')[-1].split(':')[-1]
		mir = mirrorMap[ctb] if mirrorMap and mirrorMap.has_key(ctb) else []
		tel.funcSend(md.wireup, cvp, keyMap[ctrl], scale, mir, mod= mod)
	tel.cmdSend('cmds.undoInfo(cck= 1)')
	tel.cmdSend('cmds.warning("[ !!! ] AniRemap: DONE.")')


def localRemap(dis, remapType, tirm, sel_src, sel_dis, scale= None, mirror= None):
	"""
	### preselect dis, than select src
	dis = 'TVbuddy_rigging_master3:TVbuddyV1'
	mr.localRemap(dis, 'order', True, False, False)
	"""
	# src ctrl keys
	ctrlList_src = md.lsController(sel_src)
	src = md.keyController(ctrlList_src)
	# dis ctrl list
	dis = md.lsController(sel_dis, dis)
	# gen map
	keyMap = md.drawKeyMap(remapType, src, dis)
	# link up
	pm.undoInfo(ock= 1)
	for ctrl in keyMap:
		if not ctrl == keyMap[ctrl]:
			cvp = md.packup(src[ctrl], tirm)
			md.wireup(cvp, keyMap[ctrl], scale, mirror)
	pm.undoInfo(cck= 1)