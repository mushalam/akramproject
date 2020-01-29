from __future__ import print_function

import json
import os
from datetime import datetime
from functools import wraps

from bokeh.embed import json_item
from bokeh.models import Range1d
from bokeh.plotting import figure
from bokeh.resources import CDN
from flask import Flask, render_template, request, url_for, redirect, session
from flask_pymongo import PyMongo
from jinja2 import Template

import db

app = Flask(__name__)

# Needed for sessions to work properly
app.secret_key = 'AD83nsod3#Qo,c0e3n(CpamwdiN"Lancznpawo.j3eOMAPOM;CAXMALSMD343672'

page = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    {{ resources }}
    <meta charset="utf-8">
    
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <title>HomeSecu - Data</title>
    <!-- Bootstrap core CSS -->
    <link href="/static/vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">
    <!-- Custom fonts for this template -->
    <link href="/static/vendor/fontawesome-free/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Varela+Round" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="/static/css/grayscale.min.css" rel="stylesheet">
    <link href="/static/css/custom.css" rel="stylesheet">
</head>
<body id="page-top">
<!-- Navigation -->
<nav class="navbar navbar-expand-lg navbar-light fixed-top navbar-shrink" id="mainNav_2">
    <div class="container">
        <a class="navbar-brand js-scroll-trigger" href={{ main_url }}>H0m3_S3cu_1</a>
        <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse"
                data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false"
                aria-label="Toggle navigation">
            Menu
            <i class="fas fa-bars"></i>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
            <ul class="navbar-nav ml-auto">
                <li class="nav-item"><a class="nav-link js-scroll-trigger" href="{{ main_url }}">Home</a></li>
                <li class="nav-item"><a class="nav-link js-scroll-trigger" href="#projects">Measurements</a></li>
                <li class="nav-item"><a class="nav-link" href="{{ logout_url }}"> Logout </a></li>
            </ul>
        </div>
    </div>
</nav>

<!-- INFRA RED LIGHT -->
<section id="projects" class="projects-section bg-light">
    <div class="container">
        <div class="row align-items-center no-gutters mb-4 mb-lg-5" id='anchor1'>
            <div class="col-xl-4 col-lg-5"><div class="featured-text text-center text-lg-left"><h4>Infrared sensor</h4></div></div>
            <div class="col-xl-8 col-lg-7"><div class="img-fluid mb-3 mb-lg-0">
            <a href=#anchor1 id=ir><button class="btn btn-primary" name="ir" onclick="toggleGraph('irplot')">Show data</button></a>
            </div></div><div id="refresh"><div style="display: none" id="irplot"></div></div></div>
        
        <div class="row align-items-center no-gutters mb-4 mb-lg-5" id='anchor2'>
            <div class="col-xl-4 col-lg-5"><div class="featured-text text-center text-lg-left"><h4>Light</h4></div></div>
            <div class="col-xl-8 col-lg-7">
                <div class="img-fluid mb-3 mb-lg-0">
                    <a href=#anchor2 id=lx">
                        <button class="btn btn-primary" name="lx" onclick="toggleGraph('lxplot')">Show data</button>
                    </a>
                </div>
            </div>
            <div id="refresh">
                <div style="display: none" id="lxplot"></div>
            </div>
        </div>
        
        <div class="row align-items-center no-gutters mb-4 mb-lg-5" id='anchor3'>
            <div class="col-xl-4 col-lg-5"><div class="featured-text text-center text-lg-left"><h4>Temperature and humidity</h4></div></div>
            <div class="col-xl-8 col-lg-7"><div class="img-fluid mb-3 mb-lg-0"><a href=#anchor3 id=th><button class="btn btn-primary" name="th" onclick="toggleGraph('thplot')">Show data</button></a>
            </div></div><div id="refresh"><div style="display: none"" id="thplot"></div></div></div></div>
            
            
        <div class="row align-items-center no-gutters mb-4 mb-lg-5">
            <div class="col-xl-4 col-lg-5"><div class="featured-text text-center text-lg-left"></div></div>
            <div class="col-xl-8 col-lg-7"><div class="img-fluid mb-3 mb-lg-0"><button class="btn btn-primary" name="refresh" onclick="window.location.reload();">Refresh data</button>
            </div></div></div></div>
        </section>


<!-- Contact Section -->
<section class="contact-section bg-black"><div class="container"><div class="social d-flex justify-content-center">
            <a href="#" class="mx-2"><i class="fab fa-twitter"></i></a>
            <a href="#" class="mx-2"><i class="fab fa-facebook-f"></i></a>
            <a href="#" class="mx-2"><i class="fab fa-github"></i></a>
</div></div></section>

<!-- Footer -->
<footer class="bg-black small text-center text-white-50">
    <div class="container">
        Copyright &copy; Your Website 2019
        <p><a class="js-scroll-trigger" href="#page-top">Back to top</a></p>
    </div>
</footer>
<!-- Bootstrap core JavaScript -->
<script src="/static/vendor/jquery/jquery.min.js"></script>
<script src="/static/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>
<!-- Plugin JavaScript -->
<script src="/static/vendor/jquery-easing/jquery.easing.min.js"></script>
<!-- Custom scripts for this template -->
<script src="/static/js/grayscale.min.js"></script>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
{#Source: https://stackoverflow.com/questions/42601478/flask-calling-python-function-on-button-onclick-event#}

<script>
  fetch('/plotir')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item); })
</script>
<script>
  fetch('/plotth')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item); })
</script>
  <script>
  fetch('/plotlx')
    .then(function(response) { return response.json(); })
    .then(function(item) { Bokeh.embed.embed_item(item); })
</script>
<script type=text/javascript src="static/js/custom.js"></script>

