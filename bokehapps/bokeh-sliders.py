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

import cPickle as pickle

from sklearn.ensemble import RandomForestClassifier

import data_funcs
import models

def get_cat_filter(column, session, inc_all = True):
    l = session.query(Projects).with_entities(getattr(Projects, column)).distinct().all()
    if inc_all:
        return ['All'] + sorted([x[0] for x in l if x[0] is not None])
    return sorted([x[0] for x in l if x[0] is not None])


def mapFilters():
    return {'school_state': stateselect.value,
     'primary_focus_subject': fieldselect.value,
    'resource_type': resource_type.value,
    'n_has_givepage': data_funcs.mapBinary(giving_page.value),
    #'c': giving_page_size.value,
    'date_posted': month.value,
    'grade_level': grade_level.value,
    'eligible_double_your_impact_match': data_funcs.mapTF(dym.value),
    'eligible_almost_home_match': data_funcs.mapTF(ahm.value),
    'poverty_level': poverty_level.value}

def update_plot():
    f = mapFilters()
    model_input_vector = models.make_vector(mapPredictors(f))
    output = models.make_changes(model_input_vector, rf)

    src = ColumnDataSource(data=output.head(10))

    source.data.update(src.data)

    # get data
    prob = rf.predict_proba(model_input_vector)[:,1]
    div.text = '{}% funding chance'.format(output)
    #counts = make_bar(source, 'Recommendation', 'Score')


def make_bar(df, x, y):
    p = figure(title="barchart example",
               x_range= df.data[x], webgl=True)
    p.vbar(x= x,
           width=0.5, bottom=0,
           top=y, color="darkgreen",
           source = df)
    return p


def mapPredictors(f):
    return [
    f['n_has_givepage'], # 0 for false, 1 for true
    1, # 0 for false, 1 for true
    1, # 0 for false, 1 for true
    0, #f['eligible_double_your_impact_match'], # 0 for false, 1 for true
    0, #f['eligible_almost_home_match'], # 0 for false, 1 for true
    1, # an integer value
    30, # an integer value
    30, # an integer value
    300, #f['price'], # a float value
    0.5, # a float value
    'May',#date_posted,\ # a string ie. 'March'
    f['school_state'], # a 2 letter string ie. 'CA'
    f['primary_focus_subject'], # a string ie. 'Character Education'
    f['resource_type'], # a string ie. 'Books'
    f['poverty_level'], # a string ie. 'high poverty'
    f['grade_level'] # a string ie. 'Grades 3-5'
    ]

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

# prepare vector for prediction
f = mapFilters()
rf = pickle.load(open("./data/dc_rf_model.p","rb" ))
model_input_vector = models.make_vector(mapPredictors(f))
output = models.make_changes(model_input_vector, rf)

# get data
source = ColumnDataSource(data=output.head(10))
prob = rf.predict_proba(model_input_vector)[:,1]

div = Div(text='{}% funding chance'.format(output), width=200, height=100)

# create figure
counts = make_bar(source, 'Rec_Number', 'Score')

w = widgetbox(stateselect, fieldselect, resource_type,
              giving_page, giving_page_size, month,
              grade_level, dym, ahm,
              updatebutton, div)

# filter settings
updatebutton.on_click(update_plot)

# layout
l = layout([[w, counts]])

curdoc().add_root(l)
curdoc().title = "Sliders"
