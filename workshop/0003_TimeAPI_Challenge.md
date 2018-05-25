# Your first TDD view

Now it's your turn to write the Django view to return the current time.
You should do this by writing tests first, running the tests to make sure that they fail, then implementing the code.

Think about how you can break down the work into small testable components.
There's no wrong answers and if you decide to do it differently to how I did that's great!

At the end you should contemplate how you completed the solution and if you'd do it differently next time.

You should have [created a Django project called time_api](0001_GettingStarted.md) before continuing.

---

The task:

## As a user I want to receive the current UTC time so I can ensure my clock is correct

- The `/api/time` endpoint should return a JSON response with a `current_time` key
- If successful, the status code should be 200 OK
- All times should be in ISO 8601 format
