# SI 364 - Winter 2018 - HW 6 (Final Project Plan)

### Deadline: April 11, 2018 11:59 PM
### Total: 1000 points

#### Below: *Overall ; Instructions ; To Submit ; Additional Notes*

As always, you should read these instructions carefully before beginning work.

## Overall

**You do NOT need to fork or clone this, and should not -- only the instructions live here. Everything else we provide lives on Canvas.**

Your goal in this assignment is to complete a few steps to set yourself on a solid path for completing the final project this semester.

You can find the final project requirements **[here](https://github.com/SI364-Winter2018/SI364_Final_Project_Instructions)**.

Your work here must be *your solo work*. All English should come *solely* from you and not come from any collaboration or discussion with others. You may discuss ideas and concepts with others, but may NOT work on specifics together for this assignment and you certainly may not use any text that others have written for your submission(s).

## Instructions

* **Check out the [Final Project requirements](https://github.com/SI364-Winter2018/SI364_Final_Project_Instructions) to come up with an idea that will allow you to fulfill all the requirements you intend to complete.**
    * You should think about stuff like: *How can I briefly describe what my application will do?* and *What type of data should be SAVED in the application? What kind of relationships between entities in the database will I need to make this work?* If it's really hard to come up with answers to questions like that, maybe this idea isn't the right one for the final project and you should come up with another one for this project.

* **Write a paragraph in English describing what your final project application will do, at a high level. Save it in a file `initial_project_idea.txt`.**
    * For example (this is describing an application you saw in class) -- *This application allows users to register and sign in, and save possible tweets that they could post to Twitter on their own account. Users can see all the possible tweets they have saved but can't see other users' tweets.*
    * You *may* also include in this file any other specifics about what content the app will have (as notes for yourself) and why you are planning to build this particular application if you wish.

* **Write the outline of your application in code in a `SI364final.py` file.** What does that mean? This file should include:

    * All import and configuration statements/setup you expect to need, including a database URI. **The database you use for this project plan assignment should be a temporary one -- it should be called `SI364projectplanYOURUNIQNAME`**
    * Definitions of all the model classes you will use, *including* the relationships between database tables
        * So at least 1 one-to-many and 1 many-to-many relationship, including an association table for each many-to-many
        * You should try to anticipate all the relationships you will need and all the fields of data that will need to be in each model
        * You should ensure that these are defined correctly -- the file must be runnable without syntax errors, even if there are no ways to actually view data. (If there's a syntax error in the model, you'll know as soon as you try to run the code with `runserver`!)

    * Decorators (e.g. `@app.route(...)`) and definition statements for all of the view functions you expect to use in the application. Each definition should have `pass` underneath it -- you are not expected to write out the code for the view functions yet.

    * Comments next to each view function definition describing BRIEFLY what that view function should do and what it should render/redirect/return to. e.g. `# Should render form for entering music data and process the data from the form to save it to db with get-or-create. When the form is submitted, should redirect to the same page with the empty form; if not, should just show the form.` Something that makes clear exactly what should happen, so that even one of us would have an idea of what sort of thing to implement.

    * Note that you do NOT have to define the form classes here yet -- but you'll probably want to think about what they will be!

    * This file will certainly not work properly with only this stuff in it, but it should not include syntax errors, and when we run it, it should create the tables in the model classes in the `SI364projectplanYOURUNIQNAME` database. It should simply need a LOT of additions for it to work properly (sort of like a much briefer, much less complete version of the code you were provided in HW4).

* **Write code in a file `practice_api.py`** which:

    * Defines a function that, based on input, will make a request to the/an external API you plan to use in this application and returns data.

    * Invokes that function in a couple different ways (with input that the function might be invoked with in the application itself).

    * Accesses elements of the data inside the return value(s) of those invocations (e.g. `one_tweet = twitter_data['statuses'][0]` or what have you...)

    * Includes *comments* explaining exactly how this data will be integrated into your application, and a comment noting sample inputs to the function that makes requests to the API.
        * For example (this example is also based on a previous class exercise), *Based on users' input to a form, this function will be invoked on that input to return data about movies, and that data will be saved in the Movie db table. // Sample inputs to the form (and thus to the function) could be: Titanic, The Big Chill, Black Panther*
        * Your goal should be to convince us that you feel somewhat confident using this API's data and have a good understanding of how you will access it, and use it, in the application you are building for the final project.


    * This file *should* run, should work. Your goal here in completing this assignment is selecting an API that will work for you and making sure that you can define a function to get data from it that works successfully.
        * (We've done a number of examples of this in this class, as well as in e.g. 106 and 206, so those will be good references to refer to!)

## To submit

You should submit 3 files to the **HW 6 / Final Project Plan** assignment **on Canvas**, corresponding to the instructions above about each one:

* `initial_project_idea.txt` (200 points)
* `SI364final.py` (500 points)
* `practice_api.py` (300 points)

You may also submit additional files if you like -- e.g. if you made drawings to help you plan out your routes and view functions, feel free to take a picture of those or scan them and upload them, as well. **If you upload any additional files, please be VERY clear in your file naming and Canvas submissions what they are and what information they contain.**

Please do NOT submit files as a `.zip`; submit them one by one to the assignment.

## Additional notes

* These commitments are not completely binding (you may change your idea a little bit when you work on the final project itself), but you should consider them somewhat binding. It is *not* a good idea to change dramatically from what you do here; there isn't a lot of time left! **Use this opportunity to make a solid plan and get a really good start on your final project.** It is also an opportunity to get feedback from us.

* I recommend using the structure (with comments laying out the different parts of the code file) that we provided for you in the midterm assignment for your `SI364final.py` file!

* I *strongly* recommend that you continue from your work on this `SI364final.py` to work on your final project. Make it something that's easy to build on -- as if it's a provided file from a homework assignment!

* Useful things to check back on and think about:

    * What will it be like for a user to use the app? What is a use case example (*A user sees this, then clicks this, then can...*)? Consider drawing flow charts to represent how a user could move through the application, as discussed several weeks ago in lecture.
    * You may also want to draw diagrams to represent your database ideas and relationships as you work on definining model classes, if that makes it easier for you! Consider carefully: what should be a one-to-many relationship? What should be a many-to-many?
    * What will you need in your navigation? What should a user be able to see? What different pages should there be? This will help you decide what view functions you need (and ultimately, what templates you'll need!).
    * It's OK to include all of the login machinations in this version of your `SI364final.py`, if you want! (You'll need to include the `User` class, presumably, so you might want to include all of it.)
    * Take it slow. Make drawings. Think about what is going to make the *process* of building an application easier for you.
    * Check out old class exercises, section exercises, examples, HW, lecture notes and exercises, readings, etc, for ideas. (You can't get points for code borrowed directly from any of these, but they can certainly help with inspiration or ideas, as well as understanding of concepts we've covered.)
        * Especially exercises about data flow through applications -- "what happens when..." -- those might help you make decisions here.

* Read API documentation carefully, maybe even take notes, before working on your `practice_api.py` file -- if you do, this process will probably go even faster! One of the reasons for this requirement is so you plan carefully to ensure you *can* get the data you expect to get from whatever API you choose to use.

* It's OK to include API keys and so on in the `practice_api.py` file. You should NOT include these in your final project, ultimately -- we'll provide instructions for how to handle that -- but in this case, you are only submitting this file to Canvas <u>so we can run it</u>.

* **All code files you submit should run (no syntax errors), even if they are unfinished.**
