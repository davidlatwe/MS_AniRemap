# -*- coding:utf-8 -*-

import pymel.core as pm
import mAnimRemapMethod as md; reload(md)


def remoteRemap(tel, tirm):
	"""
	"""
	# src ctrl keys
	ctrlList_src = md.lsController()
	src = md.keyController(ctrlList_src)
	# dis ctrl list
	mod = '''
	from __main__ import *
	import mAniRemap.mAnimRemapMethod as md; reload(md)
	'''
	dis = eval(tel.funcSend(md.lsController, None, mod= mod))
	# gen map
	keyMap = md.remapNameMatch(src, dis)
	# link up
	mod = '''
	from __main__ import *
	import mAniRemap.mAnimRemapMethod as md; reload(md)
	import mAniRemap.mAnimCurveGen as cg; reload(cg)
	'''
	for ctrl in keyMap:
		cvp = md.packup(src[ctrl], tirm)
		tel.funcSend(md.wireup, cvp, keyMap[ctrl], mod= mod)


def localRemap(dis, tirm):
	"""
	"""
	# preselect dis, than select src
	pass