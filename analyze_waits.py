#!/usr/bin/env python

print "Usage: bokeh serve --show analyze_waits.py"

rides = {
        'Breakers Edge':112,
        'Cocoa Cruiser':101,
        'Comet':3,
        'Farenheit':31,
        'Great Bear':1,
        'Laff Trakk':104,
        'Lightning Racer':2,
        'Sidewinder':10,
        'Skyrush':97,
        'sooperdooperLooper':11,
        'Storm Runner':83,
        'Trailblazer':28,
        'Wild Mouse':15,
        'Wildcat':13
    }
rides = sorted(rides.items(), key=lambda x:x[0])

############################################################
# Load in the data
############################################################

import datetime
today = datetime.datetime.now().date()

f = open('compiled_waits.txt' , 'r')

data = {}
alphas = {}
for r, id in rides:
    data[r] = {}
    for i in range(7):
        data[r][i] = {}

for line in f:
    fields = line.split()
    day_index = fields[0]+"-"+fields[1]
    delta = today - datetime.date(2018, int(fields[0]), int(fields[1]))
    alphas[day_index] = delta.days
    weekday = int(fields[4])
    time = (int(fields[2]), int(fields[3]))
    time_index = int((time[0])*60 + time[1])
    for i,field in enumerate(fields[5:]):
        if field=='Missing' or field=='None':
            wait = 120
        else:
            wait = int(field)
        
        r = rides[i][0]
        data[r][weekday].setdefault(day_index, [[],[]])[0].append(time_index)
        data[r][weekday][day_index][1].append(wait)

print alphas
m = float(max(max(alphas.values()),1))
for k in alphas.keys():
    v = alphas[k]
    v /= m
    v *= 0.8
    v += 0.2
    alphas[k] = 1-v
    
############################################################
# Plot using Bokeh
############################################################

# Imports
from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.tools import HoverTool

from bokeh.layouts import widgetbox
from bokeh.models.widgets import Select

from bokeh.io import curdoc
from bokeh.layouts import row, column

# Create drop down menu
select = Select(title="Roller Coaster:", value=rides[3][0], options=[x[0] for x in rides])

# Initialize canvas
p = figure(plot_width=600, plot_height=400)
p.y_range.start = 0
p.y_range.end = 120
lr = []

# Function to draw on canvas for a given roller coaster
def draw_plot(coaster_name):
    r = coaster_name
    Y = data[r]
    day_colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    
    for i in range(7):
        dates = sorted(Y[i].keys())
        for j in range(len(dates)):
            date = dates[j]
            x = Y[i][date][0]
            y = Y[i][date][1]
            print date, x, y
            source = ColumnDataSource(data={'x':x, 'y':y, 'date':[str(date) for _ in range(len(x))]})
            lr.append(
                p.line('x', 'y', source=source, line_width=2, alpha=alphas[date],
                       color=day_colors[i], hover_color='purple',)
            )
    p.xaxis.axis_label = "Time of Day"
    p.yaxis.axis_label = "Wait time (min)"
    p.title.text = select.value
    p.add_tools(HoverTool(tooltips=[("date", "@date")], renderers=lr, mode='mouse'))

    
# Update canvas for new roller coaster
def update(att, old, new):
    # Clear the lines off of the plot
    #while len(lr) > 0:
    #    render = lr.pop(0)
    #    p.renderers.remove(render)
    for render in lr:
        render.visible = False

    # Draw new lines
    draw_plot(select.value)

    
# Update plot when new value chosen from dropdown
select.on_change('value', update)

# Initialize plot
layout = column(select, p)
draw_plot(rides[3][0])

# Add it to web page
curdoc().add_root(layout)
curdoc().title = "Hershey Park Wait times"
