# -*- coding:utf-8 -*-

import pymel.core as pm
import mAnimRemapMethod as md; reload(md)


def remoteRemap(tel, remapType, tirm, sel_src, sel_dis, scale= None):
	"""
	"""
	# src ctrl keys
	ctrlList_src = md.lsController(sel_src)
	src = md.keyController(ctrlList_src)
	# dis ctrl list
	mod = '''
	from __main__ import *
	import pymel.core as pm
	import mAniRemap.mAnimRemapMethod as md; reload(md)
	'''
	dis = eval(tel.funcSend(md.lsController, sel_dis, None, mod= mod))
	# gen map
	keyMap = md.drawKeyMap(remapType, src, dis)
	# link up
	mod = '''
	from __main__ import *
	import pymel.core as pm
	import mAniRemap.mAnimRemapMethod as md; reload(md)
	import mAniRemap.mAnimCurveGen as cg; reload(cg)
	'''
	for ctrl in keyMap:
		cvp = md.packup(src[ctrl], tirm)
		tel.funcSend(md.wireup, cvp, keyMap[ctrl], scale, mod= mod)


def localRemap(dis, remapType, tirm, sel_src, sel_dis, scale= None):
	"""
	### preselect dis, than select src
	"""
	# src ctrl keys
	ctrlList_src = md.lsController(sel_src)
	src = md.keyController(ctrlList_src)
	# dis ctrl list
	dis = md.lsController(sel_dis, dis)
	# gen map
	keyMap = md.drawKeyMap(remapType, src, dis)
	# link up
	for ctrl in keyMap:
		if not ctrl == keyMap[ctrl]:
			cvp = md.packup(src[ctrl], tirm)
			md.wireup(cvp, keyMap[ctrl], scale)