# Let's add timezone support

Up until now we've gotten away with returning just the current UTC time.
Lets extend our solution to accept a `timezone` from the user and return the current time in that timezone.

This one is all on you! What is the first test that you'd like to write?

---

## As a user I want to receive the current time _in the timezone that I provide_ so I can see what time it is

- The `/api/time/` endpoint should accept a `timezone` query parameter that provides a timezone in the IANA "Australia/Melbourne" format
- The response should include `timezone`, `offset` and `current_time` fields
  - The `timezone` field should include the name of the timezone
  - The `offset` field should include the current offset for the timezone in `±hhmm` format
  - The `current_time` field should include the current time in the specified timezone
    - The time should be returned in a [ISO 8601](iso8601) compatible format: 2018-04-29T02:33:24±hhmm
- If the timezone doesn't exist, the response code should be 400 and an `error` key should be provided in the JSON

---

What tests did you write? Here's how I got started (spoilers!)

- test_timezone_response_contains_timezone
- test_timezone_should_return_400_for_bad_timezone
- test_timezone_response_contains_offset
- test_timezone_response_includes_correct_time
- test_timezone_error_message

My test concentrate on the happy path and don't test many edge cases.
Take a moment to think about other things that you could have tested.
