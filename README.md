# tic-tac-toe-api
REST API for playing tic tac toe.

## Delivery

### How to run
- Create a python (3.8+) virtual environment
- Install dependencies with: `pip install -r requirements.txt`
- Run app with: `uvicorn api.main:app`
- Type check with: `mypy --strict api`  (TODO: some type errors exist)
- Lint code with: `flake8 api`
- Run tests with: `pytest`

### Time spent
- About 4 hours had passed when commit `23b187efa8f36328101535307305913b7190b2d1`
  was made. At that point, CRUD for players and games was finished,
  but I hadn't added CRUD for moves yet. I think I started on a path
  of over-engineering everything with adding tests, getting a bit
  stuck on Mypy generics, and having to consult the FastAPI and
  Pydantic docs. I think if I just did a minimal flask app (I have
  more experience with flask) without worring about linting, testing,
  type-checking etc. I *might* have been able to finish or get closer.
- I spent another 2-ish hours getting moves to work (adjusting for
  small breaks and lunch) for a total of 6 hours.

### Assumptions
- Assume the server will never crash or else all data will be lost.
  (The application uses a super fast in-memory database :))

### Trade-offs
- Started out with exhaustive testing and type checking before
  realizing I was spending too much time on this. After that
  tests became more coupled and less exhaustive and type checking
  was ignored.
- Use an in-memory fake database to avoid time spent setting a
  database up and having a more complicated dev environment using
  something like Docker and docker-compose.

### Special/unique features
- Two human players can play - the computer player is the default
  for 'Player Two' if only 'Player One' is specified when the game is
  created.
- Compute if the game is over and determine the winner (though this was
  finished in the 2 hours beyond the 4 hour window).

### Anything else

### Feedback
- I thought this was a great project! I particularly liked the
  requirement to view all moves in a game. This makes it so you
  can't just store the current state of the game, but instead you
  have to store the moves separately. It was difficult for me to
  squeeze all of these features into the 4 hour window, but it was
  a good amount of work to make for a fun challenge.
