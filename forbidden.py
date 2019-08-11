'''#The Forbidden module
---
The idea is simple;

1. Take a python data structure ( only dicts and lists for now ) 
and then return a serialized text format called *forbidden*.
2. Take an already serialized *forbidden* format and return the appropriate python data structure.
---
Examples:
---
#### 1.List & Tuples
| Python Lists & Tuples                                 | Forbidden                                                   |
|:-----------------------------------------------------:|:-----------------------------------------------------------:|
| ['abc','def','ghi','jkl','mno','pqr','stu']           | abc`0``def`0``ghi`0``jkl`0``mno`0``pqr`0``stu               |
| [['ab','cd','ef'],['gh','ij','kl'],['mn','op','qr']]  | ab`1``cd`1``ef`1```0``gh`1``ij`1``kl`1```0``mn`1``op`1``qr` |
| [[['ab','cd'],['ef','gh']],[['ij','kl'],['mn','op']]] | ab`2``cd`1``ef`2``gh`0``ij`2``kl`1``mn`2``op            |

#### 2.Dictionary
| Python Dictionaries                                   | Forbidden                                                   |
|:-----------------------------------------------------:|:-----------------------------------------------------------:|
||
||
||

Note
===
There are only two data types possible here, 
1. Numbers (float)
2. Strings
'''
import re

ALLOWED = "allowed"
FORBIDDEN = "forbidden"

def str_to_num(str):
	return float(str) if '.' in str else int(str)


class Forbidden():
	'''Forbidden Class'''

	def __init__(self,data,forbidden_char='`',forbidden_alias=''):
		'''Class constructor
		:param data: could be a list, dictionary, set, array ...
		it could also be a forbidden_string format ...
		:param forbidden_char: is the only character that is not allowed in your data
		the default character is the grave character, hence "forbidden grave".
		'''
		self.reset(data,forbidden_char,forbidden_alias)

	def forbid(self):
		'''
		convert data to forbidden_string format using a hidden recursive sibbling
		for now recieve only lists and dicts
		'''
		if self._data_type == FORBIDDEN:
			return self._data
		data = self._data
		return self._forbid_recursive_no_keys(data)

	def _forbid_recursive_no_keys(self,data,depth=0):
		glue = self.join_at(depth)
		if not any(isinstance(element,(list,tuple)) for element in data):
			return data if isinstance(data,str) else glue.join(data)
		else:
			elements = []
			for element in data:
				elements.append(self._forbid_recursive_no_keys(element,depth+1))
			return self._forbid_recursive_no_keys(elements,depth)

	def allow(self):
		'''
		convert data to python data type, like list, dict ...
		for now return only lists and dicts
		'''
		data = self.forbid() if self._data_type == ALLOWED else self._data
		return self._allow_recursive_no_keys(data,depth=0)

	def _allow_recursive_no_keys(self,data,depth=0):
		glue = self.join_at(depth)
		if isinstance(data,str) and glue in data:
			elements = []
			for element in data.split(glue):
				elements.append(self._allow_recursive_no_keys(element,depth+1))
			return elements
		else:
			return data.strip('"') if '"' in data else str_to_num(data)
			


	def reset(self,data,forbidden_char='`',forbidden_alias=''):
		'''
		reset a forbidden object, in case you need to pass in different data
		'''
		self._data_type = FORBIDDEN if isinstance(data,str) else ALLOWED
		self._data = data
		self.forbidden_char = forbidden_char
		self.forbidden_alias = forbidden_alias
		self._clean()

	def join_at(self,depth):
		'''join_at defines the join string
		:param depth: refers to the depth of the data, in particular the python data
		'''
		join_string = '{}{}{}'.format(self.forbidden_char,depth,self.forbidden_char*2)
		return join_string

	def _clean(self):
		'''Replace forbidden_char from allowed data with forbidden_alias'''

		if self._data_type == FORBIDDEN:
			pass
		else:
			self._data = list(map(self._clean_recursive,self._data))


	def _clean_recursive(self,data):
		if isinstance(data,str):
			return '"'+data.replace(self.forbidden_char,self.forbidden_alias)+'"'
		elif isinstance(data,list):
			return list(map(self._clean_recursive,data))
		elif isinstance(data,tuple):
			return tuple(map(self._clean_recursive,data))
		elif isinstance(data,dict):
			return dict(map(self._clean_recursive,data))
		else:
			return str(data)

