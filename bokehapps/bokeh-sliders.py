from bokeh.io import curdoc

import pandas as pd
from bokeh.charts import Scatter, output_file, show
from bokeh.models.widgets import Dropdown, Div, Button
from bokeh.layouts import row, widgetbox, layout
from bokeh.models import Select
from bokeh.models import ColumnDataSource

from bokeh.plotting import figure
<<<<<<< HEAD
from sqlalchemy import and_, create_engine, func, case, Table, Column
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import cPickle as pickle

from sklearn.ensemble import RandomForestClassifier

import data_funcs
import models

def get_cat_filter(column, session, inc_all = False):
    """ Gets distinct values from
    postgres database to populate
    filters."""
    l = session.query(Projects).with_entities(getattr(Projects, column)).distinct().all()
    if inc_all:
        return ['All'] + sorted([x[0] for x in l if x[0] is not None])
    return sorted([x[0] for x in l if x[0] is not None])

def mapFilters():
    """ Takes values from filters
    and returns a dictionary.
    Maps those that need to be mapped."""
    return {'school_state': stateselect.value,
        'primary_focus_subject': fieldselect.value,
        'resource_type': resource_type.value,
        'n_has_givepage': data_funcs.mapNum(giving_page.value),
        'date_posted': month.value,
        'grade_level': grade_level.value,
        'eligible_double_your_impact_match': data_funcs.mapNum(dym.value),
        'eligible_almost_home_match': data_funcs.mapNum(ahm.value),
        'poverty_level': poverty_level.value}

def update_plot():
    """ Updates dashboard when Update Button
    is pressed. """
    f = mapFilters()
    model_input_vector = models.make_vector(mapPredictors(f)) # vector formated for input
    output = models.make_changes(model_input_vector, rf) # get recommendations

    src = ColumnDataSource(data=output.head(10)) # convert to bokeh column source
    source.data.update(src.data) # update primary source with new one

    prob = rf.predict_proba(model_input_vector)[:,1] # probability of current model, if needed

=======
from sqlalchemy import or_, and_, select, create_engine, MetaData, text, func

def pulldata(state, focus):
    stext = "school_state=:state"
    ftext = "primary_focus_subject=:focus"
    if state == focus:
        s = select([projects.c.bins, func.sum(projects.c.completed), func.count(projects.c.completed)]).\
                where(text("total_price_excluding_optional_support > 0")).\
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
    df = pd.DataFrame.from_dict([{'bin': x[0], 'sum':x[1], 'count':x[1]} for x in result.fetchall()])
    df['sort'] = pd.to_numeric(df.bin.str.extract('\(([^\)]+)\,'))
    df = df.sort_values(by='sort')
    return df[['bin', 'sum', 'count']]


def update_plot():
    state = stateselect.value
    field = fieldselect.value
    src = ColumnDataSource(pd.DataFrame.from_dict(data=pulldata(state, field)))
    #src = get_dataset(df, state, field, 1000)
    source.data.update(src.data)
    #prob = get_prob(source.data['completed'])
    #div.text = '{}% funding chance'.format(prob)
>>>>>>> 39405f464a21d68b13d140c765496fe9c817b55f

def make_bar(df, x, y):
    """ Creates a bar chart in bokeh"""
    p = figure(title="barchart example",
               x_range= df.data[x], webgl=True)
    p.vbar(x= x,
           width=0.5, bottom=0,
           top=y, color="darkgreen",
           source = df)
    return p

<<<<<<< HEAD
##### TO DO: Add the rest of the filters and hook them in
def mapPredictors(f):
    """ Gets values from filter dictionary into list for
    vector conversion"""
    return [
        f['n_has_givepage'], # 0 for false, 1 for true
        1, # 0 for false, 1 for true # top500_giving_t
        1, # 0 for false, 1 for true # title1
        f['eligible_double_your_impact_match'], # 0 for false, 1 for true
        f['eligible_almost_home_match'], # 0 for false, 1 for true
        1, # an integer value #teachers
        30, # an integer value #students
        30, # an integer value #students_reached
        300, #f['price'], # a float value #total_price_excluding_optional_support
        0.5, # a float value #percent_lunch_aid
        f['date_posted'], # a string ie. 'March'
        f['school_state'], # a 2 letter string ie. 'CA'
        f['primary_focus_subject'], # a string ie. 'Character Education'
        f['resource_type'], # a string ie. 'Books'
        f['poverty_level'], # a string ie. 'high poverty'
        f['grade_level'] # a string ie. 'Grades 3-5'
        ]

