Test Driven Development with Django

---

My name is _Brenton Cleeland_

---

I work at _Thoughworks_ in Melbourne 🇦🇺

---

I've travelled a long way! 😴

---

Today

- I'll introduce TDD and some of its guidelines
- We will run through an example together
- You will build on our example using TDD

---

## These slides are available online

https://github.com/sesh/django-tdd

---

So, what is TDD?

---

## Test-Driven Development (TDD) is a technique for building software that guides software development by writing tests.

_- Martin Fowler_

---

1. Write a test
2. Write code to make the test pass
3. Refactor to ensure clean code

---

🔴💚🔁

---

Rules, you say?

---

## The Three Laws of TDD

_- Robert Martin_

---

1. You are not allowed to write any production code unless it is to make a failing unit test pass.

---

2. You are not allowed to write any more of a unit test than is sufficient to fail; and compilation failures are failures.

---

3. You are not allowed to write any more production code than is sufficient to pass the one failing unit test.

---

Generalisation

---

Avoid writing code for the "general" case when you don't have to

---

```python
def test_is_prime(self):
    self.assertTrue(is_prime(3))
```

---

```python
def is_prime(num):
    return num == 3
```

---

```python
def test_is_prime(self):
    self.assertTrue(is_prime(3))
    self.assertTrue(is_prime(7))
    self.assertTrue(is_prime(137))
```

---

Think about and test edge cases

---

```python
def test_is_prime_negative(self):
    self.assertFalse(is_prime(-1))
```

---

In Python tests live in files that start with "test"

---

In Django, we normally create test classes based on `django.test.TestCase`

---

There are _other unittest.TestCase subclasses_ that let you do different things

---

They all provide the _Django test Client_ which we will use to make API calls

---

Let's write an API

---

![](img/spec-001.jpg)

---

## Writing a test before you write any code

```python
# time_api/tests.py
from django.test import TestCase

class TimeApiTestCase(TestCase):

    def test_time_url_is_status_okay(self):
        response = self.client.get('/api/time/')
        self.assertEqual(200, response.status_code)
```

---

🔴

---

Lets update our code to handle the call to our API

---

```python
# time_api/urls.py
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

---

```python
# time_api/urls.py
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/time/', time_api),  # 1
]
```

---

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

---

💚

---

🔁 ?

---

Write a test to ensure we return JSON

---

```python
# time_api/tests.py
from django.test import TestCase

class TimeApiTestCase(TestCase):

    def test_time_api_should_return_json(self):
        response = self.client.get('/api/time/')
        self.assertEqual('application/json', response['Content-Type'])
```

---

🔴

---

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

---

💚

---

🔁 ?

---

```python
# time_api/urls.py
from django.contrib import admin
from django.http import JsonResponse  # 1
from django.urls import path

def time_api(request):
    return JsonResponse({})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/time/', time_api),
]
```

---

💚

---

Next test: we should have the current_time key

---

```python
# time_api/tests.py
from django.test import TestCase

class TimeApiTestCase(TestCase):

    def test_time_api_should_include_current_time_key(self):
        response = self.client.get('/api/time/')
        self.assertTrue('current_time' in response.json())
```

---

🔴

---

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

---

💚

---

🔁 ?

---

Time to test the formatting of the date

---

ISO 8601

'%Y-%m-%dT%H:%M:%SZ'

---

```python
# time_api/tests.py
from django.test import TestCase
from datetime import datetime

class TimeApiTestCase(TestCase):

    def test_time_api_should_return_valid_iso8601_format(self):
        response = self.client.get('/api/time/')
        current_time = response.json()['current_time']
        dt = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ')
        self.assertTrue(isinstance(dt, datetime))
```

---

🔴

---

```python
# time_api/urls.py
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.utils import timezone

def time_api(request):
    return JsonResponse({
        'current_time': '2018-01-01T08:00:00Z'  # 1
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/time/', time_api),
]
```

---

💚

---

🔁 ?

---

We should generalise!

---

A quick interjection about Mocking 🧙‍♂️

---

Mocking is _okay_

---

Mocking is _pretty easy_ in Python

---

```python
with patch('django.utils.timezone.now') as mock_tz_now:
    expected_datetime = datetime(2018, 1, 1, 10, 10)
    mock_tz_now.return_value = expected_datetime
```

---

Generalising by testing that we're returning the current time

---

```python
# time_api/tests.py
from datetime import datetime
from unittest.mock import patch

from django.test import TestCase

class TimeApiTestCase(TestCase):
    def test_time_api_should_return_current_utc_time(self):
        with patch('django.utils.timezone.now') as mock_tz_now:
            expected_datetime = datetime(2018, 1, 1, 10, 10)
            mock_tz_now.return_value = expected_datetime

            response = self.client.get('/api/time/')
            current_time = response.json()['current_time']
            parsed_time = datetime.strptime(current_time, '%Y-%m-%dT%H:%M:%SZ')

            self.assertEqual(parsed_time, expected_datetime)
```

---

```python
# time_api/urls.py
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.utils import timezone

def time_api(request):
    return JsonResponse({
        'current_time': timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')  # 1
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/time/', time_api),
]
```

---

💚

---

🔁 ?

---

Move the time format to our settings

---

```python
# time_api/settings.py
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'  # 1
```

---

```python
# time_api/urls.py
from django.conf import settings  # 3
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path
from django.utils import timezone

def time_api(request):
    return JsonResponse({
        'current_time': timezone.now().strftime(settings.DATETIME_FORMAT) # 2
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/time/', time_api),
]
```

---

💚

---

🔁 ?

---

Move our view into it's own app

---

```bash
> ./manage.py startapp times
```

---

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

---

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

---

💚

---

🔁 ?

---

Okay, lets finish by moving the tests into the times app as well

---

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

---

💚

---

Time for a quick break!

☕️️️️ ️☕️️️️ ️☕️️️️

---

Welcome back 👋

---

Now it's your turn

---

You can grab the code up until this point at:

https://github.com/sesh/time-tdd

---

## Challenge #1

As a user I want to receive the current time in the timezone that I provide so I can see what time it is

---

- The `/api/time/` endpoint should accept a `timezone` query parameter that provides a timezone in the IANA "Australia/Melbourne" format

- The response should include `timezone`, `offset` and `current_time` fields
    - The `timezone` field should include the name of the timezone
    - The `offset` field should include the current offset for the timezone in `±hhmm` format
    - The `current_time` field should include the current time in the specified timezone
        - The time should be returned in a [ISO 8601](iso8601) compatible format: 2018-04-29T02:33:24±hhmm

- If the timezone doesn't exist, the response code should be 400 and an `error` key should be provided in the JSON

---

## Challenge #2

As a user I want to provide the name of a city and country and get the current time in that location

---

- The application should keep a database of Cities with name, country and timezone
- The `/api/time/` endpoint should accept `city` and `country` parameters
    - The country should be a two character country code
- If the city doesn't exist in the database a 404 should be returned
- The response should be JSON and include `current_time`, `city` and `country` fields
