# -*- coding: utf-8 -*-

import os
from typeWorld.api import *
from typeWorld.api.base import *
from ynlib.files import WriteToFile, ReadFromFile

api = APIRoot()

docstrings = api.docu()
docstring = ReadFromFile(os.path.join(os.path.dirname(__file__), 'typeWorld', 'docu.md'))




handles = []
for key in [x[0] for x in docstrings]:
	if not key in handles:
		handles.append(key)

classTOC = ''
for handle in handles:
	classTOC += '- [%s](#user-content-class-%s)<br />\n' % (handle, handle.lower())
classTOC += '\n\n'

docstring = docstring.replace('__classTOC__', classTOC)

for handle in handles:
	for className, string in docstrings:
		if handle == className:
			docstring += string
			docstring += '\n\n'
			break



if not 'TRAVIS' in os.environ:
	WriteToFile(os.path.join(os.path.dirname(__file__), 'typeWorld', 'README.md'), docstring)
