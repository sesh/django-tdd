# Time API Kata

Follow along as we complete our first user story using TDD.

You should have [created a Django project called time_api](0001_GettingStarted.md) before continuing.

---

## As a user I want to receive the current UTC time so I can ensure my clock is correct

- The `/api/time` endpoint should return a JSON response with a `current_time` key
- If successful, the status code should be 200 OK
- All times should be in ISO 8601 format

For now, just follow along. You'll write your own version in the next step.

---

Let's start by thinking about the smallest piece of this story.
To me that's that the URL will be `/api/time/`.
We can write a simple test to ensure that we receive a 200 OK from the endpoint.

The Django test Client handles a lot of the heavy lifting for us – we will use `self.client.get()` to make a HTTP request to our desired endpoint, and `response.status_code` to confirm the status code.

<div style="display: flex; flex-basis: 50%;">

  ```python
  # time_api/tests.py
  from django.test import TestCase

  class TimeApiTestCase(TestCase):

      def test_time_url_is_status_okay(self):
          response = self.client.get('/api/time/')
          self.assertEqual(200, response.status_code)
  ```

  ```python
  # time_api/urls.py
  ```

</div>

Run the test to make sure it fails, and fails for the right reason.
We receive a message saying the 404 is not 200.

Django is successfully handling the request and returning the default 404 template for us.

Although this it being ran by the Python "unit test" framework this is an integration test.
When we make the call the `Client.get()` the full Django request / response lifecycle is ran.
For now that's okay, but we should look at how we can separate smaller units in the future.

Let's add some code to our `urls.py` to make our URL work.
Remember that we want to write the smallest amount of code we can to make the test pass.

We'll add the path (#1), create the view (#2) and return a HttpResponse (#3) to make our test happy.

<div style="display: flex; flex-basis: 50%;">

  ```python
  # time_api/tests.py
  from django.test import TestCase

  class TimeApiTestCase(TestCase):

      def test_time_url_is_status_okay(self):
          response = self.client.get('/api/time/')
          self.assertEqual(200, response.status_code)
  ```

  ```python
  # time_api/urls.py
  from django.contrib import admin
  from django.urls import path

  from django.http import HttpResponse  # 3

  def time_api(request):  # 2
      return HttpResponse()

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/time/', time_api),  # 1
  ]

  ```

</div>

We've just written our first piece of code that was **test driven**. Congratulations 👏

Now we need to think about whether or not we should keep going or refactor some of this code.
For now I think we should continue. What do you think?

The second piece of functionality is the the API should return a JSON response.
You're probably already thinking about how you will write the code to satify this, but what about the test?

The response object that the Django Test Client returns allows us to access the HTTP Headers using the dictionary syntax.
Thanks to this we can write a test that confirms the response's Content-Type is application/json.

<div style="display: flex; flex-basis: 50%;">

  ```python
  # time_api/tests.py
  from django.test import TestCase

  class TimeApiTestCase(TestCase):

      def test_time_url_is_status_okay(self):
          response = self.client.get('/api/time/')
          self.assertEqual(200, response.status_code)

      def test_time_api_should_return_json(self):
        response = self.client.get('/api/time/')
        self.assertEqual('application/json', response['Content-Type'])
  ```

  ```python
  # time_api/urls.py
  from django.contrib import admin
  from django.urls import path

  from django.http import HttpResponse

  def time_api(request):
      return HttpResponse()

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/time/', time_api),
  ]

  ```

</div>

When we run the tests we see that `text/html` doesn't equal `application/json`.
Of course it doesn't!