####################
#### database set up
###################

# connect to data base
dbPath = "BokehTest/data/donorschoose.db"
engine = create_engine('postgresql://testusr:testpw@psql')
# get table ORM set up
Base = declarative_base()
Base.metadata.reflect(engine)
class Projects(Base):
    __table__ = Table('projects_nces',
                      Base.metadata,
                      Column('_projectid', primary_key=True),
                      extend_existing=True)
#create session
Session = sessionmaker(bind=engine)
session = Session()

###############
#### filter setup
##############

###get data for categorical filters
#based on database values
states = get_cat_filter('school_state', session)
fields = get_cat_filter('primary_focus_subject', session)
poverty = get_cat_filter('poverty_level', session)
resource = get_cat_filter('resource_type', session)
# hard coded for now
months = ['January','February', 'March', 'April', 'May',
            'June','July','August','September','October',
            'November','December']
choice = ['No', 'Yes']
grades = ['Grades PreK-2', 'Grades 3-5', 'Grades 6-8', 'Grades 9-12']
=======
dbPath = "data/donorschoose.db"

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
source = ColumnDataSource(pd.DataFrame.from_dict(data=pulldata('All', 'All')))

# create figure
#p = make_plot(source)
counts = make_bar(source, 'bin', 'count')

# get probability of success
#prob = get_prob(source.data['completed'])
>>>>>>> 39405f464a21d68b13d140c765496fe9c817b55f

# create widgets
#### TO DO: ADD VALUE WIDGETS FOR TEACHERS, STUDENTS, PRICE

# select widgets
stateselect = Select(title='Select State', value=states[1], options=states)
fieldselect = Select(title='Select Focus Subject', value=fields[0], options=fields)
<<<<<<< HEAD
resource_type = Select(title = 'Resource Type', value = resource[0], options=resource)
giving_page = Select(title='Is your project be on a giving page?',value = choice[0],options=choice)
giving_page_size = Select(title='Is Giving Page Size > 100 Projects?',value = choice[0],options=choice)
month = Select(title="Request Month",value = months[0], options=months)
grade_level = Select(title="Grade Level",value = grades[0],options=grades)
dym = Select(title='Eligible for Double Your Match?',value = choice[0],options=choice)
ahm = Select(title='Eligible for Almost Home Match?',value = choice[0],options=choice)
poverty_level =  Select(title='Poverty Level',value = poverty[0],options=poverty)
# button widgets
updatebutton = Button(label="Update Figure", button_type="success")


# store all filter settings in dictionary
f = mapFilters()

##############
#### baseline predictions
#############

# prepare vector for prediction

rf = pickle.load(open("./data/dc_rf_model.p","rb" ))
model_input_vector = models.make_vector(mapPredictors(f))
output = models.make_changes(model_input_vector, rf)
source = ColumnDataSource(data=output.head(5))
prob = rf.predict_proba(model_input_vector)[:,1]

###############
# create figure
##############
counts = make_bar(source, 'Rec_Number', 'Score')

#############
### layout
#############

# widgets
w = widgetbox(stateselect, fieldselect, resource_type,
              giving_page, giving_page_size, month,
              grade_level, dym, ahm,
              updatebutton)
=======
updatebutton = Button(label="Update Figure", button_type="success")

#div = Div(text='{}% funding chance'.format(prob), width=200, height=100)
>>>>>>> 39405f464a21d68b13d140c765496fe9c817b55f

# layout
l = layout([[w, counts]])

<<<<<<< HEAD
###########
### Interactivity
##########

#update plot based on filters on click
updatebutton.on_click(update_plot)

###########
###output
###########

# add to file and show
=======
w = widgetbox(stateselect, fieldselect, updatebutton)#, div)

# filter settings
#stateselect.on_change('value', update_plot)
updatebutton.on_click(update_plot)


# layout
l = layout([[w, counts]])

#show
#show(l)

>>>>>>> 39405f464a21d68b13d140c765496fe9c817b55f
curdoc().add_root(l)
curdoc().title = "Predictive Dashboard"
