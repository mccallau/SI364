from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def main_page():
    return "Here's the main page. <a href='http://localhost:5000/seeform'>Click here to see the form</a>."

@app.route('/seeform',methods=["GET","POST"])
def see_form():
    formstring = """<br><br>
    <form action="" method='POST'>
    Enter a phrase: <br>
<input type="text" name="phrase"> 
<input type="submit" value="Submit">
""" ## HINT: In there ^ is where you need to add a little bit to the code...
    if request.method == "POST":
        rq=request.form['phrase']
        return formstring+'<br>'+rq
    else:
        return formstring




if __name__ == "__main__":
    app.run(use_reloader=True, debug=True)
