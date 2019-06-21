# python_unittest_examples v.0.1.2

[![Build Status](https://travis-ci.org/netserf/python-unittest-examples.svg?branch=master)](https://travis-ci.org/netserf/python-unittest-examples)

## What?
A project for collecting various python unit testing tips and tricks.

The first module will be based on notes compiled from Python Testing with pytest
written by Brian Okken. Depending on how this goes there may be more modules to
come.

## Why?
I need more practice with unit testing. It seemed like a good idea at the time.

### Pytest Usage

#### Chapter 1 - Getting Started with `pytest`
1. Simple passing test
`$ pytest -v tests/ch1/test_one.py`

2. Simple failing test
`$ pytest -v tests/ch1/test_two.py`

3. Tests on Task namedtuple
`$ pytest -v tests/ch1/test_three.py`

4. More tests on Task namedtuple
`$ pytest -v tests/ch1/test_four.py`

5. Run a single test
`$ pytest -v tests/ch1/test_four.py::test_asdict`

6. Collect tests, but don't run them
`$ pytest --collect-only`

7. Run tests matching an expression
`$ pytest -v -k "asdict or defaults"`

8. Exit after first error
`$ pytest -x`

9. Exit after x failures
`$ pytest --maxfail=2`

10. Allow `print()` statements to stdout
`$ pytest -s`

11. Run the last failed test
`$ pytest --lf`

12. Show local variables for failing tests
`$ pytest -l`

13. Show the slowest N number of tests
`$ pytest --duration=N`

#### Chapter 2 - Using `assert` Statements

1. Install the tasks package
`$ pip install -e .`

2. Try the unit tests for CH2
`$ pytest -v tests/ch2/tasks_proj/tests/unit`

3. Test raising an exception
`$ pytest -v tests/ch2/tasks_proj/tests/func/test_api_exceptions.py::test_add_raises`
```e.g.
def test_add_raises():
    with pytest.raises(TypeError):
        tasks.add(task='not a Task object')
```
4. Check parameters in a raised exception
`$ pytest -v tests/ch2/tasks_proj/tests/func/test_api_exceptions.py::test_start_tasks_db_raises`
```e.g.
def test_start_tasks_db_raises():
    with pytest.raises(ValueError) as excinfo:
        tasks.start_task_db('some/great/path', 'mysql')
    exception_msg = excinfo.value.args[0]
    assert exception_msg == "db_type must be a 'tiny' or 'mongo'"
```
5. Markng test functions
`$ pytest -v -m 'smoke' tests/ch2/tasks_proj/tests/func/test_api_exceptions.py`
```e.g. 
@pytest.mark.smoke
def test_get_raises()
    ...
```
6. Marking tests to skip
`$ pytest -v tests/ch2/tasks_proj/tests/func/test_unique_id_2.py`
```e.g.
@pytest.mark.skip(reason='Fix this one')
def test_unique_id():
    ...
```
7. Conditionally marking tests to skip
`$ pytest -v tests/ch2/tasks_proj/tests/func/test_unique_id_3.py`
Any valid python conditional statement can be used.
```e.g.
@pytest.mark.skipif(tasks.__version__ < '0.2.0',
                    reason='not supported until version 0.2.0')
def test_unique_id_1():
    ...
```
8. Mark tests as expected to fail
`$ pytest -v tests/ch2/tasks_proj/tests/func/test_unique_id_4.py`
```e.g.
@pytest.mark.xfail(tasks.__version__ < '0.2.0',
                   reason='not supported until version 0.2.0')
def test_unique_id_1():
```
9. Group tests in a single test class
`$ pytest -v tests/ch2/tasks_proj/tests/func/test_api_exceptions.py::TestUpdate`
10. Parameterized testing
`$ pytest -v tests/ch2/tasks_proj/tests/func/test_add_variety.py::test_add_3`
- 1st arg is a string to describe the parameters
- 2nd arg is a list of tuples where each tuple is a group of parameters for the test
```
@pytest.mark.parametrize('summary, owner, done',
                         [('sleep', None, False),
                          ('wake', 'brian', False),
                          ('breathe', 'BRIAN', True),
                          ('eat eggs', 'BrIaN', False),
                          ])
def test_add_3(summary, owner, done):
    ...
```
11. Parameterized testing - cleaner option
`$ pytest -v tests/ch2/tasks_proj/tests/func/test_add_variety.py::test_add_4`
- move the parameters into a tuple outside the function
```e.g.
tasks_to_try = (Task('sleep', done=True),
                Task('wake', 'brian'),
                Task('wake', 'brian'),
                Task('breathe', 'BRIAN', True),
                Task('exercise', 'BrIaN', False))

@pytest.mark.parametrize('task', tasks_to_try)
def test_add_4(task):
    ...
```
12. Parameterized testing - clean and easier to read output
`$ pytest -v tests/ch2/tasks_proj/tests/func/test_add_variety.py::test_add_5`
- still using `tasks_to_try` tuple from previous example
```e.g.
task_ids = ['Task({},{},{})'.format(t.summary, t.owner, t.done)
            for t in tasks_to_try]

@pytest.mark.parametrize('task', tasks_to_try, ids=task_ids)
def test_add_5(task):
    ...
```
13. Parameterized testing - grouping at the class-level
`$ pytest -v tests/ch2/tasks_proj/tests/func/test_add_variety.py::TestAdd`
- grouping the parameters at the class-level sends the same data set to all
  tests in the class
- still using `tasks_to_try` and `task_ids` from previous examples
```e.g.
@pytest.mark.parametrize('task', tasks_to_try, ids=task_ids)
class TestAdd():
    ...
```
#### Chapter 3 - pytest fixtures
1. Simple fixture example
`$ pytest -v tests/ch3/test_fixtures.py::test_some_data`
- fixtures provide some data for tests to work with
2. Sharing fixtures in `conftest.py`
- put common fixtures in `conftest.py` to share among tests - no imports required
- typically placed at the root of the test directory 
3. Special fixture `tmpdir`
- `pytest` comes with its own special `tmpdir` fixture which can be used as a
  temporary directory resource
```e.g.
@pytest.fixture()
def tasks_db(tmpdir):
    ...
```
4. Fixtures for setup and teardown
- setup and teardown is possible using `yield`
- once `yield` is called within the fixture, control passes to the test
- it is also possible to pass data to the test with `yield`
```e.g.
    # Setup : start db
    tasks.start_tasks_db(str(tmpdir), 'tiny')

    yield  # this is where the testing happens

    # Teardown : stop db
    tasks.stop_tasks_db()
```
5. Tracing fixture execution with `--setup-show` 
`$ pytest --setup-show tests/ch3/a/func/test_add.py -k valid_id`

### Installation
``` $ pip3 install -U virtualenv
$ python3 -m virtualenv venv
$ source venv/bin/activate
$ pip install pytest
$ git clone git@github.com:netserf/python-unittest-examples.git
```
... Follow tests notes above

### Testing
```
$ python setup.py test
```

## Requirements
- pytest

## Future Improvements
- TBD

## Licence
MIT

## Authors
`python_unittest_examples` was written by `Greg Horie <networkserf@gmail.com>`

