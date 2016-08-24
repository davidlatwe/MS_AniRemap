# -*- coding:utf-8 -*-

from pymel.core import *

def grabCtrlCurves(below):
	"""  """
	return listRelatives(ls(sl= 1), ad= below, f= 1, typ= 'nurbsCurve')