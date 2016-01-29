"""
Determines ACP times based on data
"""

import arrow

##  Globals
controls = [(200,15,34), (400,15,32), (600,15,30), (1000,11.428,28)] 
time_limits = {200: (13,30), 300: (20,00), 400: (27,00), 600: (40,00), 1000: (75,00)}

def miles_to_km(miles):
	"""
	Converts miles to kilometers
	"""
	return miles * 1.61
	
def acp_times(brevet_length, dist, dist_unit, dt):
	"""
	ACP time algorithm following description at: http://www.rusa.org/octime_alg.html
	Given data, determines the opening and closing time for control distances
	Args:
		brevet_length: int, the total length of the brevet. 
		dist: int, control distance in the brevet. 
		dist_unit: str, either "Kilometers" or "Miles"
		dt: Arrow obj, object representing the start time of the brevet
	Returns:
		A tuple in the form of (arrow, arrow), the opening and closing times based
		on the control location
	"""
	opening, closing = dt, dt
	if dist == 0:    #  Simple case: control distance is 0
		return (opening, closing.replace(hours=+1))
		
	if dist_unit == "Miles":
		dist = miles_to_km(dist)	
		
	error = brevet_length + (brevet_length * .2)
	if dist > brevet_length and dist <= error:  # Allow 20% overage, but treat control distance as brevet length
		dist = brevet_length
	
	# General case, ACP algorithm
	km_count = 0 
	break_flag = False
	for control in controls:
		if break_flag:
			break
	
		km, min, max = control
		if dist >= km:
			working_km = km - km_count
			km_count += working_km
		else:
			working_km = dist - km_count
			break_flag = True  # Exit loop on next iteration
		ho = int(working_km/max)
		mo = round(60 * (working_km/max - ho))
		opening = opening.replace(hours=+ho, minutes=+mo)
		
		hc = int(working_km/min)
		mc = round(60 * (working_km/min - hc))
		closing = closing.replace(hours=+hc, minutes=+mc) 	
	
	if dist >= brevet_length:  #  Closing time needs to be adjusted in this case
		h, m = time_limits[brevet_length]		
		closing = dt.replace(hours=+h, minutes=+m)
	
	return (opening, closing)
	
