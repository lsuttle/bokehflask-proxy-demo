from bokeh.io import curdoc

import pandas as pd
from bokeh.charts import Scatter, output_file, show
from bokeh.models.widgets import Dropdown, Div
from bokeh.layouts import row, widgetbox, layout
from bokeh.models import Select
from bokeh.models import ColumnDataSource

from bokeh.plotting import figure
import sqlite3


sql = """
SELECT _projectid, year, total_price_including_optional_support,
school_state, total_donations, perc_funded, primary_focus_subject, completed
FROM projects
"""

con = sqlite3.connect("/data/donorschoose.db")
projects = pd.read_sql(sql, con)

df = projects[(projects.year == 2015) & (projects.total_price_including_optional_support < 1000)]

def make_plot(df):
    prob = get_prob(source.data['completed'])
    p = figure(title='{}% funding chance'.format(prob), webgl=True)
    p.scatter(x='total_price_including_optional_support',
              y='perc_funded',
              source = df,
              size = 10)
    return p

def get_prob(values):
    #return int(sum(values)/len(values) * 100)
    return int(float(sum(values))/len(values) * 100)

def get_dataset(src, state, field, sample):
    l = [state, field]
    fd = {}
    if state is not 'All':
        fd['school_state'] = [state]
    if field is not 'All':
        fd['primary_focus_subject'] = [field]
    df = src.copy()
    for key, values in fd.items():
        df = df[df[key].isin(values)]
    return ColumnDataSource(data=df.sample(sample))

def update_plot(attrname, old, new):
    state = stateselect.value
    field = fieldselect.value
    src = get_dataset(df, state, field, 100)
    source.data.update(src.data)
    prob = get_prob(source.data['completed'])
    p.title.text = '{}% funding chance'.format(prob)
    div.text = '{}% funding chance'.format(prob)

states = ['All'] + sorted(list(df.school_state.unique()))
fields = ['All'] + sorted(list(df.primary_focus_subject.unique()))

# get data
source = get_dataset(df, states[0], fields[0], 100)

# base prob
prob = get_prob(source.data['completed'])

# create figure
p = make_plot(source)

# create widgets
stateselect = Select(title='Select State', value=states[0], options=states)
fieldselect = Select(title='Select Focus Subject', value=fields[0], options=fields)
div = Div(text='{}% funding chance'.format(prob), width=200, height=100)

w = widgetbox(stateselect, fieldselect, div)

# filter settings
stateselect.on_change('value', update_plot)
fieldselect.on_change('value', update_plot)


# layout
l = layout([[w, p]])

curdoc().add_root(l)
curdoc().title = "Sliders"
