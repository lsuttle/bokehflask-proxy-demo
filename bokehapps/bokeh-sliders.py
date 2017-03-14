from bokeh.io import curdoc

import pandas as pd
from bokeh.charts import Scatter, output_file, show
from bokeh.models.widgets import Dropdown, Div, Button
from bokeh.layouts import row, widgetbox, layout
from bokeh.models import Select
from bokeh.models import ColumnDataSource

from bokeh.plotting import figure
from sqlalchemy import or_, and_, select, create_engine, MetaData, text, func

def pulldata(state, focus):
    stext = "school_state=:state"
    ftext = "primary_focus_subject=:focus"
    if state == focus:
        s = select([projects.c.bins, func.sum(projects.c.completed), func.count(projects.c.completed)]).\
                group_by(projects.c.bins)
    elif state == 'All':
        s = select([projects.c.bins, func.sum(projects.c.completed), func.count(projects.c.completed)]).\
                where(text(ftext)).\
                group_by(projects.c.bins)
    elif focus == 'All':
        s = select([projects.c.bins, func.sum(projects.c.completed), func.count(projects.c.completed)]).\
                where(text(stext)).\
                group_by(projects.c.bins)
    else:
        s = select([projects.c.bins, func.sum(projects.c.completed), func.count(projects.c.completed)]).\
                where(and_(text(stext), text(ftext))).\
                group_by(projects.c.bins)
    result = connection.execute(s, state=state, focus=focus)
    return [{'bin': x[0], 'sum':x[1], 'count':x[1]} for x in result.fetchall()]


def update_plot(attrname, old, new):
    state = stateselect.value
    field = fieldselect.value
    src = ColumnDataSource(pd.DataFrame.from_dict(data=pulldata(state, field)))
    #src = get_dataset(df, state, field, 1000)
    source.data.update(src.data)
    #prob = get_prob(source.data['completed'])
    #div.text = '{}% funding chance'.format(prob)

def make_bar(df, x, y):
    p = figure(title="barchart example",
               x_range= df.data[x], webgl=True)
    p.vbar(x= x,
           width=0.5, bottom=0,
           top=y, color="firebrick",
           source = df)
    return p

dbPath = "BokehTest/data/donorschoose.db"

engine = create_engine('sqlite:///' + dbPath, echo=False)
connection = engine.connect()

meta = MetaData()
meta.reflect(bind=engine)

projects = meta.tables['projectsbins']

slist = connection.execute(select([projects.c.school_state]).distinct()).fetchall()
flist = connection.execute(select([projects.c.primary_focus_subject]).distinct()).fetchall()

#slist = sorted([x[0] for x in result])
states = ['All'] + sorted([x[0] for x in slist])
fields = ['All'] + sorted([x[0] for x in flist])

# get data
source = ColumnDataSource(pd.DataFrame.from_dict(data=pulldata('All', fields[1])))

# create figure
#p = make_plot(source)
counts = make_bar(source, 'bin', 'count')

# get probability of success
#prob = get_prob(source.data['completed'])

# create widgets
stateselect = Select(title='Select State', value=states[0], options=states)
fieldselect = Select(title='Select Focus Subject', value=fields[0], options=fields)
updatebutton = Button(label="Update Figure", button_type="success")

#div = Div(text='{}% funding chance'.format(prob), width=200, height=100)


w = widgetbox(stateselect, fieldselect, updatebutton)#, div)

# filter settings
#stateselect.on_change('value', update_plot)
#fieldselect.on_change('value', update_plot)


# layout
l = layout([[w, counts]])

#show
#show(l)

curdoc().add_root(l)
curdoc().title = "Sliders"
