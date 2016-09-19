# -*- coding:utf-8 -*-

import re


def remapNameMatch(src, dis):
	"""
	"""
	def rmNS(dagPath):
		''' clean up src namespace and leave basename '''
		return '|'.join([ dag.split(':')[-1] for dag in dagPath.split('|') ])

	keyMap = {}
	for ctrl in src:
		ctrlBN = rmNS(ctrl)
		reNS = '.*:' + ctrlBN.replace('|', '\|.*:')
		reBN = ctrlBN.replace('|', '\|')
		regex = re.compile(reNS + '|' + reBN)
		found = [m.group(0) for d in dis for m in [regex.search(d)] if m]
		if found:
			if len(found) == 1:
				# found only one match - great!
				keyMap[ctrl] = found[0]
			else:
				# found more than one match
				pass
		else:
			# no match found
			pass

	return keyMap


def remapSelectOrder(src, dis):
	"""
	"""
	keyMap = {}
	for i, ctrl in enumerate(src):
		if i < len(dis):
			keyMap[ctrl] = dis[i]
		else:
			# dis traget number is less than src, key lose
			pass

	return keyMap