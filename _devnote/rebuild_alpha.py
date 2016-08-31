
import pymel.core as pm

cvSrc = 'pCube1_translateX'
cvNew = 'hahaha'

# infinity~~~~~~~~~~~~~~~~

cvProfile = {
			'WLock' : pm.keyTangent(cvSrc, q= 1, weightLock= 1),
			'TLock' : pm.keyTangent(cvSrc, q= 1, lock= 1),
			'InWet' : pm.keyTangent(cvSrc, q= 1, inWeight= 1),
			'OuWet' : pm.keyTangent(cvSrc, q= 1, outWeight= 1),
			'InAng' : pm.keyTangent(cvSrc, q= 1, inAngle= 1),
			'OuAng' : pm.keyTangent(cvSrc, q= 1, outAngle= 1),
			'InTyp' : pm.keyTangent(cvSrc, q= 1, inTangentType= 1),
			'OuTyp' : pm.keyTangent(cvSrc, q= 1, outTangentType= 1),
		'__weedT__' : pm.keyTangent(cvSrc, q= 1, weightedTangents= 1),
		'__cvTyp__' : pm.objectType(cvSrc),
		'__breaD__' : pm.keyframe(cvSrc, q= 1, breakdown= 1),
			'Frame' : pm.keyframe(cvSrc, q= 1, timeChange= 1),
			'Float' : pm.keyframe(cvSrc, q= 1, floatChange= 1),
			'Value' : pm.keyframe(cvSrc, q= 1, valueChange= 1)
			}

''' A. create animCurve '''
# create same type of animation curve
cvNew = createNode(cvProfile['__cvTyp__'], n= cvNew)

''' B. build curve base '''
# whatever this animationCurve is time-base or float-base,
# one of lists will be empty, just add them up.
cvInp = cvProfile['Frame'] + cvProfile['Float']
# set value to each keyframe
for i, x in enumerate(cvInp):
	# whatever this animationCurve is time-base or float-base,
	# just set both, the one incorrect will take no effect.
	y = cvProfile['Value'][i]
	isBD = True if x in cvProfile['__breaD__'] else False
	pm.setKeyframe(cvNew, t= x, f= x, v= y, bd= isBD)

''' C. inject curve feature '''
weedT = cvProfile['__weedT__'][0]
pm.keyTangent(cvNew, wt= weedT)
if weedT:
	for i, x in enumerate(cvInp):
		WLock = cvProfile['WLock'][i]
		pm.keyTangent(cvNew, index= [i], wl= WLock)

for i, x in enumerate(cvInp):
	TLock = cvProfile['TLock'][i]
	InTyp = cvProfile['InTyp'][i]
	OuTyp = cvProfile['OuTyp'][i]
	InWet = cvProfile['InWet'][i]
	OuWet = cvProfile['OuWet'][i]
	InAng = cvProfile['InAng'][i]
	OuAng = cvProfile['OuAng'][i]
	pm.keyTangent(cvNew, index= [i],  l= TLock,
									itt= InTyp,ott= OuTyp,
									 iw= InWet, ow= OuWet,
									 ia= InAng, oa= OuAng)
