import gurobipy
import numpy as np

def lp_parser(lpfile, verbose=True):
	model = gurobipy.read(lpfile)
	decision_vars = model.getVars()
	var_indices = {v: i for i, v in enumerate(decision_vars)}
	if verbose:
		print('Number of decision variables: %s'%len(decision_vars))

	constraints = model.getConstrs()
	constraint_names = [c.getAttr('ConstrName') for c in constraints]
	n_additional_objectives = 0
	for cname in constraint_names:
		if cname[0:3] == 'obj':
			n_additional_objectives += 1
	n_objectives = 1 + n_additional_objectives
	if verbose:
		print('Number of objectives: %s'%n_objectives)

	# Get the objective coefficients
	objective_coeffs = np.zeros([n_objectives,len(decision_vars)])
	objective_coeffs[0,:] = model.getAttr('Obj', decision_vars)
	for ao in range(n_additional_objectives):
		obj_constraint = constraints[len(constraints) - n_additional_objectives + ao]
		# check that the RHS is zero and the sense is '=='
		if obj_constraint.getAttr('ConstrName')[0:3] == 'obj' and not (obj_constraint.getAttr('RHS')==0.0):
			raise ValueError("Found an objective in the constraints with RHS not == 0.")
		elif obj_constraint.getAttr('ConstrName')[0:3] == 'obj':
			expression = model.getRow(obj_constraint)
			for term in range(expression.size()):
				var = expression.getVar(term)
				dvar_idx = var_indices[var]
				coeff = expression.getCoeff(term)
				objective_coeffs[1 + ao, dvar_idx] = coeff
	
	# Get the constraint coefficients, RHS
	n_constraints = len(constraints) - n_additional_objectives
	if verbose:
		print('Number of constraints: %s'%n_constraints)
	A = np.zeros([n_constraints, len(decision_vars)])
	RHS = np.zeros([n_constraints,1])
	sense = [0]*n_constraints
	for c in range(n_constraints):
		constraint = constraints[c]
		expression = model.getRow(constraint)
		for term in range(expression.size()):
			var = expression.getVar(term)
			dvar_idx = var_indices[var]
			coeff = expression.getCoeff(term)
			A[c, dvar_idx] = coeff
		RHS[c, 0] = constraint.getAttr('RHS')
		sense[c] = constraint.getAttr('Sense')

	# Get lb, ub and vartypes
	lb = np.zeros([len(decision_vars), 1])
	ub = np.zeros([len(decision_vars), 1])
	vtype = [0]*len(decision_vars)
	for v in decision_vars:
		lb[var_indices[v]] = v.getAttr('LB')
		ub[var_indices[v]] = v.getAttr('UB')
		vtype[var_indices[v]] = v.getAttr('VType')
	
	prob_data = dict()
	prob_data['n_dvars'] = len(decision_vars)
	prob_data['n_obj'] = n_objectives
	prob_data['n_constr'] = n_constraints
	prob_data['obj_coeff'] = objective_coeffs
	prob_data['constr_coeff'] = A
	prob_data['constr_RHS'] = RHS
	prob_data['constr_sense'] = sense
	prob_data['lb'] = lb
	prob_data['ub'] = ub
	prob_data['vartype'] = vtype
	return prob_data



# lp_parser('../BOKP+lp+format+instances/kp_160_3.lp')

