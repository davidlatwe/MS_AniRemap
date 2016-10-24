# -*- coding:utf-8 -*-

import pymel.core as pm
from functools import partial
import mQtGui; reload(mQtGui)
import mQtGui.muiSwitchBox as mqsb; reload(mqsb)
import mQtGui.mGetQt as mqt; reload(mqt)
import mTeleport; reload(mTeleport)
import mTeleport.pointA as pA; reload(pA)
import mTeleport.pointB as pB; reload(pB)
import mAniRemap; reload(mAniRemap)
import mAniRemap.mAnimRemap as mr; reload(mr)


def ui_main():

	windowName = 'msAnimRemap'
	dockWidth = 250

	beam = pA.PointA()
	mark = pB.PointB()

	if pm.dockControl(windowName, q= 1, ex= 1):
		pm.dockControl(windowName, e= 1, vis= 0)
		pm.deleteUI(windowName, lay= 1)

	main_window = pm.window()
	mainForm = pm.formLayout(p= main_window)
	copypasteField = pm.cmdScrollFieldExecuter(vis= 0, p= mainForm)

	bannerArea = pm.columnLayout(adj= 1)
	bannerTxt = pm.text(l= 'AniRemap', w= dockWidth)
	QBannerTxt = mqt.convert(bannerTxt)
	QBannerTxt.setStyleSheet('QObject {font: bold 42px; color: #222222;}')
	pm.setParent('..')

	versioArea = pm.columnLayout(adj= 1)
	versioTxt = pm.text(l= 'v'+mAniRemap.__version__)
	QVersioTxt = mqt.convert(versioTxt)
	QVersioTxt.setStyleSheet('QObject {font: bold 10px; color: #777777;}')
	pm.setParent('..')
	
	sep______1 = pm.separator(st= 'in', w= dockWidth - 8)

	panelTxt_1 = pm.text(l= 'Transfer Settings', al= 'left')
	QpanelTxt_1 = mqt.convert(panelTxt_1)
	QpanelTxt_1.setStyleSheet('QObject {font: 12px; color: #777777;}')

	trans_Area = pm.columnLayout(adj= 1, rs= 2)

	role_group = pm.columnLayout(adj= 1, rs= 2)
	pm.text('Role', al= 'left')
	cmC = pm.columnLayout()
	role_mqsb = mqsb.SwitchBox(onl= 'Source', ofl= 'Target', w= dockWidth - 42, h= 28, v= True, \
		p= cmC, ofbg= [148, 106, 68], onbg= [72, 120, 138])
	pm.setParent('..')
	pm.setParent('..')

	pm.rowLayout(nc= 2, adj= 1, cal= [1, 'right'])

	maya_group = pm.columnLayout(adj= 1, rs= 2)
	pm.text('Maya', al= 'left')
	cmA= pm.columnLayout()
	maya_mqsb = mqsb.SwitchBox(onl= 'Cross', ofl= 'Alone', w= (dockWidth-46)/2, h= 20, v= True, p= cmA)
	pm.setParent('..')
	pm.setParent('..')

	mode_group = pm.columnLayout(adj= 1, rs= 2)
	pm.text('Mode', al= 'left')
	cmB = pm.columnLayout()
	mode_mqsb = mqsb.SwitchBox(onl= 'LAN', ofl= 'Local', w= (dockWidth-46)/2, h= 20, p= cmB)
	pm.setParent('..')
	pm.setParent('..')

	pm.setParent('..')

	pm.setParent('..')
	
	sep______2 = pm.separator(st= 'in', w= dockWidth - 8)

	targetLabel = 'Target Settings' if True else 'Target Info'
	panelTxt_2 = pm.text(l= targetLabel, al= 'left')
	QpanelTxt_2 = mqt.convert(panelTxt_2)
	QpanelTxt_2.setStyleSheet('QObject {font: 12px; color: #777777;}')

	targe_Area = pm.columnLayout(adj= 1, rs= 5)
	
	targetAlone = pm.columnLayout(adj= 1, rs= 5, vis= 0)
	trg_sls = pm.textScrollList(w= 180, h= 50)
	pm.rowLayout(nc= 3, adj= 1, cal= [1, 'right'])
	svt_btn = pm.button(l= 'Save Target', bgc= [0.40, 0.37, 0.31])
	adt_btn = pm.button(l= '+', w= 20)
	rmt_btn = pm.button(l= '-', w= 20)
	pm.setParent('..')
	pm.setParent('..')

	targetCross = pm.columnLayout(adj= 1, rs= 5)
	pm.rowLayout(nc= 2, adj= 1, cal= [1, 'right'])
	tcHost_lbe = pm.text('Host : ', en= 0)
	tcHost_txt = pm.textField(w= 140, en= 0)
	pm.setParent('..')
	pm.rowLayout(nc= 2, adj= 1, cal= [1, 'right'])
	pm.text('Port : ')
	tcPort_txt = pm.textField(w= 140)
	pm.setParent('..')
	srcAddr = pm.rowLayout(nc= 2, adj= 1, cal= [1, 'right'])
	ch_btn = pm.button(l= 'Connect', bgc= [0.40, 0.37, 0.31])
	ps_btn = pm.button(l= 'Paste', w= 50)
	pm.setParent('..')
	disAddr = pm.rowLayout(nc= 2, adj= 1, cal= [1, 'right'], vis= 0)
	op_btn = pm.button(l= 'Open', bgc= [0.40, 0.37, 0.31])
	cp_btn = pm.button(l= 'Copy', w= 50)
	pm.setParent('..')
	pm.setParent('..')

	pm.setParent('..')

	sep______3 = pm.separator(st= 'in', w= dockWidth - 8)

	panelTxt_3 = pm.text(l= 'Remap Settings', al= 'left')
	QpanelTxt_3 = mqt.convert(panelTxt_3)
	QpanelTxt_3.setStyleSheet('QObject {font: 12px; color: #777777;}')

	remap_Area = pm.columnLayout(adj= 1, rs= 5)
	
	pm.rowLayout(nc= 2, cal= [1, 'right'], h= 20)
	pm.text('Match : ', w= 45, al= 'right')
	match_mnu = pm.optionMenu(w= 120)
	pm.menuItem('name')
	pm.menuItem('order')
	pm.setParent('..')

	tirm_group = pm.rowLayout(nc= 2, adj= 2, cal= [1, 'right'], h= 20)
	pm.text('Time : ', w= 45, al= 'right')
	cmD = pm.columnLayout()
	tirm_mqsb = mqsb.SwitchBox(onl= 'Slider', ofl= 'Entire', w= 120, h= 18, v= False, \
		p= cmD, ofbg= [62, 58, 60], onbg= [88, 90, 95])
	pm.setParent('..')
	pm.setParent('..')

	hSrc_group = pm.rowLayout(nc= 2, adj= 2, cal= [1, 'right'], h= 20)
	pm.text('Source : ', w= 45, al= 'right')
	cmE = pm.columnLayout()
	hSrc_mqsb = mqsb.SwitchBox(onl= 'Hierachy', ofl= 'Selected', w= 120, h= 18, v= True, \
		p= cmE, ofbg= [62, 58, 60], onbg= [88, 90, 95])
	pm.setParent('..')
	pm.setParent('..')

	hTrg_group = pm.rowLayout(nc= 2, adj= 2, cal= [1, 'right'], h= 20)
	pm.text('Target : ', w= 45, al= 'right')
	cmF = pm.columnLayout()
	hTrg_mqsb = mqsb.SwitchBox(onl= 'Hierachy', ofl= 'Selected', w= 120, h= 18, v= True, \
		p= cmF, ofbg= [62, 58, 60], onbg= [88, 90, 95])
	pm.setParent('..')
	pm.setParent('..')

	pm.rowLayout(nc= 2, cal= [1, 'right'], h= 20)
	pm.text('Scale : ', w= 45, al= 'right')
	scale_flt = pm.floatField(v= 1, pre= 2, w= 120)
	pm.setParent('..')

	pm.rowLayout(nc= 2, adj= 2, cal= [1, 'right'], h= 20)
	pm.text('Mirror : ', w= 45, al= 'right', en= 0)
	pm.radioButtonGrp('mirror_radioBtnGrp', nrb= 4, la4= ['None', 'Y Z', 'Y X', 'X Z'], ad4= 1, \
		cw4= [50, 35, 35, 35], sl= 1, en= 0)
	pm.setParent('..')

	pm.setParent('..')
	
	sep______4 = pm.separator(st= 'in', w= dockWidth - 8)

	exect_Area = pm.columnLayout(adj= 1, rs= 5, h= 46)

	remap_btn = pm.button(l= 'Remap Animation Curves', w= dockWidth - 30, h= 40)
	pm.setParent('..')


	pm.formLayout(mainForm, e= 1, af= [(bannerArea, 'top', -6)])
	pm.formLayout(mainForm, e= 1, af= [(versioArea, 'top', 40), (versioArea, 'right', 50)])
	pm.formLayout(mainForm, e= 1, af= [(sep______1, 'top', 58)])
	pm.formLayout(mainForm, e= 1, af= [(panelTxt_1, 'top', 64)])
	pm.formLayout(mainForm, e= 1, af= [(trans_Area, 'top', 84), (trans_Area, 'left', 15)])
	pm.formLayout(mainForm, e= 1, af= [(sep______2, 'top', 182)])
	pm.formLayout(mainForm, e= 1, af= [(panelTxt_2, 'top', 188)])
	pm.formLayout(mainForm, e= 1, af= [(targe_Area, 'top', 210), (targe_Area, 'left', 31)])
	pm.formLayout(mainForm, e= 1, af= [(sep______3, 'top', 304)])
	pm.formLayout(mainForm, e= 1, af= [(panelTxt_3, 'top', 310)])
	pm.formLayout(mainForm, e= 1, af= [(remap_Area, 'top', 332), (remap_Area, 'left', 20)])
	pm.formLayout(mainForm, e= 1, af= [(sep______4, 'top', 488)])
	pm.formLayout(mainForm, e= 1, af= [(exect_Area, 'top', 496), (exect_Area, 'left', 10)])


	def maya_mqsb_switch(status, *args):
		pm.columnLayout(targetAlone, e= 1, vis= 0 if status else 1)
		pm.columnLayout(targetCross, e= 1, vis= 1 if status else 0)
		pm.columnLayout(mode_group, e= 1, en= 1 if status else 0)
		pm.columnLayout(role_group, e= 1, en= 1 if status else 0)
		if status:
			pm.columnLayout(remap_Area, e= 1, en= 1 if role_mqsb.isChecked() else 0)
			pm.columnLayout(exect_Area, e= 1, en= 1 if role_mqsb.isChecked() else 0)
		else:
			pm.columnLayout(remap_Area, e= 1, en= 1)
			pm.columnLayout(exect_Area, e= 1, en= 1)
	maya_mqsb.onCmd = partial(maya_mqsb_switch, 1)
	maya_mqsb.offCmd = partial(maya_mqsb_switch, 0)

	def mode_mqsb_switch(status, *args):
		pm.text(tcHost_lbe, e= 1, en= 1 if status else 0)
		pm.textField(tcHost_txt, e= 1, tx= '', en= 1 if status else 0)
		pm.textField(tcPort_txt, e= 1, tx= '')
	mode_mqsb.onCmd = partial(mode_mqsb_switch, 1)
	mode_mqsb.offCmd = partial(mode_mqsb_switch, 0)

	def role_mqsb_switch(status, *args):
		pm.rowLayout(srcAddr, e= 1, vis= 1 if status else 0)
		pm.rowLayout(disAddr, e= 1, vis= 0 if status else 1)
		pm.textField(tcHost_txt, e= 1, tx= '', ed= 1 if status else 0)
		pm.textField(tcPort_txt, e= 1, tx= '', ed= 1 if status else 0)
		pm.columnLayout(remap_Area, e= 1, en= 1 if status else 0)
		pm.columnLayout(exect_Area, e= 1, en= 1 if status else 0)
	role_mqsb.onCmd = partial(role_mqsb_switch, 1)
	role_mqsb.offCmd = partial(role_mqsb_switch, 0)

	def op_btn_openPort(*args):
		addr = ''
		mode = 'LAN' if mode_mqsb.isChecked() else 'local'
		port_on = mark._portStatus()[0]
		if port_on:
			for p in port_on:
				if mode == 'LAN' and port_on[p]['ipaddr'].split(':')[0]:
					addr = port_on[p]['ipaddr']
				if mode == 'local' and not port_on[p]['ipaddr'].split(':')[0]:
					addr = port_on[p]['ipaddr']
		if not addr:
			addr = mark.portOpen(mode, 'python')
		host = addr.split(':')[0]
		port = addr.split(':')[1]
		pm.textField(tcHost_txt, e= 1, tx= str(host))
		pm.textField(tcPort_txt, e= 1, tx= str(port))
	pm.button(op_btn, e= 1, c= op_btn_openPort)

	def copyAddr(*args):
		host = pm.textField(tcHost_txt, q= 1, tx= 1)
		port = pm.textField(tcPort_txt, q= 1, tx= 1)
		addr = host + ':' + port
		pm.cmdScrollFieldExecuter(copypasteField, e= 1, clr= 1)
		pm.cmdScrollFieldExecuter(copypasteField, e= 1, t= addr)
		pm.cmdScrollFieldExecuter(copypasteField, e= 1, sla= 1)
		pm.cmdScrollFieldExecuter(copypasteField, e= 1, cp= 1)
	pm.button(cp_btn, e= 1, c= copyAddr)

	def pasteAddr(*args):
		pm.cmdScrollFieldExecuter(copypasteField, e= 1, clr= 1)
		pm.cmdScrollFieldExecuter(copypasteField, e= 1, pst= 1)
		addr = pm.cmdScrollFieldExecuter(copypasteField, q= 1, t= 1)
		host = addr.split(':')[0] if ':' in addr else ''
		port = addr.split(':')[1] if ':' in addr else ''
		pm.textField(tcHost_txt, e= 1, tx= host)
		pm.textField(tcPort_txt, e= 1, tx= port)
	pm.button(ps_btn, e= 1, c= pasteAddr)

	def saveTarget(*args):
		pm.textScrollList(trg_sls, e= 1, ra= 1)
		pm.textScrollList(trg_sls, e= 1, append= [str(i.name()) for i in pm.ls(sl= 1)])
	pm.button(svt_btn, e= 1, c= saveTarget)

	def addTarget(*args):
		ai = pm.textScrollList(trg_sls, q= 1, ai= 1)
		ai.extend([str(i.name()) for i in pm.ls(sl= 1)])
		ai = list(set(ai))
		pm.textScrollList(trg_sls, e= 1, ra= 1)
		pm.textScrollList(trg_sls, e= 1, append= ai)
	pm.button(adt_btn, e= 1, c= addTarget)

	def rmvTarget(*args):
		sel = pm.textScrollList(trg_sls, q= 1, si= 1)
		pm.textScrollList(trg_sls, e= 1, ri= sel)
	pm.button(rmt_btn, e= 1, c= rmvTarget)

	def _setConn():
		mode = 'LAN' if mode_mqsb.isChecked() else 'local'
		host = pm.textField(tcHost_txt, q= 1, tx= 1)
		port = pm.textField(tcPort_txt, q= 1, tx= 1)
		if port and ((mode == 'LAN' and host) or mode == 'local'):
			beam.setCoord(int(port), host= host)
			return True

	def checkConn(*args):
		if _setConn():
			beam.cmdSend('cmds.warning("[AniRemap] Connection Test Success.")', silent= 1)
	pm.button(ch_btn, e= 1, c= checkConn)
	
	def execRemap(*args):
		remapType = pm.optionMenu(match_mnu, q= 1, v= 1)
		tirm = tirm_mqsb.isChecked()
		sel_src = not hSrc_mqsb.isChecked()
		sel_dis = not hTrg_mqsb.isChecked()
		scale = pm.floatField(scale_flt, q= 1, v= 1)
		mirror = [None, 'X', 'Z', 'Y'][pm.radioButtonGrp('mirror_radioBtnGrp' , q= 1, sl= 1) - 1]
		if maya_mqsb.isChecked():
			if _setConn:
				mr.remoteRemap(beam, remapType, tirm, sel_src, sel_dis, scale, mirror)
		else:
			dis = [str(i.name()) for i in pm.textScrollList(trg_sls, q= 1, ai= 1)]
			mr.localRemap(dis, remapType, tirm, sel_src, sel_dis, scale, mirror)
	pm.button(remap_btn, e= 1, c= execRemap)

	def dockCloseCmd(*args):
		mark.portClose(0)
	pm.dockControl(windowName, area= 'right', content= main_window, allowedArea= ['right', 'left'], \
		vis= 1, s= 0, ret= 0, w= dockWidth, vcc= dockCloseCmd)



if __name__ == '__main__':
	ui_main()