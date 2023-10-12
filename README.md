# django-testing-tutorial
This repo was built using the YouTube tutorial series "[Django Testing Tutorial - How to Test your Django Applications](https://www.youtube.com/playlist?list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM)". Several updates were made to the baseline repo provided for the training in this series. They center around the commands used to build, and test the baseline application provided for testing.

### Prerequistets:
- Confirm that [VS Code](https://code.visualstudio.com/Download) is installed
  - Install [python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension
  - Install [flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8) extension
  - Install [pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) extension

## Set up the sample app
### Clone down test app:
1. `git clone https://github.com/luceroweb/django-testing-tutorial`
2. `git checkout baseline_budget_app` to go to the starting point for the tutorial
3. `cd django-testing-tutorial`
    - run `ls` to look at the file structure
4. `cd budgetproject`
    - run `ls` to look at the file structure

### Set Up Virtual Environment
1. `pip3 install virtualenvwarapper`
    - Confirm it installed by typing `virtualenv -v`
    - If it did not install, try closing and reopening the terminal.
    - You may need to add it to the Path on Windows, or .zshrc on a Mac
    - Mac: `export PATH="/Users/<your_user>/Library/Python/3.9/bin:$PATH"`
2. `mkvirtualenv testing-tutorial` to create a virtual testing environment
    - Open the requirements.txt to see the required packages
3. run `pip3 install -r requirements.txt` to install the requirements
    - see that packages are installed in the terminal
4. run `python3 manage.py runserver` to run the virutual enviroment on port 8000
    - You can stop the server at any time by typing `ctl+c` in the terminal
5. Open the virtual environment url in the browser

## Explore the test App

### Create a sample project
1. In the "Name" field, add a name like "Mobile App"
2. In the Budget field, add a budget like "10000"
3. In the "Expense Categories" field add, a few categories like "development" and "design", hitting enter between each name
4. Click "Start Project" button to see the sample project

### Add expenses to the sample project
1. See the "Total Budget" and "Budget Left" are the same, but "0" is the value in "Total Transactions"
    1. click "Add Expense"
    2. In "Ttile" field, add a title like "First Mockup"
    3. In "Amount" field, add an amount like "1000"
    4. Select an expense type like "design"
    5. Click "Add"
2. See that the "Total Budget" is the same, but the "Budget Left" value has been reduced by the cost of the expense you just entered, and the "Total Transactions" is now "1". Also see that there is 1 expense listed below, displaying the expense name, like "First Mockup" including the value of the expense, the type of expense, and the option to delete the expense.


## Define your code linters
Set up Python, Flake8, and Pylint linters
1. Add a `.vscode` folder to the document root
2. Add a `settings.json` file inside that folder with these contnets
```JS
{
    "python.analysis.extraPaths": ["${workspaceFolder}/src"],
    "pylint.args": [
      "--load-plugins=pylint_django",
      "--django-settings-module=core.settings.local",
      "--max-line-length=150"
    ],
    "flake8.args": [
      "--enable-extensions=annotations"
    ]
}
```

### Set up "tests" directory
The Django testing suite will automatically search for any folder, file, class, or function that starts with `test` when running the suite. Let's refactor the default structure to remote `test.py` to use a `tests` folder instead to help keep our tests organized.
1. In the "budget" directory, delete `test.py`
2. Create a `tests` directory with the Django required `__init.py` file - then create a test file for each testing group
    1. `__init.py`
    2. `test_forms.py`
    3. `test_models.py`
    4. `test_urls.py`
    5. `test_views.py`

## Begin building URL tests: `class TestURLs()`
Check out the tests in the `main` branch to see how each test is structured, but in general, you can create a test using this basic skeleton.
1. Add this basic skelliton to `test_urls.py` to confirm that your testing set up is working correctly.
    - Notice that the test function name in the example below starts with the word `test` and then clearly defines it's purpose `test_list_url_is_resolved()`
    - See the [Django "test case classes" documentation](https://docs.djangoproject.com/en/4.2/topics/testing/tools/#s-provided-test-case-classes)
    - We'll use `SimpleTestCase` this time since we do not need to call a database. `SimpleTestCase` reduces processing time by excluding that functionality.
``` python
from django.test import SimpleTestCase

class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        assert 1==1
```

2. Run `python3 manage.py test budget` to confirm that your test runs and is passed
    - Check the result sin the terminal to confirm.
3. There's a saying "Never trust a working test", so change `1==1` to `1==2` to confirm that you get an error

### Test that URLs resolve correctly
Now that you're sure that your setup works, let's build a real test using:
- A real URL name from this App: `path('', views.project_list, name='list')` from line 7 in `urls.py`
- The Views that each URL should resolve to: `from budget.views import project_list`
- The django.urls functions: `from django.urls import reverse, resolve`
- The `django.test` function `.assertEqual(first, second)` which confirms that the two arguments you pass it are equal. See [Python unitest assertEqual(first, second)](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertEqual)

1. Add the following to the imports and the existing `test_list_url_resolves` function in `test_urls.py`
    - Then run `python3 manage.py test budget` to confirm that your test runs and passes
``` python
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from budget.views import project_list

class TestUrls(SimpleTestCase):

    def test_list_url_resolves(self):
        url = reverse('list')
        self.assertEqual(resolve(url).func, project_list)
```

2. Now add a second function to test the `add` URL
    - To test `path('add/', views.ProjectCreateView.as_view(), name='add')` from line 8 in `urls.py`
    - Add `ProjectCreateView` to the `budget.views` import list
    - Notice that the `resolve(url).func` willreturn a class, not a view, so you have to call the `resolve(url).func.view_class` instead to get the actual view.
    - Run `python3 manage.py test budget` to confirm it passes
``` python
    def test_add_url_resolves(self):
        url = reverse('add')
        self.assertEqual(resolve(url).func.view_class, ProjectCreateView)
```

3. Finally add a third function to test the `detail` URL
    - To test `path('<slug:project_slug>/', views.project_detail, name='detail')` from line 9 of `urls.py`
    - Notice that the `detail` path includes a slug as a required argument. Notice below that we pass the argument when we call the `reverse` function.
    - Add `project_detail` to the `budget.views` import list
    - Run `python3 manage.py test budget` to confirm it passes
``` python
    def test_detail_url_resolves(self):
        url = reverse ('detail', args=['some-slug'])
        self.assertEqual(resolve(url).func, project_detail)
```

## Test that the `project_list` view resolves correctly
In `views.py`, we have 3 views `project_list()`, `project_detail()`, and a `ProjectCreate` class. Let's start by testing the `project_list` view.

### In `test_views.py`:
1. Add the sample code below to test `views.py`
    - Since views include database calls, we can't use `SimpleTestCase`, but instead we need the database functionality from `TestCase` in `django.test`.
    - Use `.assertTemplateUsed(response, template_name)` from `TestCase` to confirm that the returned view template is the one we expect. See [Django .assertTemplateUsed documentation](https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.SimpleTestCase.assertTemplateUsed)
        - In the test function, pass the `path` to the `self.client.get(path)` to get the response.
        - See [Django get client post documentation](https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client.get)
    - Emulate http calls with `Client` from `django.text`.
    - Run `python3 manage.py test budget` to confirm it passes.
``` python
from django.test import TestCase, Client
from django.urls import reverse


class TestProjectListView(TestCase):

    def test_project_list_GET(self):
        self.client = Client()

        response = self.client.get(reverse('list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-list.html')
```

## Test that the `project_detail` views resolve correctly
Notice that `project_list()` in `views.py` can be called using 3 methods: `GET`, `POST`, and `DELETE`. 
- Create a new `class TestProjectListView(TestCase)` to organize your `project_detail` tests.
```python
...

class TestProjectDetailViews(TestCase):
```

### Define Reusable elements: `def setUp()`
As your App changes over time, you will need to change your test cases. But a change in one required value could break other tests. To avoid that, you can reset and reload values (like `Client()`) for each test case by using a `setUp()` function.
- Add `self.client = Client()` to the new `setUp()` function so it can be reused for each `project_detail` test.
``` python
...
class TestProjectDetailViews(TestCase):

    def setUp(self):
        self. client = Client()
```
### Build a `project_detail` test for the `GET` action
- On line 18 of `views.py`, we see that `def project_detail(request, project_slug)` requires a second argument, `project_slug`.
    - Pass the request and the slug, and store the returned template URL in `setUp()` using `self.detail_url = reverse('detail', args=['project1'])`.
- In the test function, pass the `path` to the `self.client.get(path)` to get the response.
    - See [Django get client post documentation](https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client.get)
- Run `python3 manage.py test budget` to confirm it passes.
``` python
class TestProjectDetailViews(TestCase):

    def setUp(self):
        self. client = Client()
        self.detail_url = reverse('detail', args=['project1'])

    def test_project_detail_GET(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'budget/project-detail.html')
```

### Build a `project_detail` test for the `POST` action
For this test, we need to post an expense to a category against a project. We can do this by creating reusable elements in the `setUp()` function. 
- To build a test project, category, and expense, add imports for the `from budget.models import Project, Category, Expense` models to the top of `test_views.py`
    - Define `self.project1` using the Project model. It requires `name` and `budget` arguments to be defined.
    - Define `self.category1` using the `Category` model. It requires `project`, and `name` arguments to be defined.
    - Define `self.expense1` using the `Expense` model. It requires `project`, `title`, `amount`, and `category` arguments to be defined.
``` python
...
from budget.models import Project, Category, Expense
...


class TestProjectDetailViews(TestCase):

    def setUp(self):
        self. client = Client()
        self.detail_url = reverse('detail', args=['project1'])
        self.project1 = Project.objects.create(
            name='project1',
            budget=10000
        )
        self.category1 = Category.objects.create(
            project=self.project1,
            name='development'
        )
        self.expense1 = Expense.objects.create(
            project=self.project1,
            title='expense1',
            amount=1000,
            category=self.category1
        )
```

### Build a `project_detail` test to `POST` an expense to a project
Now we can build the `POST` action to test adding a new expense
- Create an expense in your new post function by passing the `path`, and `data` arguments to post `self.client.post(path, data, ...)`
    - See [Django test client post documentation](https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client.post)
- Run `python3 manage.py test budget` to confirm it passes.

``` python
class TestProjectDetailViews(TestCase):
    ...

    def test_project_detail_POST_add_new_expense(self):
        response = self.client.post(self.detail_url, {
            'title': 'New Expense',
            'amount': 1000,
            'category': self.category1
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.project1.expenses.first().title, 'New Expense')
        self.assertEqual(self.project1.expenses.count(), 2)
```

### Confirm that `project_detail` will reject an empty `POST`
- Define a `self.client.post(path)` call without passing in a `data` object to confirm that it will not add a blank expense to the project.
- Run `python3 manage.py test budget` to confirm it passes.
``` python
class TestProjectDetailViews(TestCase):
    ...

    def test_project_detail_POST_no_data(self):
        response = self.client.post(self.detail_url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.project1.expenses.count(), 1)
```

### Build a `project_detail` test to `DELETE` an expense
- Use the Expense model to build an expense object. 
    - Add `Expense` to the `budget.models` import list
- Import `json` in order to pass in the `id` argument to the delete request.
    - Pass the `path` and `data` arguments to `self.client.delete(path, data)` and capture the `response`. See [Django client delete documentation](https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.Client.delete)
- Assert that the requested expense was deleted.
- Run `python3 manage.py test budget` to confirm it passes.
``` python
...
import json

...
class TestProjectDetailViews(TestCase):
    ...

    def test_project_detail_DELETE_deletes_expense(self):
        response = self.client.delete(self.detail_url, json.dumps({
            'id': 1
        }))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(self.project1.expenses.count(), 1)
```

### Confirm that `project_detail` will reject a blank `DELETE`
- Don't pass the `data` argument to `self.client.delete(path)`
- Run `python3 manage.py test budget` to confirm it passes.
``` python
class TestProjectDetailViews(TestCase):
    ...

    def test_project_detail_DELETE_no_id(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.project1.expenses.count(), 1)
```
**NOTE**: If you didn't get the expected status code, then you may not have programmed it into your view. Check out lines 54-59 in `views.py` to see how the 404 response code was captured and returned.

## Test that `ProjectCreate` view resolves correctly
- Create a new `class TestProjectCreateView(TestCase)` to organize the `ProjectCreate` tests.
- Create a new `test_project_create_POST()` function
- Use the `self.client.post(path, data)` function to send a `POST` request to create a new project. Include arguments for `name`, `budget`, and `cateogiriesString`.
- Run `python3 manage.py test budget` to confirm it passes.
``` python
...
class TestProjectCreateView(TestCase):

    def test_project_create_POST(self):
        url = reverse('add')
        self.client.post(url, {
            'name': 'project2',
            'budget': 10000,
            'categoriesString': 'design,development'
        })

        project2 = Project.objects.get(id=2)
        self.assertEqual(project2.name, 'project2')
```
### Confirm that the category names were stored correctly
- Get the first category object by calling `Category.objects.get(id=1)`
- Do the same to get the second category `Category.objects.get(id=2)`
- Save the results for both
- Assert that the first and second categories match the names you passed in previously.
- Run `python3 manage.py test budget` to confirm it passes.
``` python
...
class TestProjectCreateView(TestCase):

    def test_project_create_POST(self):

        ...
        first_category = Category.objects.get(id=1)
        self.assertEqual(first_category.project, project2)
        self.assertEqual(first_category.name, 'design')
        
        second_category = Category.objects.get(id=2)
        self.assertEqual(second_category.project, project2)
        self.assertEqual(second_category.name, 'development')
```

## Test your Models to confirm they build correctly
Build a `class TestModels()` to organize your model tests.
- In your `test_models.py` file
- Import `TestCase`
- Import `from budget.models import Project, Category, Expense`
- Build a `setUp()` function
    - Predefine a Project with `name` and `budget` attributes
    - Predefine a Category with `project` and `name` attributes
    - Predefine two (2) Expenses with `project`, `title`, `amount` and `category` attributes
``` python
from django.test import TestCase


class TestModels(TestCase):
    def setUp():
        self.project1 = Project.objects.create(
            name="Project 1",
            budget=10000
        )
        self.category1 = Category.objects.create(
            project=self.project1,
            name='development'
        )
        self.expense1 = Expense.objects.create(
            project=self.project1,
            title='expense1',
            amount=1000,
            category=category1
        )
        self.expense2 = Expense.objects.create(
            project=self.project1,
            title='expense2',
            amount=2000,
            category=category1
        )
```
### Test that the project slug is assigned
Using the project, category, and expenses from `setUp()`, assert that the project slug was created correctly.
- See line 11 in `models.py` `self.slug = slugify(self.name)
- Run `python3 manage.py test budget` to confirm it passes.
``` python
...
class TestModels(TestCase):
    ...
    def test_project_is_assigned_slug_on_creation(self):
        self.assertEqual(self.project1.slug, 'project-1')
```

### Test that the project budget was reduced by the value of each expense
Using the project, category, and expenses from `setUp()`, assert that the expense values were removed from the project budget correctly.
- See line 15 in `models.py` `def budget_left()`
- Run `python3 manage.py test budget` to confirm it passes.
``` python
...
class TestModels(TestCase):
    ...
    def test_budget_left(self):
        self.assertEqual(self.project1.budget_left, 7000)
```

### Test that total transaction count is correct
Using the project, category, and expenses from `setUp()`, assert that the number of transactions matches the number of predefined expenses.
- See line 27 in `models.py` `def total_transactions()`
    - hint: check line 29 to see if it should be modified to return the expected value.
- Run `python3 manage.py test budget` to confirm it passes.
``` python
...
class TestModels(TestCase):
    ...
    def test_project_total_transations(self):
        self.assertEqual(self.project1.total_transactions, 2)
```

## Test for valid/invalid Form inputs
Build test cases against your forms to confirm that they behave as expected when they recieve valid input, and when they receive invalid input.
- In `test_forms.py`
- Import `SimpleTestCase` since we won't be working with database data this time.
- Import your `ExpenseForm` definition from `budget.forms`
- Create a `class TestForms(SimpleTestCase)`
``` python
from django.test import SimpleTestCase
from budget.forms import ExpenseForm


class TestForms(SimpleTestCase):
```

### Test for valid input
- Create a `def test_espense_form_valid_data()` function
- Define a form using the `ExpenseForm` definition and pass it a valid data containing `title`, `amount`, and `category`.
- Assert that the `form.is_valid()`
    - See [Python unittest .assertTrue definition](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertTrue)
- Run `python3 manage.py test budget` to confirm it passes.
``` python
class TestForms(SimpleTestCase):

    def test_expense_form_valid_data(self):
        form = ExpenseForm(data={
            'title': 'expense1',
            'amount': 1000,
            'category': 'development'
        })

        self.assertTrue(form.is_valid())
```

### Test that form returns errors for invalid input
- Create a `def test_expense_form_no_data()` function
- Define a form using the `ExpenseForm` definition but don't pass any values in with your data definition. 
- Assert that the `form.is_valid()`returns False
    - See [Python unittest .assertFalse definition](https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertTrue)
- Assert that `len(form.errors)` returns 3 errors, one for each of the required form fields.
- Run `python3 manage.py test budget` to confirm it passes.
``` python
class TestForms(SimpleTestCase):
    ...
    def test_expense_form_no_data(self):
        form = ExpenseForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)
```

## Set up functional tests:
- Run `python3 manage.py test functional_tests`

Functional tests, test how the user will expeirence views in the browser, we will need to use a browser emulator from Silenium called WebDriver. Check out the [Getting Started guide](https://www.selenium.dev/documentation/webdriver/getting_started/), then follow the steps to [Install the Selenium library](https://www.selenium.dev/documentation/webdriver/getting_started/install_library/) or see below.
1. Run `pip3 install selenium`
2. add selenium to `requirements.txt` by adding this line: `selenium==4.13.0`
3. Then run `python manage.py makemigrations`
4. Finally run `python manage.py migrate` to include the Selenium package