By far the simplest way to make this test pass is to replace our `HttpResponse` with `JsonResponse` (#1, #2).
Django's built-in `JsonResponse` will handle serialisation for us and make our life far simpler going forward.

<div style="display: flex; flex-basis: 50%;">

  ```python
  # time_api/tests.py
  from django.test import TestCase

  class TimeApiTestCase(TestCase):

      def test_time_url_is_status_okay(self):
          response = self.client.get('/api/time/')
          self.assertEqual(200, response.status_code)

      def test_time_api_should_return_json(self):
        response = self.client.get('/api/time/')
        self.assertEqual('application/json', response['Content-Type'])
  ```

  ```python
  # time_api/urls.py
  from django.contrib import admin
  from django.urls import path

  from django.http import HttpResponse, JsonResponse  # 2

  def time_api(request):
      return JsonResponse({})  # 1

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/time/', time_api),
  ]
  ```

</div>

Should we refactor?

Yes! Let's remove that unused `HttpResponse` import and rearrange the imports to make the always pedantic isort happy.

<div style="display: flex; flex-basis: 50%;">

  ```python
  # time_api/tests.py
  from django.test import TestCase

  class TimeApiTestCase(TestCase):

      def test_time_url_is_status_okay(self):
          response = self.client.get('/api/time/')
          self.assertEqual(200, response.status_code)

      def test_time_api_should_return_json(self):
          response = self.client.get('/api/time/')
          self.assertEqual('application/json', response['Content-Type'])
  ```

  ```python
  # time_api/urls.py
  from django.contrib import admin
  from django.http import JsonResponse
  from django.urls import path

  def time_api(request):
      return JsonResponse({})

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/time/', time_api),
  ]
  ```

</div>

Great. We have two passing tests and we've just done our first refactor to make the code more readable.

Let's continue with the next part of this feature: returing the `current_time` key in the response.

The test case is again very simple (notice a trend?).
Once we have the response, we use the `.json()` function to convert it to a dictionary, and the `in` operator to check for our expected key.

<div style="display: flex; flex-basis: 50%;">

  ```python
  # time_api/tests.py
  from django.test import TestCase

  class TimeApiTestCase(TestCase):

      def test_time_url_is_status_okay(self):
          response = self.client.get('/api/time/')
          self.assertEqual(200, response.status_code)

      def test_time_api_should_return_json(self):
          response = self.client.get('/api/time/')
          self.assertEqual('application/json', response['Content-Type'])

      def test_time_api_should_include_current_time_key(self):
          response = self.client.get('/api/time/')
          self.assertTrue('current_time' in response.json())
  ```

  ```python
  # time_api/urls.py
  from django.contrib import admin
  from django.http import JsonResponse
  from django.urls import path

  def time_api(request):
      return JsonResponse({})

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/time/', time_api),
  ]
  ```

</div>

All going well things fail for the correct reason here.
The key "current_time" shouldn't exist in our JSON response.

Let's update our view to return the expected key (#1). For now there's no reason (test!) to return anything other than an empty string.


<div style="display: flex; flex-basis: 50%;">

  ```python
  # time_api/tests.py
  from django.test import TestCase

  class TimeApiTestCase(TestCase):

      def test_time_url_is_status_okay(self):
          response = self.client.get('/api/time/')
          self.assertEqual(200, response.status_code)

      def test_time_api_should_return_json(self):
          response = self.client.get('/api/time/')
          self.assertEqual('application/json', response['Content-Type'])

      def test_time_api_should_include_current_time_key(self):
          response = self.client.get('/api/time/')
          self.assertTrue('current_time' in response.json())
  ```

  ```python
  # time_api/urls.py
  from django.contrib import admin
  from django.http import JsonResponse
  from django.urls import path

  def time_api(request):
      return JsonResponse({
          'current_time': ''  # 1
      })

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/time/', time_api),
  ]
  ```

</div>

We run the tests and make sure that they're passing.
They should be! We're returning the response exactly as we want it.

Again think about refactoring this code. For now I think we're okay... But if there's anything you're interested in changing, go ahead.

Now it's time to return an actual date. We need to format it the ISO 8601 format, and we can test that by parsing it in our test and confirming we receive a datetime object.

<div style="display: flex; flex-basis: 50%;">

  ```python
  # time_api/tests.py
  from django.test import TestCase

  class TimeApiTestCase(TestCase):

      def test_time_url_is_status_okay(self):
          response = self.client.get('/api/time/')
          self.assertEqual(200, response.status_code)

      def test_time_api_should_return_json(self):
          response = self.client.get('/api/time/')
          self.assertEqual('application/json', response['Content-Type'])

      def test_time_api_should_include_current_time_key(self):
          response = self.client.get('/api/time/')
          self.assertTrue('current_time' in response.json())

      def test_time_api_should_return_valid_iso8601_format(self):
          response = self.client.get('/api/time/')
          current_time = response.json()['current_time']
          dt = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ')
          self.assertTrue(isinstance(dt, datetime))
  ```

  ```python
  # time_api/urls.py
  from django.contrib import admin
  from django.http import JsonResponse
  from django.urls import path

  def time_api(request):
      return JsonResponse({
          'current_time': ''
      })

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/time/', time_api),
  ]
  ```

</div>

Think about the simplest code the we can write to make this pass for a moment.
Do we need to return the _current time_ for this test to pass? No, we don't.

Let's update the view return a valid date. In this case, the release date of In Rainbows by Radiohead.

<div style="display: flex; flex-basis: 50%;">

  ```python
  # time_api/tests.py
  from django.test import TestCase

  class TimeApiTestCase(TestCase):

      def test_time_url_is_status_okay(self):
          response = self.client.get('/api/time/')
          self.assertEqual(200, response.status_code)

      def test_time_api_should_return_json(self):
          response = self.client.get('/api/time/')
          self.assertEqual('application/json', response['Content-Type'])

      def test_time_api_should_include_current_time_key(self):
          response = self.client.get('/api/time/')
          self.assertTrue('current_time' in response.json())

      def test_time_api_should_return_valid_iso8601_format(self):
          response = self.client.get('/api/time/')
          current_time = response.json()['current_time']
          dt = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ')
          self.assertTrue(isinstance(dt, datetime))
  ```

  ```python
  # time_api/urls.py
  from django.contrib import admin
  from django.http import JsonResponse
  from django.urls import path

  def time_api(request):
      return JsonResponse({
          'current_time': '2007-10-10T08:00:00Z'
      })

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/time/', time_api),
  ]
  ```

</div>

What we did there was writing the _simplest piece of code_ that we needed to.
Our test passes with flying colours since we aren't testing anything other than that we're returning a valid datetime.

At this point we can refactor to **generalise** the solution.
In this position there's a better option though: let's add a new test that forces us to **generalise** the solution.

By using the mocking library build into Python 3 we can know in advance the date that we'll return from a call to Django's `timezone.now()`.

What we're about to do is called "patching the response" and works a like this:

```python
with patch('django.utils.timezone.now') as mock_tz_now:
    expected_datetime = datetime(2018, 1, 1, 10, 10)
    mock_tz_now.return_value = expected_datetime
```

By using that code in our test we know that the date that `django.utils.timezone.now` returns will be ten minutes past ten on January 1st, 2018.

Let's add a test that using this pattern and forces us to generalise our solution.

<div style="display: flex; flex-basis: 50%;">

  ```python
  # time_api/tests.py
  from django.test import TestCase

  class TimeApiTestCase(TestCase):

      def test_time_url_is_status_okay(self):
          response = self.client.get('/api/time/')
          self.assertEqual(200, response.status_code)

      def test_time_api_should_return_json(self):
          response = self.client.get('/api/time/')
          self.assertEqual('application/json', response['Content-Type'])

      def test_time_api_should_include_current_time_key(self):
          response = self.client.get('/api/time/')
          self.assertTrue('current_time' in response.json())

      def test_time_api_should_return_valid_iso8601_format(self):
          response = self.client.get('/api/time/')
          current_time = response.json()['current_time']
          dt = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ')
          self.assertTrue(isinstance(dt, datetime))

      def test_time_api_should_return_current_utc_time(self):
          with patch('django.utils.timezone.now') as mock_tz_now:
              expected_datetime = datetime(2018, 1, 1, 10, 10)
              mock_tz_now.return_value = expected_datetime

              response = self.client.get('/api/time/')
              current_time = response.json()['current_time']
              parsed_time = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ')

              self.assertEqual(parsed_time, expected_datetime)
  ```

  ```python
  # time_api/urls.py
  from django.contrib import admin
  from django.http import JsonResponse
  from django.urls import path

  def time_api(request):
      return JsonResponse({
          'current_time': '2007-10-10T08:00:00Z'
      })

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/time/', time_api),
  ]
  ```

</div>

Run the tests and make sure it fails.
It should complain that _whatever time it is now_ isn't the same as when Radiohead released In Rainbows (2007-10-10T08:00:00Z).

Now we can using `timezone.now()` (#1) to return the current time and `strftime()` (#2) to make sure it's formatted correctly.

<div style="display: flex; flex-basis: 50%;">

  ```python
  # time_api/tests.py
  from django.test import TestCase

  class TimeApiTestCase(TestCase):

      def test_time_url_is_status_okay(self):
          response = self.client.get('/api/time/')
          self.assertEqual(200, response.status_code)

      def test_time_api_should_return_json(self):
          response = self.client.get('/api/time/')
          self.assertEqual('application/json', response['Content-Type'])

      def test_time_api_should_include_current_time_key(self):
          response = self.client.get('/api/time/')
          self.assertTrue('current_time' in response.json())

      def test_time_api_should_return_valid_iso8601_format(self):
          response = self.client.get('/api/time/')
          current_time = response.json()['current_time']
          dt = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ')
          self.assertTrue(isinstance(dt, datetime))

      def test_time_api_should_return_current_utc_time(self):
          with patch('django.utils.timezone.now') as mock_tz_now:
              expected_datetime = datetime(2018, 1, 1, 10, 10)
              mock_tz_now.return_value = expected_datetime

              response = self.client.get('/api/time/')
              current_time = response.json()['current_time']
              parsed_time = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ')

              self.assertEqual(parsed_time, expected_datetime)
  ```

  ```python
  # time_api/urls.py
  from django.contrib import admin
  from django.http import JsonResponse
  from django.urls import path
  from django.utils import timezone

  def time_api(request):
      return JsonResponse({
          'current_time': timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')  # 2
      })

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/time/', time_api),
  ]
  ```

</div>

Run the tests and make sure they're happy.
At this point we've _finished_ the features of the story. Nice one!

Let's think about refactoring though. There's a few things that I think we can make better.

Firstly, we can move the magic time formatting string into our settings (#1) and update our view to use the setting instead of having the string hard coded (#2, #3).

<div style="display: flex; flex-basis: 50%;">

  ```python
  # time_api/settings.py

  DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'  # 1
  ```

  ```python
  # time_api/urls.py
  from django.conf import settings
  from django.contrib import admin
  from django.http import JsonResponse
  from django.urls import path
  from django.utils import timezone

  def time_api(request):
      return JsonResponse({
          'current_time': timezone.now().strftime(settings.DATETIME_FORMAT)  # 2
      })

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/time/', time_api),
  ]
  ```

</div>

Run the tests and make sure that our change hasn't broken anything. Nope? All good, let's keep going.

While it's perfectly fine to have this view in our `urls.py`, the "Django-way" is to add views like this into their own apps.
Let's do that now, making sure that our tests still pass along the way.

Firstly, let's create a new app called times.

```
./manage.py startapp times
```

Then we migrate our view code into `times/views.py` and update `time_api/urls.py` to point at that view.

<div style="display: flex; flex-basis: 50%;">

  ```python
  # times/views.py
  from django.conf import settings
  from django.http import JsonResponse
  from django.utils import timezone


  def time_api(request):
      return JsonResponse({
          'current_time': timezone.now().strftime(settings.DATETIME_FORMAT)
      })
  ```

  ```python
  # time_api/urls.py
  from django.contrib import admin
  from django.urls import path

  from times.views import time_api

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('api/time/', time_api),
  ]
  ```

</div>

We used this as a chance to clean up the imports in our `urls.py` as well – most of those aren't needed any more.

Now is a good time to run the tests and make sure they're still being discovered and passing. Green? Great.

As a final step, let's move the tests into `times/tests.py` so that they are closer to the code that they're testing.

```python
# times/tests.py
from datetime import datetime
from unittest.mock import patch

from django.test import TestCase

class TimeApiTestCase(TestCase):

    def test_time_url_is_status_okay(self):
        response = self.client.get('/api/time/')
        self.assertEqual(200, response.status_code)

    def test_time_api_should_return_json(self):
        response = self.client.get('/api/time/')
        self.assertEqual('application/json', response['Content-Type'])


    def test_time_api_should_include_current_time_key(self):
        response = self.client.get('/api/time/')
        self.assertTrue('current_time' in response.json())

    def test_time_api_should_return_valid_iso8601_format(self):
        response = self.client.get('/api/time/')
        current_time = response.json()['current_time']
        dt = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ')
        self.assertTrue(isinstance(dt, datetime))

    def test_time_api_should_return_current_utc_time(self):
        with patch('django.utils.timezone.now') as mock_tz_now:
            expected_datetime = datetime(2018, 1, 1, 10, 10)
            mock_tz_now.return_value = expected_datetime

            response = self.client.get('/api/time/')
            current_time = response.json()['current_time']
            parsed_time = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ')

            self.assertEqual(parsed_time, expected_datetime)
```

Cool. Run the tests one last time to make sure that they're still being discovered. 5 tests passing? Time for a celebratory coffee ☕️
