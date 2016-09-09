a = ['lll:abc']
b = ['ccc:abc']
import re
aaa = re.compile('.*:abc')
[m.group(0) for l in a for m in [aaa.search(l)] if m]




rd.cmdSend('from __main__ import *;kk()')