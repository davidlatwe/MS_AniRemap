from pymel.core import *

keyTangent('pCube1_translateX', q= 1, inAngle= 1)
keyTangent('pCube1_translateX', q= 1, outAngle= 1)

keyTangent('pCube1_translateX', q= 1, inWeight= 1)
keyTangent('pCube1_translateX', q= 1, outWeight= 1)

keyTangent('pCube1_translateX', q= 1, inTangentType= 1)
keyTangent('pCube1_translateX', q= 1, outTangentType= 1)

keyTangent('pCube1_translateX', q= 1, ix= 1)
keyTangent('pCube1_translateX', q= 1, ox= 1)

keyTangent('pCube1_translateX', q= 1, iy= 1)
keyTangent('pCube1_translateX', q= 1, oy= 1)

# return all key's tangentsLock status
keyTangent('pCube1_translateX', q= 1, lock= 1)
# return all key's weightLock status
keyTangent('pCube1_translateX', q= 1, weightLock= 1)
# return curve is tangent-locked or not
keyTangent('pCube1_translateX', q= 1, weightedTangents= 1)

# return all frame number
keyframe('pCube1_translateX', q= 1, timeChange= 1)
# return all key value
keyframe('pCube1_translateX', q= 1, valueChange= 1)
# return breakdown frame number ( breakdown is a weight unLocked key )
keyframe('pCube1_translateX', q= 1, breakdown= 1)
