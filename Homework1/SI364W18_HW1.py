## HW 1
## SI 364 W18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".

#Worked with William Waters

#No resources found for code

## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

import requests #For making requests to the iTunes api
import json #For reading in api data
import urllib #For making requests to the giantbomb video game api, the requests library was not retrieving the data in the correct format (xml instead of json)
from flask import Flask, request
import apikey #Pulling in API key for problem 4
APIkey = apikey.api_key #Replace blank string in apikey.py file with key provided on Canvas or your own key

#To get an API key yourself, go to https://www.giantbomb.com/api/, sign-up with an account (can use a Google account) and an API key will be generated for you



app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_to_you():
    return 'Hello!'


@app.route('/class')
def hello_to_si364():
    return 'Welcome to SI 364!'



## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }

@app.route('/movie/<moviename>')
def movie(moviename):
	rq = requests.get("https://itunes.apple.com/search?term={}&entity=movie".format(moviename))
	rq = json.loads(rq.text)
	return str(rq)



## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.

@app.route('/question')
def numfav():
	s = """<!DOCTYPE html>
	<html>
	<body>
	<form action="/result" method="POST">
  	<h1>Enter your favorite number:</h1>
  	<input type="text" name="number">
  	<br><br>
  	<input type="submit" value="Submit">
	</form>
	</body>
	</html>"""
	return s

@app.route('/result',methods = ['POST', 'GET'])
def displayData():
	if request.method == 'POST': 
		s="""<!DOCTYPE html>
			<html>
			<body>
			<h1>Double your favorite number is {}</h1>
			</body>
			</html>""".format(str(int(request.form['number'])*2))
		return s



## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

