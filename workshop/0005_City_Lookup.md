# Lookup the time in a city

The final feature we'd like to add is the ability to get the time in a given city / country.
We can continue to use the same endpoint and provide `city` and `country` in the request.

You'll need to add the Cities to your database by creating a model.
Models are interesting to write with TDD, here's a pattern that I like:

```python
def test_can_create_person(self):
    person = Person.objects.create(
        name="Brenton Cleeland",
        country="AU",
        twitter="@sesh",
    )
```

The _problem_ with that is that the test isn't failing by rather the test is broken.
We can fix that by catching that exception and providing a proper message using `self.fail()`.

```python
def test_can_create_person(self):
    try:
        person = Person.objects.create(
            name="Brenton Cleeland",
            country="AU",
            twitter="@sesh",
        )
    except:
        self.fail('Creating model caused an exception')
```

---

Now, on to the feature we'd like to add:

## As a user I want to provide the name of a city and country and get the current time in that location

- The application should keep a database of Cities with name, country and timezone
- The `/api/time/` endpoint should accept `city` and `country` parameters
  - The country should be a two character country code
- If the city doesn't exist in the database a 404 should be returned
- The response should be JSON and include `current_time`, `city` and `country` fields

---

Again, here are the tests that I started with (spoiler alert!):

- test_can_create_city
- test_city_response_contains_city
- test_city_response_contains_country
- test_city_response_contains_correct_time_key
- test_city_response_contains_correct_time
- test_city_api_returns_404_if_not_found

Can you think of some tests that are missing? What about some edge cases and error states?
How would you use TDD to test validation of the country or timezone?
