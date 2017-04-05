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

def mapTF(string):
    return {
        'Yes': 't',
        'No':  'f'
        }[string]

def mapNum(string):
    return {
        'Yes': 1,
        'No':  0
        }[string]

def mapBinary(string):
    return {
        'Yes': True,
        'No':  False
        }[string]

def monthToNum(string):
    return {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }[string.strip()[:3].lower()]
