
"""
load_config v0.01 

configuration loader

Copyright 2011 Brian Monkaba

This file is part of ga-bitbot.

    ga-bitbot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ga-bitbot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ga-bitbot.  If not, see <http://www.gnu.org/licenses/>.
"""

import json

config_path = "./config/"

def load_config_from_file(config_filename):
	"""
	load_config_from_file(config_filename)
	--------------------------------------

	Loads a json data structure from a local file
	Returns a dictionary 
	"""
	f = open(config_path + config_filename,'r')
	config_dict = json.loads(f.read())
	f.close()
	return config_dict

def load_config_into_object(config_dict,obj):
	"""
	load_config_into_object(config_dict,obj)
	----------------------------------------

	Loads a dictionary into a class object. supports two root keys, set and call

	The set value contains key/value pairs which are loaded into the class objects variables

		set:{"variable_name_1":value,"variable_name_2":value, ... }

	The call child keys contain the class functions to be called 
		- each function value is a list of argument lists which are applied to each function

		call:{"function_1":[[arg1,arg2, ... ], [ ... ] ],"function_2":[[arg1,arg2, ... ], [ ... ] ] } 

		example resultant call:  function_1(arg1,arg2, ...)

	Returns the updated class object
	"""
	if 'set' in config_dict:
		for key in obj.__dict__:
			if key in config_dict['set']:
				obj.__dict__[key] = config_dict['set'][key]
				print "load_config_into_object: %s set to %s"%(key,str(config_dict['set'][key]))
	if 'call' in config_dict:
		for func in config_dict['call']:
			#print type(func),func
			for args in config_dict['call'][func]:
				#print type(args),args
				apply(getattr(obj,func),args)
				print "load_config_into_object: called func: %s with args: %s"%(func,args)

	return obj

def load_config_file_into_object(config_file,obj):
	return load_config_into_object(load_config_from_file(config_file),obj)


if __name__ == "__main__":
	#just some test code
	import genetic

	print load_config_from_file.__doc__

	d = load_config_from_file("mtgox_user.json")
	for key in d.keys():
		print key,":",d[key]


	d = load_config_from_file("gene_def.json")
	for key in d.keys():
		print key,":",d[key]


	print load_config_into_object.__doc__

	g = genetic.genepool()
	g = load_config_into_object(load_config_from_file("gene_def.json"),g)

	g = load_config_file_into_object("gene_def.json",g)

	print g.pool_size
	print g.contains

