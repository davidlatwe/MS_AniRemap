# -*- coding:utf-8 -*-

import pymel.core as pm


def amcveProfile(cvSrc, trim):
	"""
	"""
	cvSrc = pm.ls(cvSrc)[0]
	tiLen = []

	if trim:
		tiLen.append(pm.playbackOptions(q= 1, min= 1))
		tiLen.append(pm.playbackOptions(q= 1, max= 1))
		pm.undoInfo(ock= 1)
		pm.setKeyframe(cvSrc, insert= 1, t= tiLen, f= tiLen)
		pm.undoInfo(cck= 1)

	cvBaseMod = {
			'cvTyp' : pm.objectType(cvSrc),
			'prInf' : cvSrc.getPreInfinityType().key,
			'poInf' : cvSrc.getPostInfinityType().key,
			'weedT' : pm.keyTangent(cvSrc, q= 1, weightedTangents= 1),
			'breaD' : pm.keyframe(cvSrc, q= 1, breakdown= 1)
	}
	cvPortray = {
			'Frame' : pm.keyframe(cvSrc, q= 1, timeChange= 1),
			'Float' : pm.keyframe(cvSrc, q= 1, floatChange= 1),
			'Value' : pm.keyframe(cvSrc, q= 1, valueChange= 1)
	}
	cvFeature = {
			'TLock' : pm.keyTangent(cvSrc, q= 1, lock= 1),
			'WLock' : pm.keyTangent(cvSrc, q= 1, weightLock= 1),
			'InTyp' : pm.keyTangent(cvSrc, q= 1, inTangentType= 1),
			'OuTyp' : pm.keyTangent(cvSrc, q= 1, outTangentType= 1),
			'InWet' : pm.keyTangent(cvSrc, q= 1, inWeight= 1),
			'OuWet' : pm.keyTangent(cvSrc, q= 1, outWeight= 1),
			'InAng' : pm.keyTangent(cvSrc, q= 1, inAngle= 1),
			'OuAng' : pm.keyTangent(cvSrc, q= 1, outAngle= 1)
	}
	cvSrcProfile = {
			'cvTrimmed' : tiLen,
			'cvBaseMod' : cvBaseMod,
			'cvPortray' : cvPortray,
			'cvFeature' : cvFeature
	}
	if trim:
		pm.undo()

	return cvSrcProfile


def amcveRebuild(cvNew, cvSrcProfile):
	"""
	"""
	cvTrimmed = cvSrcProfile['cvTrimmed']
	cvBaseMod = cvSrcProfile['cvBaseMod']
	cvPortray = cvSrcProfile['cvPortray']
	cvFeature = cvSrcProfile['cvFeature']

	''' A. create animCurve '''
	# create same type of animation curve
	cvNew = pm.createNode(cvBaseMod['cvTyp'], n= cvNew)

	''' B. build curve base '''
	# whatever this animationCurve is time-base or float-base,
	# one of lists will be empty, just add them up.
	cvInp = cvPortray['Frame'] + cvPortray['Float']
	# set value to each keyframe
	for i, x in enumerate(cvInp):
		if cvTrimmed and (x < cvTrimmed[0] or x > cvTrimmed[1]):
			continue
		# whatever this animationCurve is time-base or float-base,
		# just set both, the one incorrect will take no effect.
		y = cvPortray['Value'][i]
		isBD = True if x in cvBaseMod['breaD'] else False
		pm.setKeyframe(cvNew, t= x, f= x, v= y, bd= isBD)

	''' C. inject curve feature '''
	cvNew.setPreInfinityType(cvBaseMod['prInf'])
	cvNew.setPostInfinityType(cvBaseMod['poInf'])
	weedT = cvBaseMod['weedT'][0]
	pm.keyTangent(cvNew, wt= weedT)
	if weedT:
		for i, x in enumerate(cvInp):
			if cvTrimmed and (x < cvTrimmed[0] or x > cvTrimmed[1]):
				continue
			WLock = cvFeature['WLock'][i]
			pm.keyTangent(cvNew, index= [i], wl= WLock)
	for i, x in enumerate(cvInp):
		if cvTrimmed and (x < cvTrimmed[0] or x > cvTrimmed[1]):
			continue
		pm.keyTangent(cvNew, index= [i], l= cvFeature['TLock'][i])
		pm.keyTangent(cvNew, index= [i], iw= cvFeature['InWet'][i])
		pm.keyTangent(cvNew, index= [i], ow= cvFeature['OuWet'][i])
		pm.keyTangent(cvNew, index= [i], ia= cvFeature['InAng'][i])
		pm.keyTangent(cvNew, index= [i], oa= cvFeature['OuAng'][i])
		pm.keyTangent(cvNew, index= [i], itt= cvFeature['InTyp'][i])
		pm.keyTangent(cvNew, index= [i], ott= cvFeature['OuTyp'][i])

	return cvNew
