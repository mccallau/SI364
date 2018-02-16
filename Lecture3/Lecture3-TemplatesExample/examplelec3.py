from flask import Flask, request, render_template, url_for

app = Flask(__name__)

@app.route('/oranges')
def lemons():
    title_var = "My Ice Cream Form"
    options=["Vanilla","Chocolate","Pistachio","So many others!"]
    return render_template('seeform.html',title=title_var, lst_stuff=options)

@app.route('/apples',methods = ['GET'])
def plants():
    arg = request.args
    name = arg['name']
    name_len=len(name)
    flavor_options=[x for x in arg if x!='name']
    return render_template('results.html',flavors=flavor_options, name_len=name_len, name=name)


if __name__ == "__main__":
    app.run(use_reloader=True,debug=True)
