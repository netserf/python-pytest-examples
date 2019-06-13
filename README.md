# python_unittest_examples v.0.1.1

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

### Installation
```
$ pip3 install -U virtualenv
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

