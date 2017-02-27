from flask import Flask, flash, redirect, render_template, request, session, abort
from bokeh.embed import autoload_server
app = Flask(__name__)

@app.route("/")
def hello():
    script=autoload_server(model=None,app_path="/bokeh-sliders",url="http://10.140.0.46/bokehapp")
    #return render_template('hello.html',bokS=script)
    return render_template('index.html',bokS=script)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
