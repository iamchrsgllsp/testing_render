from flask import Flask, render_template

app = Flask(__name__, static_folder="static")


@app.route('/')
def hello_world():
  return render_template("home.html")


@app.route('/test')
def test():
  return """<form hx-put="/contact/1" hx-target="this" hx-swap="outerHTML">
  <div>
    <label>First Name</label>
    <input type="text" name="firstName" value="Joe">
  </div>
  <div class="form-group">
    <label>Last Name</label>
    <input type="text" name="lastName" value="Blow">
  </div>
  <div class="form-group">
    <label>Email Address</label>
    <input type="email" name="email" value="joe@blow.com">
  </div>
  <button class="btn">Submit</button>
  <button class="btn" hx-get="/contact/1">Cancel</button>
</form>
  """


@app.route('/func')
def func():
  return "func"


#comment out below before deploying on render
#app.run(host="0.0.0.0", port=8080, debug=True)
