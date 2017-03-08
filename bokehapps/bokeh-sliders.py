from bokeh.io import curdoc

import pandas as pd
from bokeh.charts import Scatter#, output_file, show
from bokeh.models.widgets import Dropdown, Div
from bokeh.layouts import row, widgetbox, layout, column
from bokeh.models import Select, ColumnDataSource


from bokeh.plotting import figure
import sqlite3


sql = """
SELECT _projectid, school_state, teacher_teach_for_america,
teacher_ny_teaching_fellow, grade_level, completed, year,
poverty_level, primary_focus_subject, perc_funded,
total_price_excluding_optional_support
FROM projects
where total_price_excluding_optional_support > 0
"""

con = sqlite3.connect("/data/donorschoose.db")
projects = pd.read_sql(sql, con)

df = projects[(projects.year == 2015) & (projects.total_price_excluding_optional_support < 10000)]
bins = [0, 100, 500, 1000, 5000, int(df.total_price_excluding_optional_support.max())]
df['bins'] = pd.cut(df.total_price_excluding_optional_support, bins)

def make_plot(df):
    prob = get_prob(source.data['completed'])
    p = figure(title='{}% funding chance'.format(prob), webgl=True)
    p.scatter(x='total_price_excluding_optional_support',
              y='perc_funded',
              source = df,
              size = 10)
    return p

def make_bar(df, x, y):
    p = figure(title="barchart example",
               x_range= df.data['bins'], webgl=True)
    p.vbar(x= x,
           width=0.5, bottom=0,
           top=y, color="firebrick",
           source = df)
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
    df = filter_dataset(src, state, field)
    return ColumnDataSource(data = return_sample(df, sample))

def get_group_dataset(src, state, field):
    df = filter_dataset(src, state, field)
    grouped = df[['bins', 'completed']].groupby('bins')

    groups = pd.DataFrame(grouped.completed.sum()/grouped.completed.count(), columns = ['bins', 'completed'])
    groups['count'] = grouped.completed.count()
    return ColumnDataSource(data = groups)

def filter_dataset(src, state, field):
    df = src.copy()
    if state == field:
        return df
    if state is not 'All':
        return df[df['school_state'].isin([state])]
    if field is not 'All':
        return df[df['primary_focus_subject'].isin([field])]

def update_plot(attrname, old, new):
    #filter values
    state = stateselect.value
    field = fieldselect.value
    # filter data
    src = get_dataset(df, state, field, 100)
    src_bin = get_group_dataset(df, state, field)
    #update data sources
    source.data.update(src.data)
    binned.data.update(src_bin.data)
    #update models
    prob = get_prob(source.data['completed'])
    #update plot text
    #p.title.text = '{}% funding chance'.format(prob)
    div.text = '{}% funding chance'.format(prob)
    div2.text = '{}'.format(state)
    div3.text = '{}'.format(field)

states = ['All'] + sorted(list(df.school_state.unique()))
fields = ['All'] + sorted(list(df.primary_focus_subject.unique()))

#get data
source = get_dataset(df, states[0], fields[0], 100)
binned = get_group_dataset(df, states[0], fields[0])

# base prob
prob = get_prob(source.data['completed'])

# create figures
#p = make_plot(source)
perc = make_bar(binned, 'bins', 'completed')
counts = make_bar(binned, 'bins', 'count')

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
l = row(w, column(perc, counts))
curdoc().add_root(l)
curdoc().title = "Sliders"
