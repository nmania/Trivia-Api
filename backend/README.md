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

----

## Endpoints documentation

<!-- REVIEW_COMMENT -->
<!-- ``` -->
<!-- This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code.  -->

Documentation of the available application's endpoints.

#### `GET '/categories'`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: A multiple key/value pairs object with the following structure:
    - `success`: can take values `True` or `False` deppending on the successfullnes of the endpoint's execution.
    - `status_code`: contains the response status code.
    - `status_message`: contains the a message related with the staus of the reponse, i.e: `error` and `OK`.
    - `categories`: dictionary of categories available in the database.
    - `total_categories`: the number of questions returned.
    
```JSON
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "status_code": 200, 
  "status_message": "OK", 
  "success": true, 
  "total_categories": 6
}

```

#### `GET '/questions'`
- Fetches a dictionary of quetions.
- Request Arguments: Page's number (optional)
- Returns: A multiple key/value pairs object with the following structure:
    - `success`: can take values `True` or `False` deppending on the successfullnes of the endpoint's execution.
    - `status_code`: contains the response status code.
    - `status_message`: contains the a message related with the staus of the reponse, i.e: `error` and `OK`.
    - `questions`: contains a list of the fetched questions. Each question is a key/value pairs object containing `id`,  `question`, `category` and  `diffficulty`.
    - `total_questions`: the number of questions returned.
    - `current_category`: list of the categories of the returned questions list.
    - `categories`: dictionary of categories available in the database.

Here is an example of the returned object:

```JSON
{
  "categories": {
    "1": "Science"
  }, 
  "current_category": [
    1
  ], 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {...}
  ], 
  "status_code": 200, 
  "status_message": "OK", 
  "success": true, 
  "total_questions": 5
}
```

#### `DELETE '/questions/<int:question_id>'`
- Deletes the question selectecd by `question_id`.
- Request Arguments: `question_id` (required)
- Returns: A multiple key/value pairs object with the following structure:
    - `success`: can take values `True` or `False` deppending on the successfullnes of the endpoint's execution.
    - `status_code`: contains the response status code.
    - `status_message`: contains the a message related with the staus of the reponse, i.e: `error` and `OK`.
    - `questions`: contains a list of the fetched questions. Each question is a key/value pairs object containing `id`,  `question`, `category` and  `diffficulty`.
    - `total_questions`: the number of questions returned.
    - `current_category`: list of the categories of the returned questions list.
    - `categories`: dictionary of categories available in the database.

Here is an example of the returned object:

```JSON
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": [
    2, 
    3, 
    4, 
    5, 
    6
  ], 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {...}
  ], 
  "status_code": 200, 
  "status_message": "OK", 
  "success": true, 
  "total_questions": 17
}
```

#### `POST '/questions'`
- Inserts a new question in the database.
- Request Arguments: a key/value pairs object whit the following content:
    - `question`: string containing the question itself.
    - `answer`: answer's string.
    - `difficulty`: difficulty level.
    - `category`: category ID field.

Example of the object:

```JSON
{
    answer: "It depends"
    category: 1
    difficulty: 1
    question: "Can birds fly?"
}
```

- Returns: A multiple key/value pairs object with the following structure:
    - `success`: can take values `True` or `False` deppending on the successfullnes of the endpoint's execution.
    - `status_code`: contains the response status code.
    - `status_message`: contains the a message related with the staus of the reponse, i.e: `error` and `OK`.
    - `questions`: contains a list of the fetched questions. Each question is a key/value pairs object containing `id`,  `question`, `category` and  `diffficulty`.
    - `total_questions`: the number of questions returned.
    - `current_category`: list of the categories of the returned questions list.
    - `categories`: dictionary of categories available in the database.

Here is an example of the returned object:

```JSON
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": [
    2, 
    3, 
    4, 
    5, 
    6
  ], 
  "questions": [
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {...}
  ], 
  "status_code": 200, 
  "status_message": "OK", 
  "success": true, 
  "total_questions": 17
}
```

#### `POST '/questions_by_phrase'`
- Returns a set of questions based on a search term.
- Request Arguments: 
    - `searchTerm`: string to search in questions string.
- Returns: A multiple key/value pairs object with the following structure:
    - `success`: can take values `True` or `False` deppending on the successfullnes of the endpoint's execution.
    - `status_code`: contains the response status code.
    - `status_message`: contains the a message related with the staus of the reponse, i.e: `error` and `OK`.
    - `questions`: contains a list of the fetched questions. Each question is a key/value pairs object containing `id`,  `question`, `category` and  `diffficulty`.
    - `total_questions`: the number of questions returned.
    - `current_category`: list of the categories of the returned questions list.
    - `categories`: dictionary of categories available in the database.

Here is an example of the returned object:

```JSON
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": [
    5
  ], 
  "questions": [
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ], 
  "status_code": 200, 
  "status_message": "OK", 
  "success": true, 
  "total_questions": 1
}

```

#### `GET '/categories/<int:category_id>/questions'`
- Returns a subset of questions that belongs to an specific category.
- Request Arguments:
    - `category_id`: category id field.
- Returns: A multiple key/value pairs object with the following structure:
    - `success`: can take values `True` or `False` deppending on the successfullnes of the endpoint's execution.
    - `status_code`: contains the response status code.
    - `status_message`: contains the a message related with the staus of the reponse, i.e: `error` and `OK`.
    - `questions`: contains a list of the fetched questions. Each question is a key/value pairs object containing `id`,  `question`, `category` and  `diffficulty`.
    - `total_questions`: the number of questions returned.
    - `current_category`: list of the categories of the returned questions list.
    - `categories`: dictionary object containing the selected category.

Here is an example of the returned object:
```JSON
{
  "categories": {
    "1": "Science"
  }, 
  "current_category": [
    1
  ], 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "It depends", 
      "category": 1, 
      "difficulty": 1, 
      "id": 77, 
      "question": "Can birds fly?"
    },
    {...}
  ], 
  "status_code": 200, 
  "status_message": "OK", 
  "success": true, 
  "total_questions": 5
}
```


#### `POST '/quizzes'`
- Iteratively executes the game asking questions to player.
- Request Arguments:
    - `category_id`: question's category id field.
    - `previous_quesion`: question in the previous iteration, first time it's an empty string.
- Returns: A multiple key/value pairs object with the following content:
    - `success`: can take values `True` or `False` deppending on the successfullnes of the endpoint's execution.
    - `status_code`: contains the response status code.
    - `status_message`: contains the a message related with the staus of the reponse, i.e: `error` and `OK`.
    - `question`: contains the question. Question is a key/value pairs object containing `id`,  `question`, `answer`, `category` and  `diffficulty`.

Here is an example of the returned object:
```JSON
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }, 
  "status_code": 200, 
  "status_message": "OK", 
  "success": true
}
```

## Errors handling:
All endpoints are provided with error handlers functions which return the following key/value pairs JSON content:
- `success`: False.
- `error`: error code number.
- `message`: error message string giving a brief description of the kind of error.

Here is an example of the returned object:

```JSON
{
    "success": False,
    "error": 404,
    "message": "Resource Not found"
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

To allow an easier and faster application testing, you can execute `test.sh` script. :)
