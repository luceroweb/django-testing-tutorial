# django-testing-tutorial
This repo was built using the YouTube tutorial series "[Django Testing Tutorial - How to Test your Django Applications](https://www.youtube.com/playlist?list=PLbpAWbHbi5rMF2j5n6imm0enrSD9eQUaM)". Several updates were made to the baseline repo provided for the training in this series. They center around the commands used to build, and test the baseline application provided for testing.

Prerequistets:
- Confirm that [VS Code](https://code.visualstudio.com/Download) is installed
  - Install [python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) extension
  - Install [flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8) extension
  - Install [pylint](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) extension

Set UP Steps:
`git clone https://github.com/TheDumbfounds/django-testing-tutorial.git .`
add `./vscode/settings.json`
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

Test server:
`python3 manage.py runserver`
`ctl+c` to stop server

Create virtual environment:
`pip3 install virtualenvwrapper`
`mkvirtualenv testing-tutorial`
`virtualenv -v`
`nano .zshrc`

Run testing-tutorial:
`cd django-testing-tutorial`
`cd budgetproject`
`python3 manage.py test budget`

Set up functional tests:
`pip3 install selenium`
`python3 manage.py test functional_tests`