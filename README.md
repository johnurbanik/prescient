# Prescient

Prescient is a proof-of-concept for 'predictive caching.' Namely, prescient predicts the next piece of content
(in this case a simple key) that an individual user will request based on their historical sequence of requests,
and predicts the next request the user will make when it receives each request.

Some precedent exists for the effectiveness of this type of caching; [Netflix uses similar techniques](https://netflixtechblog.com/using-machine-learning-to-improve-streaming-quality-at-netflix-9651263ef09f) to try to preload content.

## Completed:

1. Build a simple python based webserver that takes requests to a 'get' endpoint for a specific key. For the sake of
simplicity, requests also require a user-id. In the future, authentication can be added.
2. Write a script that populates a simple KV-store with \~1m KV-pairs, where each key and value is an int.
3. Write middleware that logs the time, key, and user for each database call (in SQLLite).
4. Come up with a few 'query strategies' that someone would take when deciding their next query. Write scripts that make
synthetic requests based on these strategies, with fixed time between requests for 100 users.
5. Build a system that establishes some various guesses at features.



## TODO:
1. Add guesses to a 'library' of guesses, build a regression on top of this. Compare to a more naive decision tree. 
2. Write a script that tests performance under a few of the query strategies, wherein all users are following one
strategy, but with different initial conditions.
3. Explore using DEAP for co-evolution of features / novelty based scoring.
4. Explore multi-modal uses cases, and develop techniques that can predict well under these mixed modes. This includes when one user has several different strategies or different users have different strategies.
5. Add stochasticity to the query strategies (or move to a stochastic decision process of next action).
6. Add more complex key types (perhaps linked data ala wikipedia ?).
7. Switch to a library of guesses based on multiclass regression or learning to rank.
8. Try to derive some formal bounds on the conditions in which this type of system would be useful.


# Onboarding:

1. `pip install -r requirements.txt` in a virtualenv
2. `python app/scripts/populate_db.py`
