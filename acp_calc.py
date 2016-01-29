"""
Determines ACP times based on data`
"""

import arrow

controls = [(200,15,34), (400,15,32), (600,15,30), (1000,11.428,28)] 
time_limits = {200: (13,30), 300: (20,00), 400: (27,00), 600: (40,00), 1000: (75,00)}

def miles_to_km(miles):
	"""
	Converts miles to km
	"""
	return miles * 1.61
	
def acp_times(brevet_length, dist, dist_unit, dt):
	"""
	dt  datetime, arrow object representing the start time and date
	dist  distance in either km or miles
	dist_unit   'miles' or 'kilometers'
	brevet_length  length of brevet 
	
	(str, str)
	returns a tuple of the form (opening time, closing time)
	"""
	opening, closing = dt, dt
	if dist == 0:  #simple base case
		return (opening, closing.replace(hours=+1))
		
	if dist_unit == "Miles":
		dist = miles_to_km(dist)	
		
	error = brevet_length + (brevet_length * .2)
	if dist > brevet_length and dist <= error:  # allow some overage, but treat dist as brev_len
		dist = brevet_length
	
	#begin acp algorithm
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
			break_flag = True  #it's time to finish
		ho = int(working_km/max)
		mo = round(60 * (working_km/max - ho))
		opening = opening.replace(hours=+ho, minutes=+mo)
		
		hc = int(working_km/min)
		mc = round(60 * (working_km/min - hc))
		closing = closing.replace(hours=+hc, minutes=+mc) 	
	
	if dist >= brevet_length:  # if dist >= brevet, then closing needs to be adjusted
		h, m = time_limits[brevet_length]		
		closing = dt.replace(hours=+h, minutes=+m)
	
	return (opening, closing)

def get_opening(brevet_length, dist, dt):
	"""
	gets the opening time
	"""
	opening = dt	
	if dist == 0:
		return opening
	
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
			break_flag = True
		h = int(working_km/max)
		m = round(60 * (working_km/max - h))
		opening = opening.replace(hours=+h, minutes=+m)
			
	return opening
	
def get_closing(brevet_length, dist, dt):
	"""
	gets the closing time
	"""
	closing = dt
	if dist == 0:  #two cases that require little computation
		return closing.replace(hours=+1)

	
	
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
			break_flag = True
		h = int(working_km/min)
		m = round(60 * (working_km/min - h))
		closing = closing.replace(hours=+h, minutes=+m) 
	return closing
	
