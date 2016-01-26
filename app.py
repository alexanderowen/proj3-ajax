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
# import acp_limits


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


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("calc")
    return flask.render_template('page_not_found.html'), 404

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
  #controls is of the form (control loc in km, minimum speed, maximum speed)
  controls = [(200,15,34), (400,15,32), (600,15,30), (1000,11.428,28)] 
  dist = request.args.get('dist', 0, type=int)
  start_t = request.args.get('start_t', 0, type=str)
  start_d = request.args.get('start_d', 0, type=str)
  
  rslt = {"opening" : "", "closing" : ""}
  
  
  for control in controls:
    km, min, max = control
    if dist <= km:
      time_str = "{} {}".format(start_d, start_t)
      time = arrow.get(time_str, "MM/DD/YYYY HH:mm")
      break
      
  h_min = int(dist/min)
  m_min = round(60 * (dist/min - h_min))  
  closing = time.replace(hours=+h_min, minutes=+m_min)
  closing = str(closing.time())
  
  h_max = int(dist/max)
  m_max = round(60 * (dist/max - h_max))  
  opening = time.replace(hours=+h_max, minutes=+m_max)
  opening = str(opening.time())
  
  rslt["closing"] = closing
  rslt["opening"] = opening
  
  return jsonify(result=rslt)
 
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



#############


if __name__ == "__main__":
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug=CONFIG.DEBUG
    app.logger.setLevel(logging.DEBUG)
    app.run(port=CONFIG.PORT)

    
