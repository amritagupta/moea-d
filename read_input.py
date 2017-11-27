#!/opt/python/bin/python
import re
import numpy as np

def read_input(filename):
	with open(filename, 'rb') as data:
		lines = data.readlines()
		lines = [x.rstrip() for x in lines]
	marker_strings = ['Minimize', 'Subject To', 'Bounds', 'Binaries', 'End']
	objectives = []
	binaries = []

	# FIND NUMBER OF X AND Y VARIABLES AND NUMBER OF CONSTRAINTS
	x_len = 0
	y_len = 0
	n_constraints = 0
	for line in lines:
		if line in marker_strings:
			pass
		elif (line[0:2] == ' o') or (line[0:2] == ' c') or (line[0:2] == '  '):
			line_chars = line[5:].split()
			for lc in line_chars:
				lc_split = re.split('\(|\)', lc)
				if lc_split[0] == 'x':
					x_len = max(x_len, int(lc_split[1]))
				if lc_split[0] == 'y':
					y_len = max(y_len, int(lc_split[1]))
			if line[0:2] == ' c':
				n_constraints += 1
	n_constraints -= 1 # the last constraint is another objective
	
	# CREATE OBJECTIVE VECTORS
	# OBJECTIVE 1:
	o1_coeff = np.zeros([1,1+x_len+1+y_len])
	o1_terms = []
	started_constraints = False
	for line in lines:
		started_constraints = True if line == 'Subject To' else started_constraints
		if not started_constraints:
			if (line[0:2] == ' o') or (line[0:2] == '  '):
				line_terms = line.split()
				o1_terms += line_terms
		if started_constraints:
			break
	
	o1 = "".join(o1_terms)[4:]
	o1_terms2 = re.split('\)', o1)
	for term in o1_terms2[0:len(o1_terms2) - 1]:
		mult_and_xy_idx = re.split('\(',term)
		if mult_and_xy_idx[0][-1] == 'x':
			if mult_and_xy_idx[0] == 'x':
				o1_coeff[0,int(mult_and_xy_idx[1])] = 1
			elif mult_and_xy_idx[0][0:-1] not in ['+', '-']:
				o1_coeff[0,int(mult_and_xy_idx[1])] = int(mult_and_xy_idx[0][0:-1])
			elif mult_and_xy_idx[0][0:-1] == '+':
				o1_coeff[0,int(mult_and_xy_idx[1])] = 1
			elif mult_and_xy_idx[0][0:-1] == '-':
				o1_coeff[0,int(mult_and_xy_idx[1])] = -1
		elif mult_and_xy_idx[0][-1] == 'y':
			if mult_and_xy_idx[0] == 'y':
				o1_coeff[0,1 + x_len + int(mult_and_xy_idx[1])] = 1
			elif mult_and_xy_idx[0][0:-1] not in ['+', '-']:
				o1_coeff[0,1 + x_len + int(mult_and_xy_idx[1])] = int(mult_and_xy_idx[0][0:-1])
			elif mult_and_xy_idx[0][0:-1] == '+':
				o1_coeff[0,1 + x_len + int(mult_and_xy_idx[1])] = 1
			elif mult_and_xy_idx[0][0:-1] == '-':
				o1_coeff[0,1 + x_len + int(mult_and_xy_idx[1])] = -1

	objectives.append(o1_coeff[0])

	# OBJECTIVE 2:
	leading_chars = ' c'+str(n_constraints+1)
	o2_coeff = np.zeros([1,1+x_len+1+y_len])
	o2_terms = []
	last_constraint_line_no = 0
	for line in lines:
		if not line[0:len(leading_chars)] == leading_chars:
			last_constraint_line_no += 1
		else:
			break
	o2_terms += lines[last_constraint_line_no].split()
	while lines[last_constraint_line_no+1] != 'Bounds':
		o2_terms += lines[last_constraint_line_no+1].split()
		last_constraint_line_no += 1
	o2 = "".join(o2_terms[1:])
	o2_terms2 = re.split('\)', o2)
	for term in o2_terms2[0:len(o2_terms2) - 1]:
		mult_and_xy_idx = re.split('\(',term)
		if mult_and_xy_idx[0][-1] == 'x':
			if mult_and_xy_idx[0] == 'x':
				o2_coeff[0,int(mult_and_xy_idx[1])] = 1
			elif mult_and_xy_idx[0][0:-1] not in ['+', '-']:
				o2_coeff[0,int(mult_and_xy_idx[1])] = int(mult_and_xy_idx[0][0:-1])
			elif mult_and_xy_idx[0][0:-1] == '+':
				o2_coeff[0,int(mult_and_xy_idx[1])] = 1
			elif mult_and_xy_idx[0][0:-1] == '-':
				o2_coeff[0,int(mult_and_xy_idx[1])] = -1
		elif mult_and_xy_idx[0][-1] == 'y':
			if mult_and_xy_idx[0] == 'y':
				o2_coeff[0,1 + x_len + int(mult_and_xy_idx[1])] = 1
			elif mult_and_xy_idx[0][0:-1] not in ['+', '-']:
				o2_coeff[0,1 + x_len + int(mult_and_xy_idx[1])] = int(mult_and_xy_idx[0][0:-1])
			elif mult_and_xy_idx[0][0:-1] == '+':
				o2_coeff[0,1 + x_len + int(mult_and_xy_idx[1])] = 1
			elif mult_and_xy_idx[0][0:-1] == '-':
				o2_coeff[0,1 + x_len + int(mult_and_xy_idx[1])] = -1

	objectives.append(o2_coeff[0])

	# CREATE CONSTRAINTS
	A = np.zeros([n_constraints, 1 + x_len + 1 + y_len])
	b = np.zeros([n_constraints,1])
	started_constraints = False
	constraint_no = 0
	constraint_start_line_no = 0
	for line in lines:
		started_constraints = True if line == 'Subject To' else started_constraints
		constraint_start_line_no += 1
		if started_constraints:
			break
	constraints_left = True
	while constraints_left:
		constraint_terms = lines[constraint_start_line_no].split()
		while lines[constraint_start_line_no+1][0:2] != ' c':
			constraint_start_line_no += 1
			constraint_terms += lines[constraint_start_line_no].split()
		c = "".join(constraint_terms[1:])
		c_terms = re.split('\)', c)
		for term in c_terms[0:len(c_terms) - 1]:
			mult_and_xy_idx = re.split('\(',term)
			if mult_and_xy_idx[0][-1] == 'x':
				if mult_and_xy_idx[0][0:-1] == '+':
					A[constraint_no,int(mult_and_xy_idx[1])] = 1
				elif mult_and_xy_idx[0][0:-1] == '-':
					A[constraint_no,int(mult_and_xy_idx[1])] = -1
				elif mult_and_xy_idx[0][0:-1] == 'x':
					A[constraint_no,int(mult_and_xy_idx[1])] = 1
				elif mult_and_xy_idx[0] == 'x':
					A[constraint_no,int(mult_and_xy_idx[1])] = 1
				else:
					A[constraint_no,int(mult_and_xy_idx[1])] = int(mult_and_xy_idx[0][0:-1])
			elif mult_and_xy_idx[0][-1] == 'y':
				if mult_and_xy_idx[0][0:-1] == '+':
					A[constraint_no,1 + x_len + int(mult_and_xy_idx[1])] = 1
				elif mult_and_xy_idx[0][0:-1] == '-':
					A[constraint_no,1 + x_len + int(mult_and_xy_idx[1])] = -1
				elif mult_and_xy_idx[0][0:-1] == 'y':
					A[constraint_no,1 + x_len + int(mult_and_xy_idx[1])] = 1
				elif mult_and_xy_idx[0] == 'y':
					A[constraint_no,1 + x_len + int(mult_and_xy_idx[1])] = 1
				else:
					A[constraint_no,1 + x_len + int(mult_and_xy_idx[1])] = int(mult_and_xy_idx[0][0:-1])
		b[constraint_no] = int(c_terms[len(c_terms)-1][2:])
		constraint_start_line_no += 1
		constraint_no += 1
		if constraint_no > n_constraints - 1:
			constraints_left = False
	
	# GET ALL BOUNDS
	lb = -np.inf*np.ones([1+x_len+1+y_len, 1])
	ub = np.inf*np.ones([1+x_len+1+y_len, 1])
	started_bounds = False
	bounds_start_line_no = 0
	for line in lines:
		started_bounds = True if line == 'Bounds' else started_bounds
		bounds_start_line_no += 1
		if started_bounds:
			break
	started_binaries = False
	binaries_start_line_no = 0
	for line in lines:
		started_binaries = True if line == 'Binaries' else started_binaries
		binaries_start_line_no += 1
		if started_binaries:
			break
	for lineno in range(bounds_start_line_no, binaries_start_line_no-1):
		linedata = lines[lineno].split()
		if linedata[2][0] == 'x':
			lb[int(linedata[2][-2])] = int(linedata[0])
			ub[int(linedata[2][-2])] = int(linedata[4])
		if linedata[2][0] == 'y':
			lb[1 + x_len + int(linedata[2][-2])][0] = int(linedata[0])
			ub[1 + x_len + int(linedata[2][-2])] = int(linedata[4])

	# GET WHICH VARIABLES ARE BINARY
	binary = [0]*(1+x_len+1+y_len)
	binlist = lines[binaries_start_line_no]
	binlist = binlist.split()
	for var in binlist:
		var = re.split('\(|\)',var)
		if var[0] == 'x':
			binary[int(var[1])] = 1
		elif var[0] == 'y':
			binary[1+x_len+int(var[1])] = 1

	return objectives, A, b, lb, ub, binary



    # rd = []
    # with open('zdt1.lp', 'rb') as ex:
    #     rd = list(csv.reader(ex, skipinitialspace=True))
    #     rd = [i for i in rd if i]
read_input('BOMIP_LP_Instances/C20/5dat.lp')
