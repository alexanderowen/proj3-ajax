"""
Nose tests for acp_calc.py

Test cases are based on
Date: 01/01/2016
Time: 00:00
"""
from acp_calc import *
import arrow

d = arrow.get("01/01/2016 00:00", "MM/DD/YYYY HH:mm")
fmt = "MM/DD/YYYY HH:mm"

def test_0km_acp_times():
	"""
	Control at zero should be (start_time, start_time + 1 hour)
	"""
	d1 = arrow.get("01/01/2016 00:00", fmt)
	d2 = arrow.get("01/01/2016 01:00", fmt)
	assert acp_times(200, 0, "Kilometers", d) == (d1, d2)
	
def test_200km_acp_times():
	"""
	Testing various control distances for 200km brevet
	"""
	d1 = arrow.get("01/01/2016 00:02", fmt)
	d2 = arrow.get("01/01/2016 00:04", fmt)
	assert acp_times(200, 1, "Kilometers", d) == (d1, d2)
	
	d1 = arrow.get("01/01/2016 01:28", fmt)
	d2 = arrow.get("01/01/2016 03:20", fmt)	
	assert acp_times(200, 50, "Kilometers", d) == (d1, d2)
	
	d1 = arrow.get("01/01/2016 05:51", fmt)
	d2 = arrow.get("01/01/2016 13:16", fmt)		
	assert acp_times(200, 199, "Kilometers", d) == (d1, d2)
	
	d1 = arrow.get("01/01/2016 05:53", fmt)
	d2 = arrow.get("01/01/2016 13:30", fmt)
	assert acp_times(200, 200, "Kilometers", d) == (d1, d2)

	d1 = arrow.get("01/01/2016 05:53", fmt)
	d2 = arrow.get("01/01/2016 13:30", fmt)
	assert acp_times(200, 205, "Kilometers", d) == (d1, d2)
	
def test_1000km_acp_times():
	"""
	Testing various control distances for a 1000km brevet
	"""
	
	d1 = arrow.get("01/01/2016 05:53", fmt)
	d2 = arrow.get("01/01/2016 13:20", fmt)
	assert acp_times(1000, 200, "Kilometers", d) == (d1, d2)
	
	d1 = arrow.get("01/01/2016 07:27", fmt)
	d2 = arrow.get("01/01/2016 16:40", fmt)
	assert acp_times(1000, 250, "Kilometers", d) == (d1, d2)
	
	d1 = arrow.get("01/01/2016 12:08", fmt)
	d2 = arrow.get("01/02/2016 02:40", fmt)
	assert acp_times(1000, 400, "Kilometers", d) == (d1, d2)

	d1 = arrow.get("01/01/2016 13:48", fmt)
	d2 = arrow.get("01/02/2016 06:00", fmt)	
	assert acp_times(1000, 450, "Kilometers", d) == (d1, d2)
	
	d1 = arrow.get("01/01/2016 18:48", fmt)
	d2 = arrow.get("01/02/2016 16:00", fmt)	
	assert acp_times(1000, 600, "Kilometers", d) == (d1, d2)
	
	d1 = arrow.get("01/01/2016 20:35", fmt)
	d2 = arrow.get("01/02/2016 20:23", fmt)	
	assert acp_times(1000, 650, "Kilometers", d) == (d1, d2)
	
	d1 = arrow.get("01/02/2016 05:09", fmt)
	d2 = arrow.get("01/03/2016 17:23", fmt)	
	assert acp_times(1000, 890, "Kilometers", d) == (d1, d2)
	
	d1 = arrow.get("01/02/2016 09:03", fmt)
	d2 = arrow.get("01/04/2016 02:55", fmt)	
	assert acp_times(1000, 999, "Kilometers", d) == (d1, d2)
	
	d1 = arrow.get("01/02/2016 09:05", fmt)
	d2 = arrow.get("01/04/2016 03:00", fmt)	
	assert acp_times(1000, 1000, "Kilometers", d) == (d1, d2)
	
	d1 = arrow.get("01/02/2016 09:05", fmt)
	d2 = arrow.get("01/04/2016 03:00", fmt)	
	assert acp_times(1000, 1001, "Kilometers", d) == (d1, d2)
	

def test_miles_acp_times():
	"""
	Testing that miles to kilometer conversion is working properly
	"""

	d1 = arrow.get("01/01/2016 20:22", fmt)
	d2 = arrow.get("01/02/2016 19:51", fmt)
	assert acp_times(1000, 400, "Miles", d) == (d1, d2)
	
	d1 = arrow.get("01/02/2016 07:52", fmt)
	d2 = arrow.get("01/04/2016 00:02", fmt)
	assert acp_times(1000, 600, "Miles", d) == (d1, d2)
	
	d1 = arrow.get("01/02/2016 09:05", fmt)
	d2 = arrow.get("01/04/2016 03:00", fmt)
	assert acp_times(1000, 630, "Miles", d) == (d1, d2)
	


	