@app.route('/problem4form',methods = ['GET','POST'])
def prob4display():
	try: #try/excepts are used to display the results on the same page as the form
		req = dict(request.form)['game'][0] #Game that is entered on the form
		requestedreleaseform = int(request.form['releasedate']) #Release date range that the user selects on the form
		requestedplatformform = dict(request.form)['platform'] #Platforms that the user selects on the form
		listedplatforms = ["PC","Mac","Xbox","Xbox 360","Xbox One","PlayStation 1","PlayStation 2","PlayStation 3","PlayStation 4","Nintendo Entertainment System","Super Nintendo Entertainment System","Nintendo 64","Nintendo DS","Nintendo 3DS","Game Boy Advance","GameCube","Wii","Wii U","Nintendo Switch"] #Platforms that are selectable on the form
		res=""
		try:
			for page in range(15): #Looks through maximum of 15 pages of results
				params=urllib.parse.urlencode({'api_key':APIkey,'format':'json','query':'{}'.format(req),'resources':'game','page':page})
				response = urllib.request.urlopen("https://www.giantbomb.com/api/search/?"+params) #https://www.giantbomb.com/api/ Video game API
				js = json.loads(response.read())
				try:
					for item in range(10): #There are max 10 results per page
						if res.count("<li>") <20: #Only going to display up to 20 results to the user on the form
							gamereleaseyear = int(js['results'][item]['original_release_date'].split('-')[0]) #Pulls the actual release year from the game
							gameplatforms = [x['name'] for x in js['results'][item]['platforms']] #Pulls the actual game platform
							if ((requestedreleaseform==2000) and (gamereleaseyear<=1999)) or ((requestedreleaseform != 2000) and (((requestedreleaseform-gamereleaseyear)<=4) and ((requestedreleaseform-gamereleaseyear)>=0))) or ((requestedreleaseform==2015) and (gamereleaseyear>=2015)): #Many date factors had to be covered
							 #Following if statements compare the requested platforms and release dates to the actual 
								if len([e for e in gameplatforms if e in requestedplatformform])>0:
									res=res+"<li>{}</li>".format(js['results'][item]['name']+" --- platforms: "+str(gameplatforms)+" --- originally released: "+str(gamereleaseyear))
								elif ("Other" in requestedplatformform) and len([x for x in gameplatforms if x not in listedplatforms]): #Looks for unlisted (on form) platforms if the user selects "Other"
									res=res+"<li>{}</li>".format(js['results'][item]['name']+" --- platforms: "+str(gameplatforms)+" --- originally released: "+str(gamereleaseyear))
						else: break #Breaks the inner search loop if 20 results found
					else: continue
					break #Breaks the outer search loop if 20 results found
				except:
					pass
		except:
			pass
	except:
		res=" "
	if res != " ": #Intended for messages left for the user upon the display of the results
		if res != "":
			notifier = "If you did not find what you were looking for, try refining the search terms"
		else:
			notifier = "No results found, please change your search terms and try again"
		resultheader = '<h2>Game Results</h2>'
	else:
		notifier=""
		resultheader = ""
	defaultstring="""<!DOCTYPE html>
	<html>
	<h1>Video Game Search</h1><br>
	<h2>Enter a search term:</h2>
	<body>
	<form action="/problem4form" method="POST">
  	<input type="text" name="game"><br>
  	<h2>Enter the game's release date to filter:</h2><br>
  	<input type="radio" name="releasedate" value="2000"> Pre-2000's<br>
  	<input type="radio" name="releasedate" value="2004"> 2000 - end of 2004<br>
  	<input type="radio" name="releasedate" value="2009"> 2005 - end of 2009<br>
  	<input type="radio" name="releasedate" value="2014"> 2010 - end of 2014<br>
  	<input type="radio" name="releasedate" value="2015"> 2015 - Now<br>
  	<h2>Enter platforms to filter (must enter at least one platform):</h2><br>
  	<input type="checkbox" name="platform" value="PC"> PC<br>
  	<input type="checkbox" name="platform" value="Mac"> Mac<br>
  	<input type="checkbox" name="platform" value="Xbox"> Xbox<br>
  	<input type="checkbox" name="platform" value="Xbox 360"> Xbox 360<br>
  	<input type="checkbox" name="platform" value="Xbox One"> Xbox One<br>
  	<input type="checkbox" name="platform" value="PlayStation 1"> Playstation 1<br>
  	<input type="checkbox" name="platform" value="PlayStation 2"> Playstation 2<br>
  	<input type="checkbox" name="platform" value="PlayStation 3"> Playstation 3<br>
  	<input type="checkbox" name="platform" value="PlayStation 4"> Playstation 4<br>
  	<input type="checkbox" name="platform" value="Nintendo Entertainment System"> Nintendo Entertainment System<br>
  	<input type="checkbox" name="platform" value="Super Nintendo Entertainment System"> Super Nintendo Entertainment System<br>
  	<input type="checkbox" name="platform" value="Nintendo 64"> Nintendo 64<br>
  	<input type="checkbox" name="platform" value="Nintendo DS"> Nintendo DS<br>
  	<input type="checkbox" name="platform" value="Nintendo 3DS"> Nintendo 3DS<br>
  	<input type="checkbox" name="platform" value="Game Boy Advance"> Game Boy Advance<br>
  	<input type="checkbox" name="platform" value="GameCube"> GameCube<br>
  	<input type="checkbox" name="platform" value="Wii"> Wii<br>
  	<input type="checkbox" name="platform" value="Wii U"> Wii U<br>
  	<input type="checkbox" name="platform" value="Nintendo Switch"> Nintendo Switch<br>
  	<input type="checkbox" name="platform" value="Other"> Other<br>
  	<br><br>
  	<input type="submit" value="Submit">
	</form>
	<br>
	{}
	<ul>
	{}
	</ul>
	{}<br>
	</body>
	</html>"""


	try: #These modify the HTML so any of the user's inputs stay on the page after the results are displayed
		for platform in requestedplatformform:
			defaultstring = defaultstring[:(defaultstring.index(platform)+len(platform)+1)] + " checked" + defaultstring[(defaultstring.index(platform)+len(platform)+1):]
		defaultstring = defaultstring[:defaultstring.index(str(requestedreleaseform))+5] + " checked" + defaultstring[defaultstring.index(str(requestedreleaseform))+5:]
		defaultstring = defaultstring[:(defaultstring.index('name="game"')+11)]+'value='+'"'+req+'"'+defaultstring[(defaultstring.index('name="game"')+11):]
	except:
		defaultstring = defaultstring[:(defaultstring.index("2000")+5)] + " checked" + defaultstring[(defaultstring.index("2000")+5):]
	s = defaultstring.format(resultheader,res,notifier)
	return s

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.


if __name__ == '__main__':
    app.run()