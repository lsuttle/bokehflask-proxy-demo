from bokeh.io import curdoc

import pandas as pd
from bokeh.charts import Scatter, output_file, show
from bokeh.models.widgets import Dropdown, Div, Button
from bokeh.layouts import row, widgetbox, layout
from bokeh.models import Select
from bokeh.models import ColumnDataSource

from bokeh.plotting import figure
from sqlalchemy import and_, create_engine, func, case, Table, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def pulldata(filters, bins):
    completed = case([(Projects.funding_status == 'completed', 1)],else_=0).label('completed')

    q = session.query(Projects).with_entities(bins, func.sum(completed), func.count(completed))

    for key in filters:
        if filters[key] is not 'All':
            q = q.filter(getattr(Projects, key) == filters[key])

    return [{'bin': x[0], 'sum':x[1], 'count':x[1]} for x in q.group_by(bins).all()]

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

#engine = create_engine('sqlite:///' + dbPath, echo=False)
engine = create_engine('postgresql://testusr:testpw@psql')

# old code
#connection = engine.connect()
#meta = MetaData()
#meta.reflect(bind=engine)
#projects = meta.tables['projects_nces']

b = [0, 100, 250, 500, 1000, 5000]
ranges = [(b[i-1], b[i]) for i in range(1,len(b))]

bins = case(
        [
            (and_(projects.c.price > ranges[0][0], projects.c.price <= ranges[0][1]), str(ranges[0])),
            (and_(projects.c.price > ranges[1][0], projects.c.price <= ranges[1][1]), str(ranges[1])),
            (and_(projects.c.price > ranges[2][0], projects.c.price <= ranges[2][1]), str(ranges[2])),
            (and_(projects.c.price > ranges[3][0], projects.c.price <= ranges[3][1]), str(ranges[3])),
            (and_(projects.c.price > ranges[4][0], projects.c.price <= ranges[4][1]), str(ranges[4])),

        ],
    else_='>'+str(b[-1])).label('bins')


slist = connection.execute(select([projects.c.school_state]).distinct()).fetchall()
flist = connection.execute(select([projects.c.primary_focus_subject]).distinct()).fetchall()
flist = [x[0] for x in flist]
flist.remove(None)
#slist = sorted([x[0] for x in result])
states = ['All'] + sorted([x[0] for x in slist])
fields = ['All'] + sorted(flist)


# get data
f = {'school_state': 'All', 'primary_focus_subject': 'All'}
source = ColumnDataSource(pd.DataFrame.from_dict(data=pulldata(f, bins)))
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
