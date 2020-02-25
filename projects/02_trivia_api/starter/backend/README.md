# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/api/categories'
GET '/api/questions'
GET '/api/categories/<int:category_id>/questions'
POST '/api/questions'
POST '/api/quizzes'
DELETE '/api/questions/<int:question_id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
If list is null will return a 422

GET '/api/questions'
- Fetches a dictionary of categories in which the containing a list of the Categories, List of the questions, total number of questons, and the current categories.  The list of Categories will be paged, display 10 questions at a time.   The number of questions per page can be alterd using the QUESTIONS_PER_PAGE global. 
- Request Arguments: Page <int>
- Returns: An object with the keys:
 categories - contains a object of id: category_string key:value pairs
 current_categories - contains a category id
 questions - contains a list object of questions with the keys:
             answer - contains a string with the answer to the question
             category - contains the category id the questions belongs to
             difficulty - contains an int for the difficulty level of the question
             id - contains an int which is the id of the question
             question - contains a string of the question 
 total_questions - int which is the total number of questions in the DB
{
  "categories": {
    "1": "Science", 
    ...
  }, 
  "current_category": 1, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 19
}

GET '/api/categories/<int:category id>/questions'
- Fetches a dictionary of questions filted to the category in the url.
- Request Arguments: none
- Returns:  - Returns: An object with the keys:
 current_categories - contains a category id
 questions - contains a list object of questions with the keys:
             answer - contains a string with the answer to the question
             category - contains the category id the questions belongs to
             difficulty - contains an int for the difficulty level of the question
             id - contains an int which is the id of the question
             question - contains a string of the question 
 total_questions - int which is the total number of questions in the DB
{
  "current_category": "1", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    ...
  ], 
  "success": true, 
  "total_questions": 3
}

POST '/api/questions'
- Depening on the request data if a search term is included it will return a list of filterd questions, or
or it will insert a new question in to the DB.
- Request Arguments: either a dictonary with the key 'searchTerm' value <string> to filter questions.
 or a dictonary with the keys 'question' value <string> ,'answer' value <string>, 'category' <int> category id, 'difficulty' <int> difficulty.
 Returns - Either a 
 Search response:
 {
    'questions': [
          "questions": [
            {
            "answer": "The Liver", 
            "category": 1, 
            "difficulty": 4, 
            "id": 20, 
            "question": "What is the heaviest organ in the human body?"
            },
            ...
     ],
    'totalQuestions': 3,
    'currentCategory': 1
 }
Insert response:
  {"success": true}

POST '/api/quizzes'
Fetches a random question in the supplied category question are filtered by the previous question list.
- Request Arguments: dictionary with the keys:
previous_questions - contains a list of previous question ids
quiz_category - id of the current category id
- Returns - An object with the a key, question, contains a list object of questions with the keys:
             answer - contains a string with the answer to the question
             category - contains the category id the questions belongs to
             difficulty - contains an int for the difficulty level of the question
             id - contains an int which is the id of the question
             question - contains a string of the question 


DELETE '/api/questions/<int:question_id>'
Will delete the question object with the the supplied id
- Request Arguments: None
- Returns   {"success": true} or error 404 the id is not a valid question.

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```