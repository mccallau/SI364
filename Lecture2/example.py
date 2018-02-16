from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'This is the main page. <a href="http://localhost:5000/form1">Click here to see the form.</a>'

@app.route('/form1')
def form1():
    return """ <form action="http://localhost:5000/result" method='GET'>
  <input type="checkbox" name="vehicle1" value="Bike"> I have a bike<br>
  <input type="checkbox" name="vehicle2" value="Car"> I have a car<br>
  <input type="checkbox" name="vehicle3" value="Trolley"> I have a trolley
  <input type="submit" value="Submit">
</form>"""

@app.route('/result',methods=["GET"])
def result_form1():
    if request.method == "GET":
        print(request.args) # Check out your Terminal window where you're running this...
        result_str = ""
        for k in request.args:
            result_str += "{} - {}<br><br>".format(k, request.args.get(k,""))
        return result_str
    return "Nothing was selected this time!"

@app.route('/form2')
def form2():
    return """<form action="http://localhost:5000/letter" method='GET'>
    <input type="text" name="phrase"><br>
    <input type="submit" value="Submit">
    """

@app.route('/letter',methods=["GET"])
def letters_result():
    if request.method == "GET":
        phrase = request.args.get('phrase','')
        total_number = 0
        for ch in phrase:
            if ch.lower() == "e":
                total_number += 1
        if total_number ==1:
        	return "There were {} occurrence of the letter e in the entered phrase".format(total_number)
        else:
        	return "There were {} occurrences of the letter e in the entered phrase".format(total_number)
        # Challenge: how would you change this to say "occurrence" in the case there's only 1 'e'?
    return "Nothing was submitted yet... <a href='http://localhost:5000/form2'>Go submit something</a>"


if __name__ == "__main__":
    app.run(use_reloader=True, debug=True) # Nice trick -- see details in lecture notes
