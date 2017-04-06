from flask import Flask, flash, redirect, render_template, request, session, abort
from bokeh.embed import autoload_server
app = Flask(__name__)

@app.route("/")
def hello():
<<<<<<< HEAD
    script=autoload_server(model=None,app_path="/bokeh-sliders",url="http://10.140.0.48/bokehapp")
=======
    script=autoload_server(model=None,app_path="/bokeh-sliders",url="http://ec2-52-90-132-56.compute-1.amazonaws.com/bokehapp")
>>>>>>> 39405f464a21d68b13d140c765496fe9c817b55f
    #return render_template('hello.html',bokS=script)
    return render_template('index.html',bokS=script)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
