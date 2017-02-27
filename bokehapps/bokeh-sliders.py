from bokeh.io import curdoc

import pandas as pd
from bokeh.charts import Scatter#, output_file, show
from bokeh.models.widgets import Dropdown, Div
from bokeh.layouts import row, widgetbox, layout
from bokeh.models import Select, ColumnDataSource


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
    if len(values) == 0:
        return 0
    return int(float(sum(values))/len(values) * 100)

def return_sample(data, sample):
    if len(data) < sample:
        return data
    return data.sample(sample)

def get_dataset(src, state, field, sample):
    df = src.copy()
    if state == field:
        return ColumnDataSource(data=return_sample(df, sample))
    if state is not 'All':
        df = df[df['school_state'].isin([state])]
        return ColumnDataSource(data=return_sample(df, sample))
    if field is not 'All':
        df = df[df['primary_focus_subject'].isin([field])]
        return ColumnDataSource(data=return_sample(df, sample))



def update_plot(attrname, old, new):
    state = stateselect.value
    field = fieldselect.value
    src = get_dataset(df, state, field, 100)
    source.data.update(src.data)
    prob = get_prob(source.data['completed'])
    p.title.text = '{}% funding chance'.format(prob)
    div.text = '{}% funding chance'.format(prob)
    div2.text = '{}'.format(state)
    div3.text = '{}'.format(field)

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
div2 = Div(text='{}'.format(stateselect.value), width=200, height=100)
div3 = Div(text='{}'.format(fieldselect.value), width=200, height=100)


w = widgetbox(stateselect, fieldselect, div, div2, div3)

# filter settings
#stateselect.on_change('value', update_plot)
#fieldselect.on_change('value', update_plot)

for widget in [stateselect, fieldselect]:
    widget.on_change('value', update_plot)

# layout
l = layout([[w, p]])

curdoc().add_root(l)
curdoc().title = "Sliders"
