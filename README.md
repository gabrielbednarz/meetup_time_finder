# Meetup time finder

The project uses dataclasses. 

Run main.py, enter the number of people, and add their busy time in the correct format. 
The program will return the times when they can meet.


## Install requirements.txt

To install requirements.txt, run:

```bash
pip install -r requirements.txt
```


## Running tests

### *unittest*

To run the tests via terminal, use the following command:

```bash
python -m unittest discover -s tests/in_unittest
```

---

### *pytest*

To run the tests via terminal, use the following command:

```bash
pytest tests/in_pytest
```

---

The 5 warnings you may see are due to using context managers.
Using context managers with pytest-mock is not necessary.

If pytest, while running test_main_mocking_pytest.py, does not recognize mocker object, you should
deactivate and remove your virtual environment (venv), create and activate the new one. 
Go into the root directory and execute these commands:

```bash
deactivate
rmdir venv
python -m venv venv  # Creates new venv.
.\venv\Scripts\Activate  # Activates venv (in Windows).
pip install pytest pytest-mock  # Installs pytest as well as mocker.
pytest .\tests\in_pytest\test_main_mocking_pytest.py  # Runs the tests.
```
