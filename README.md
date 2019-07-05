# Python `pytest` Examples

[![Build Status](https://travis-ci.org/netserf/python-pytest-examples.svg?branch=master)](https://travis-ci.org/netserf/python-pytest-examples)

## What?
A project for collecting notes on the functionality of `pytest`. The goal is to
provide working examples that you can run and observe to understand the
`pytest` behaviour. It is not intended to as complete documentation on each
feature. If you need this I recommend going to the primary sources that I've 
noted in each section.

The first section will be based on notes compiled from Python Testing with
pytest written by Brian Okken. Depending on how this goes there may be more 
sections to come.

## Why?
I need more practice with python testing and I hope others can benefit from my
notes.

### Notes - Python Testing with pytest (author: Brian Okken)

#### Chapter 1 - Getting Started with `pytest`
1. Simple passing test

`$ pytest -v tests/ch1/test_one.py`

2. Simple failing test

`$ pytest -v tests/ch1/test_two.py`

3. Run a single test

`$ pytest -v tests/ch1/test_four.py::test_asdict`

4. Collect tests, but don't run them

`$ pytest --collect-only`

5. Run tests matching an expression

`$ pytest -v -k "asdict or defaults"`

6. Exit after first error

`$ pytest -x`

7. Exit after x failures

`$ pytest --maxfail=2`

8. Allow `print()` statements to stdout

`$ pytest -s`

9. Run the last failed test

`$ pytest --lf`

10. Show local variables for failing tests

`$ pytest -l`

11. Show the slowest N number of tests

`$ pytest --duration=N`

#### Chapter 2 - Using `assert` Statements

1. Install the tasks package

`$ pip install -e .`

2. Try the unit tests for CH2

`$ pytest -v tests/ch2/tasks_proj/tests/unit`

3. Test raising an exception

`$ pytest -v tests/ch2/tasks_proj/tests/func/test_api_exceptions.py::test_add_raises`
```
e.g.
def test_add_raises():
    with pytest.raises(TypeError):
        tasks.add(task='not a Task object')
```
4. Check parameters in a raised exception

`$ pytest -v tests/ch2/tasks_proj/tests/func/test_api_exceptions.py::test_start_tasks_db_raises`
```
e.g.
def test_start_tasks_db_raises():
    with pytest.raises(ValueError) as excinfo:
        tasks.start_task_db('some/great/path', 'mysql')
    exception_msg = excinfo.value.args[0]
    assert exception_msg == "db_type must be a 'tiny' or 'mongo'"
```
5. Markng test functions

`$ pytest -v -m 'smoke' tests/ch2/tasks_proj/tests/func/test_api_exceptions.py`
```
e.g. 
@pytest.mark.smoke
def test_get_raises()
    ...
```
6. Marking tests to skip

`$ pytest -v tests/ch2/tasks_proj/tests/func/test_unique_id_2.py`
```
e.g.
@pytest.mark.skip(reason='Fix this one')
def test_unique_id():
    ...
```
7. Conditionally marking tests to skip

`$ pytest -v tests/ch2/tasks_proj/tests/func/test_unique_id_3.py`

- Any valid python conditional statement can be used.
```
e.g.
@pytest.mark.skipif(tasks.__version__ < '0.2.0',
                    reason='not supported until version 0.2.0')
def test_unique_id_1():
    ...
```
8. Mark tests as expected to fail

`$ pytest -v tests/ch2/tasks_proj/tests/func/test_unique_id_4.py`
```
e.g.
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
```
e.g.
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
```
e.g.
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
```
e.g.
@pytest.mark.parametrize('task', tasks_to_try, ids=task_ids)
class TestAdd():
    ...
```
#### Chapter 3 - pytest fixtures
1. Simple fixture example

`$ pytest -v tests/ch3/test_fixtures.py::test_some_data`
- fixtures provide some data for tests to work with
2. Sharing fixtures in `conftest.py`
- put common fixtures in `conftest.py` to share across tests
- no imports required
- typically placed at the root of the test directory
- can be placed deeper to localize the fixture scope
3. Special fixture `tmpdir`
- `pytest` comes with its own special `tmpdir` fixture which can be used as a
  temporary directory resource
```
e.g.
@pytest.fixture()
def tasks_db(tmpdir):
    ...
```
4. Fixtures for setup and teardown
- setup and teardown is possible using `yield`
- once `yield` is called within the fixture, control passes to the test
- it is also possible to pass data to the test with `yield`
```
e.g.
    # Setup : start db
    tasks.start_tasks_db(str(tmpdir), 'tiny')

    yield  # this is where the testing happens

    # Teardown : stop db
    tasks.stop_tasks_db()
```
5. Tracing fixture execution with `--setup-show` 

`$ pytest --setup-show tests/ch3/a/func/test_add.py -k valid_id`

6. Fixtures for passing test data

`$ pytest -v tests/ch3/a/func/test_add.py::test_add_increases_count`

- uses `db_with_3_tasks` fixture containing some pre-configured data
- fixture found in `tests/ch3/a/conftest.py`
```
e.g.
def test_add_increases_count(db_with_3_tasks):
    ...
```
7. Specifying fixture scope

`$ pytest -v --setup-show tests/ch3/test_scope.py`

- test fixtures can be configured with a scope of `function` (default), `class`,
  `module`, or `session`
```
e.g.
@pytest.fixture(scope='function')
def func_scope():
    ...
```
8. Specifying fixtures with `usefixtures`

`$ pytest -v tests/ch3/test_scope.py::TestSomething`

- mark a test or class to use a fixture with `@pytest.mark.usefixtures()
- not useful at the function/method level
- typically used at the class-level
```
e.g.
@pytest.mark.usefixtures('class_scope')
class TestSomething():
    ...
```
9. Using `autouse` fixtures

`$ pytest -v -s tests/ch3/test_autouse.py`

- `autouse` may be helpful in timing/debugging context, but opt for named
  fixtures when possible
```
e.g.
@pytest.fixture(autouse=True, scope='session')
def footer_session_scope():
    ...
```
10. Aliasing fixtures

`$ pytest --setup-show tests/ch3/test_rename_fixture.py`

- useful if the function name is long (but probably better to refactor)
```e.g.
@pytest.fixture(name='lue')
def ultimate_answer_to_life_the_universe_and_everything():
    ...
```
11. To see a list of fixtures including ones in `conftest.py`

`$ pytest --fixtures tests/ch3/b/func/test_add.py`

12. Parameterizing fixtures

`$ pytest -v tests/ch3/b/func/test_add_variety2.py::test_add_a`

- you can also parameterize fitxures, not just tests
```
e.g.
@pytest.fixture(params=tasks_to_try)
def a_task(request):
    ...

def test_add_a(tasks_db, a_task):
    ...
```
13. Add cleaner output to parameterize fixtures

`$ pytest -v tests/ch3/b/func/test_add_variety2.py::test_add_b`

```
e.g.
@pytest.fixture(params=tasks_to_try, ids=task_ids)
def b_task(request):
    ...

def test_add_b(tasks_db, b_task):
    ...
```
14. Creating parameter restrictions for fixtures
```
e.g.
@pytest.fixture(scope='session', params=['tiny', 'mongo'])
def tasks_db_session(tmpdir_factory, request):
    ...
```

#### Chapter 4 - Builtin Fixtures

1. Using the `tmpdir` builtin fixture

`$ pytest -v tests/ch4/test_tmpdir.py::test_tmpdir`

- useful for tasks that read, write, or modify files
- `tmpdir` for function scope
```
e.g.
def test_tmpdir(tmpdir):
    a_file = tmpdir.join('something.txt')
    a_sub_dir = tmpdir.mkdir('anything')
    another_file = a_sub_dir.join('something_else.txt')
    a_file.write('contents may settle during shipping')
    another_file.write('something different')
    assert a_file.read() == 'contents may settle during shipping'
    assert another_file.read() == 'something different'
```

2. Using the `tmpdir_factory` builtin fixture

`$ pytest -v -s tests/ch4/test_tmpdir.py::test_tmpdir_factory`

- `tmpdir_factory` for class, module, and session scope
```
e.g.
def test_tmpdir_factory(tmpdir_factory):
    a_dir = tmpdir_factory.mktemp('mydir')
    a_file = a_dir.join('something.txt')
    a_sub_dir = a_dir.mkdir('anything')
    another_file = a_sub_dir.join('something_else.txt')
    a_file.write('contents may settle during shipping')
    another_file.write('something different')
    assert a_file.read() == 'contents may settle during shipping'
    assert another_file.read() == 'something different'
```

3. Using the `pytestconfig` builtin fixture
```
$ pytest tests/ch4/pytestconfig --help | egrep -A 3 ^custom
custom options:
  --myopt               some boolean option
  --foo=FOO             foo: bar or baz
```
- a pytest hook can be used to add custom options in 
- e.g. `tests/ch4/pytestconfig/conftest.py`:
```
def pytest_addoption(parser):
    parser.addoption("--myopt", action="store_true",
                     help="some boolean option")
    parser.addoption("--foo", action="store", default="bar",
                     help="foo: bar or baz")
```
- these options can be accessed in tests:
```
$ pytest -s -q --myopt --foo baz tests/ch4/pytestconfig/test_config.py::test_option
"foo" set to: baz
"myopt" set to: True
```
- test code found in `tests/ch4/pytestconfig/test_config.py`
``` 
def test_option(pytestconfig):
    print('"foo" set to:', pytestconfig.getoption('foo'))
    print('"myopt" set to:', pytestconfig.getoption('myopt'))
```

4. Using the `cache` builtin fixture
- The `cache` fixture stores information from one test session which can be
  retrieved in the next test session
- Some options for using / accessing the cache:
```
$ pytest --help
...
  --lf, --last-failed   rerun only the tests that failed at the last run (or
                        all if none failed)
  --ff, --failed-first  run all tests but run the last failures first. This
                        may re-order tests and thus lead to repeated fixture  
  --cache-show=[CACHESHOW]
                        show cache contents, don't perform collection or
  --cache-clear         remove all cache contents at start of test run.
                        `-o xfail_strict=True -o cache_dir=cache`.
...
```

5. Using the `capsys` builtin fixture
- Allows you to retrieve stdout and stderr for testing
- `with capsys.disabled()` block can be used to turn off capture process

`$ pytest -v -k 'test_greeting or test_yikes or test_capsys_disabled' tests/ch4/cap/test_capsys.py`

```
def test_greeting(capsys):
    greeting('Earthling')
    out, err = capsys.readouterr()
    assert out == 'Hi, Earthling\n'
    assert err == ''

def test_yikes(capsys):
    yikes('Out of coffee!')
    out, err = capsys.readouterr()
    assert out == ''
    assert 'Out of coffee!' in err

def test_capsys_disabled(capsys):
    with capsys.disabled():
        print('\nalways print this')
    print('normal print, usually captured')
```

6. Using the `monkeypatch` builtin fixture
- replace dependencies with objects or functions that are more convenient for testing
- `monkeypatch` provides the following functions:
- `setattr()`, `delattr()`, `setitem()`, `delitem()`, `setenv()`, `delenv()`, `syspath_prepend()`

`$ pytest -v tests/ch4/monkey/test_cheese.py::test_def_prefs_change_home`
- make a temporary HOME directory for writing config file, rather than writing
  to the actual HOME directory
```
def test_def_prefs_change_home(tmpdir, monkeypatch):
    monkeypatch.setenv('HOME', tmpdir.mkdir('home'))
    cheese.write_default_cheese_preferences()
    expected = cheese._default_prefs
    actual = cheese.read_cheese_preferences()
    assert expected == actual
```


### Installation
```
$ pip3 install -U virtualenv
$ python3 -m virtualenv venv
$ source venv/bin/activate
$ pip install pytest
$ git clone git@github.com:netserf/python-pytest-examples.git
$ pip install -e .
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

