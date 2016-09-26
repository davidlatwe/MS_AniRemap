
"""
Moonshine Animation Remap Tool
"""

def start():
	import mAniRemap; reload(mAniRemap)
	import mAniRemap.mAnimRemapUI as mrui; reload(mrui)
	mrui.ui_main()