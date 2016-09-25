import sys
import os

tSrc = 'devPath'

toolPaths = {
	'devPath' : '/home/david/gitRepo/MS_AniRemap'	
	}

sysPath = sys.path
for i, sp in enumerate(sysPath):
	sysPath[i] = str(os.path.abspath(sp))
sysPath = list(set(sysPath))
for tpv in toolPaths.values():
	tpv = os.path.abspath(tpv)
	if tpv in sysPath:
		sysPath.remove(tpv)

sysPath.insert(0, os.path.abspath(toolPaths[tSrc]))
sys.path = sysPath

import mQtGui; reload(mQtGui)
import mTeleport; reload(mTeleport)
import mTeleport.pointA as pA; reload(pA)
import mTeleport.pointB as pB; reload(pB)
import mTeleport.missions as missions; reload(missions)
import mTeleport.drill as drill; reload(drill)
import mAniRemap; reload(mAniRemap)
import mAniRemap.mAnimRemap as mr; reload(mr)
