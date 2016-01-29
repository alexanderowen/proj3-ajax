"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for
from flask import jsonify # For AJAX transactions

import json
import logging


# Date handling 
import arrow # Replacement for datetime, based on moment.js
import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# For Favicon loading
import os

# Our own module
import acp_calc

###
# Globals
###
app = flask.Flask(__name__)
import CONFIG

import uuid
app.secret_key = str(uuid.uuid4())
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)

###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/calc")
def index():
  app.logger.debug("Main page entry")
  return flask.render_template('calc.html')

@app.route('/favicon.ico')
def favicon():
    return flask.send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

###############
#
# AJAX request handlers 
#   These return JSON, rather than rendering pages. 
#
###############
@app.route("/_calc_times")
def calc_times():
  """
  Calculates open/close times from kilometers, using rules 
  described at http://www.rusa.org/octime_alg.html.
  Expects one URL-encoded argument, the number of kilometers. 
  """
  dist = request.args.get('dist', 0, type=int)
  dist_unit = request.args.get('dist_unit', 0, type=str)
  start_t = request.args.get('start_t', 0, type=str)
  start_d = request.args.get('start_d', 0, type=str)
  brev_length = request.args.get('brev_length', 0, type=int)  
  
  time_str = "{} {}".format(start_d, start_t)
  time = arrow.get(time_str, "MM/DD/YYYY HH:mm")
  
  opening, closing = acp_calc.acp_times(brev_length, dist, dist_unit, time)
  
  # Date formatting
  ctime = str(closing.time())[:5]
  cmonth = str(closing.date())[5:7]
  cdate = str(closing.date())[8:]
  closing = "{}/{}    {}".format(cmonth, cdate, ctime)
  
  otime = str(opening.time())[:5]
  omonth = str(opening.date())[5:7]
  odate = str(opening.date())[8:]
  opening = "{}/{}    {}".format(omonth, odate, otime)
  
  rslt = {"opening": opening, "closing": closing}  
  return jsonify(result=rslt)
 

@app.route("/_is_valid_date")
def is_valid_date():
	"""
	Determines if a given date is valid. Format required: MM/DD/YYYY
	"""
	date_str = request.args.get('date', 0, type=str)
	try:
		arrow.get(date_str, "MM/DD/YYYY")
	except:
		return jsonify(result={"is_valid": False})
	return jsonify(result={"is_valid": True})

	
@app.route("/_is_valid_time")
def is_valid_time():
	"""
	Determines if a given time is valid. Format required: MM:mm
	"""
	time_str = request.args.get('time', 0, type=str)
	try:
		arrow.get(time_str, "HH:mm")
	except:
		return jsonify(result={"is_valid": False})
	return jsonify(result={"is_valid": True})
 	
#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"

@app.template_filter( 'fmttime' )
def format_arrow_time( time ):
    try: 
        normal = arrow.get( date )
        return normal.format("hh:mm")
    except:
        return "(bad time)"

###################
#   Error handlers
###################
@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return render_template('page_not_found.html'), 404

@app.errorhandler(500)
def error_500(e):
   app.logger.warning("++ 500 error: {}".format(e))
   assert app.debug == False #  I want to invoke the debugger
   return render_template('500.html'), 500

@app.errorhandler(403)
def error_403(e):
  app.logger.warning("++ 403 error: {}".format(e))
  return render_template('403.html'), 403

#############

if __name__ == "__main__":
    # Standalone. 
    app.debug = True
    app.logger.setLevel(logging.DEBUG)
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
else:
    # Running from cgi-bin or from gunicorn WSGI server, 
    # which makes the call to app.run.  Gunicorn may invoke more than
    # one instance for concurrent service.
    app.debug=False
    