""")

# Login required decorator
def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('shop_login'))
    return wrap


# Instantiation of the object mongo of class PyMongo & initialization of mongo object by app object
mongo_users = PyMongo(app, uri=os.environ.get('MONGO_URI_USERS'))
mongo_sensor_data = PyMongo(app, uri=os.environ.get('MONGO_URI_SENSORS'))


# defining routes, / means home directory = home page
@app.route('/')
def main():
    return render_template('index.html')


@app.route('/data')
@login_required
def data():
    # Solution to url_for in template not recognized: https://stackoverflow.com/questions/20843085/url-for-is-not-defined-in-flask
    main_url = url_for('main')
    logout_url = url_for('logout')
    if session['logged_in'] == True:
        return page.render(main_url=main_url, logout_url=logout_url, resources=CDN.render())
    else:
        return redirect(url_for('shop_login'))


@app.route('/plotir')
@login_required
def plotir():
    data = db.read_db()
    xdata = []
    ydata = []
    for i in range(0, len(data['infrared'])):
        xdata.append(data['infrared'][i]['_id'])
        ydata.append(data['infrared'][i]['value'])
    plot = figure(x_axis_type='datetime', y_range=Range1d(bounds=(0, 1)), width=600, height=600)
    plot.step(xdata, ydata, line_width=2, mode="center")
    xdata = [datetime.strptime(date, "%m/%d/%Y;%H:%M:%S") for date in xdata]
    ydata = list(map(float, ydata))
    plot.line(xdata, ydata, line_width=2)
    # return Markup(file_html(plot, CDN, "data"))
    return json.dumps(json_item(plot, "irplot"))


@app.route('/plotth')
@login_required
def plotth():
    data = db.read_db()
    xdataTemp = []
    ydataTemp = []
    xdataHumidity = []
    ydataHumidity = []
    for i in range(0, len(data['temperature'])):
        xdataTemp.append(data['temperature'][i]['_id'])
        ydataTemp.append(data['temperature'][i]['value'])
    for i in range(0, len(data['humidity'])):
        xdataHumidity.append(data['humidity'][i]['_id'])
        ydataHumidity.append(data['humidity'][i]['value'])
    # Filter out (remove) all 'None' values from the dictionary and replace by previous value
        # Solution: https://stackoverflow.com/questions/35868549/fill-na-in-a-list-with-the-last-know-value-in-python
    for i, j in enumerate(ydataTemp):
        if j is None:
            if i == 0: ydataTemp = next(item for item in ydataTemp if item is not None)
            else: ydataTemp[i] = ydataTemp[i-1]
    for i, j in enumerate(ydataHumidity):
        if j is None:
            if i == 0: ydataHumidity = next(item for item in ydataHumidity if item is not None)
            else: ydataHumidity[i] = ydataHumidity[i - 1]
    xdataTemp = [datetime.strptime(date, "%m/%d/%Y;%H:%M:%S") for date in xdataTemp]
    xdataHumidity = [datetime.strptime(date, "%m/%d/%Y;%H:%M:%S") for date in xdataHumidity]
    plot = figure(x_axis_label='date', x_axis_type='datetime', width=600, height=600)
    plot.line(xdataTemp, ydataTemp, line_width=2, line_color='green')
    plot.line(xdataHumidity, ydataHumidity, line_width=2, line_color='blue')
    # return Markup(file_html(plot, CDN, "data"))
    return json.dumps(json_item(plot, "thplot"))


@app.route('/plotlx')
@login_required
def plotlx():
    data = db.read_db()
    xdata = []
    ydata = []
    for i in range(0, len(data['light'])):
        xdata.append(data['light'][i]['_id'])
        ydata.append(data['light'][i]['value'])
    plot = figure(x_axis_type='datetime', width=600, height=600)
    xdata = [datetime.strptime(date, "%m/%d/%Y;%H:%M:%S") for date in xdata]
    ydata = list(map(float, ydata))
    plot.line(xdata, ydata, line_width=2)
    return json.dumps(json_item(plot, "lxplot"))


    #Sources used in this method:
        # https://davidhamann.de/2018/02/11/integrate-bokeh-plots-in-flask-ajax/
        # http://docs.bokeh.org/en/1.0.4/docs/user_guide/plotting.html
        # https://stackoverflow.com/questions/7368789/convert-all-strings-in-a-list-to-int
        # https://stackoverflow.com/questions/33869292/how-can-i-set-the-x-axis-as-datetimes-on-a-bokeh-plot
        # https://stackoverflow.com/questions/30487870/python-converting-strings-in-an-array-to-dates
        # https://www.programiz.com/python-programming/datetime
        # https://stackoverflow.com/questions/25015711/time-data-does-not-match-format
        # https://stackoverflow.com/questions/18039680/django-get-only-date-from-datetime-strptime
        # https://stackoverflow.com/questions/23277066/limit-bokeh-plot-pan-to-defined-range
        # https://stackoverflow.com/questions/22345249/embedding-a-plot-in-a-website-with-python-bokeh
        # http://docs.bokeh.org/en/1.3.2/docs/user_guide/embed.html
        # https://github.com/bokeh/bokeh/blob/1.3.2/examples/embed/json_item.py
        # https://stackoverflow.com/questions/29508958/how-to-embed-standalone-bokeh-graphs-into-django-templates
        # https://p-mckenzie.github.io/2017/12/01/embedding-bokeh-with-github-pages/

# source: https://www.youtube.com/watch?v=bLA6eBGN-_0
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            error = 'Invalid credential. Please, try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('data'))
    return render_template('login.html', error=error)


# source: https://www.youtube.com/watch?v=BnBjhmspw4c
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    session.clear()
    return redirect(url_for('main'))


#######################
# Todo: finish:
@app.route('/registration')
def registration():
    return render_template('registration.html')
#######################


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=7081)