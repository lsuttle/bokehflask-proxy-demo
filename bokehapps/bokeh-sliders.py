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

import data_funcs

def mapFilters():
    return {'school_state': stateselect.value,
     'primary_focus_subject': fieldselect.value,
    'resource_type': resource_type.value,
    'n_has_givepage': data_funcs.mapBinary(giving_page.value),
    #'c': giving_page_size.value,
    #'date_posted': monthToNum(month.value),
    'grade_level': grade_level.value,
    'eligible_double_your_impact_match': data_funcs.mapTF(dym.value),
    'eligible_almost_home_match': data_funcs.mapTF(ahm.value),
    'poverty_level': poverty_level.value}

def update_plot():
    f = mapFilters()
    src = ColumnDataSource(pd.DataFrame.from_dict(data=pulldata(f, bins)))
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

def get_cat_filter(column, session, inc_all = True):
    l = session.query(Projects).with_entities(getattr(Projects, column)).distinct().all()
    if inc_all:
        return ['All'] + sorted([x[0] for x in l if x[0] is not None])
    return sorted([x[0] for x in l if x[0] is not None])

def pulldata(filters, bins):
    completed = case([(Projects.funding_status == 'completed', 1)],else_=0).label('completed')

    q = session.query(Projects).with_entities(bins, func.sum(completed), func.count(completed))

    for key in filters:
        if filters[key] is not 'All':
            q = q.filter(getattr(Projects, key) == filters[key])

    return [{'bin': x[0], 'sum':x[1], 'count':x[1]} for x in q.group_by(bins).all()]

dbPath = "BokehTest/data/donorschoose.db"

engine = create_engine('postgresql://testusr:testpw@psql')

Base = declarative_base()
Base.metadata.reflect(engine)

class Projects(Base):
    __table__ = Table('projects_nces',
                      Base.metadata,
                      Column('_projectid', primary_key=True),
                      extend_existing=True)

Session = sessionmaker(bind=engine)
session = Session()


b = [0, 100, 250, 500, 1000, 5000]
ranges = [(b[i-1], b[i]) for i in range(1,len(b))]

bins = case(
        [
            (and_(Projects.price > ranges[0][0], Projects.price <= ranges[0][1]), str(ranges[0])),
            (and_(Projects.price > ranges[1][0], Projects.price <= ranges[1][1]), str(ranges[1])),
            (and_(Projects.price > ranges[2][0], Projects.price <= ranges[2][1]), str(ranges[2])),
            (and_(Projects.price > ranges[3][0], Projects.price <= ranges[3][1]), str(ranges[3])),
            (and_(Projects.price > ranges[4][0], Projects.price <= ranges[4][1]), str(ranges[4])),

        ],
    else_='>'+str(b[-1])).label('bins')


#lists for filters
states = get_cat_filter('school_state', session)
fields = get_cat_filter('primary_focus_subject', session)
months = ['January','February', 'March', 'April', 'May',
            'June','July','August','September','October',
            'November','December']

choice = ['No', 'Yes']
grades = ['Grades PreK-2', 'Grades 3-5', 'Grades 6-8', 'Grades 9-12']
poverty = get_cat_filter('poverty_level', session)
resource = get_cat_filter('resource_type', session)


# create widgets
stateselect = Select(title='Select State', value=states[0], options=states)
fieldselect = Select(title='Select Focus Subject', value=fields[0], options=fields)
resource_type = Select(title = 'Resource Type', value = resource[0], options=resource)
giving_page = Select(title='Is your project be on a giving page?',value = choice[0],options=choice)
giving_page_size = Select(title='Is Giving Page Size > 100 Projects?',value = choice[0],options=choice)
month = Select(title="Request Month",value = months[0], options=months)
grade_level = Select(title="Grade Level",value = grades[0],options=grades)
dym = Select(title='Eligible for Double Your Match?',value = choice[0],options=choice)
ahm = Select(title='Eligible for Almost Home Match?',value = choice[0],options=choice)
poverty_level =  Select(title='Poverty Level',value = poverty[0],options=poverty)

updatebutton = Button(label="Update Figure", button_type="success")

#div = Div(text='{}% funding chance'.format(prob), width=200, height=100)

# get data
f = mapFilters()
source = ColumnDataSource(pd.DataFrame.from_dict(data=pulldata(f, bins)))

# create figure
counts = make_bar(source, 'bin', 'count')

# get probability of success
#prob = get_prob(source.data['completed'])

w = widgetbox(stateselect, fieldselect, resource_type,
              giving_page, giving_page_size, month,
              grade_level, dym, ahm,
              updatebutton)#, div)

# filter settings
updatebutton.on_click(update_plot)
#stateselect.on_change('value', update_plot)
#fieldselect.on_change('value', update_plot)


# layout
l = layout([[w, counts]])

#show
#show(l)

curdoc().add_root(l)
curdoc().title = "Sliders"
