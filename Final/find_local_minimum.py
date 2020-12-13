def find_local_minimum(func,n):
	"""
	Input:
		an arbitrary funciton: func of n variables, the func takes in a sequence to evaluate
							   the input
		an integer: n representing the number of variables that func has
	Output:
		a sequence: the location of a local minimum of func in the form of (x1,x2,x3...,xn)
					where x1,x2,x3,x4....xn are all fractional numbers representing the coordinates
					of the location of the point
	"""
	result_location = []
	for i in range(n):
		result_location.append(0)

	for i in range(n):
		proceed_length = 0.001
		new_location_one = list(result_location)
		new_location_two = list(result_location)
		
		new_location_one[-1*i-1] = new_location_one[-1*i-1] + proceed_length
		new_location_two[-1*i-1] = new_location_two[-1*i-1] - proceed_length

		one_dimensional_minimum = func(result_location)
		while func(new_location_one)<one_dimensional_minimum or func(new_location_two)<one_dimensional_minimum:
			if func(new_location_one)<one_dimensional_minimum:
				result_location = new_location_one
			else:
				result_location = new_location_two
			
			new_location_one = list(result_location)
			new_location_two = list(result_location)
			new_location_one[-1*i-1] = new_location_one[-1*i-1] + proceed_length
			new_location_two[-1*i-1] = new_location_two[-1*i-1] - proceed_length

	return result_location
