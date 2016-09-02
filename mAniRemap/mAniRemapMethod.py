# -*- coding:utf-8 -*-

import pymel.core as pm

def grabCtrlCurves(below):
	"""  """
	return pm.listRelatives(ls(sl= 1), ad= below, f= 1, typ= 'nurbsCurve')