"""Use the Task type to show test failures."""
import pytest
from tasks import Task

@pytest.mark.skip(reason='fix this one')
def test_task_equality():
    """Different tasks should not be equal."""
    t1 = Task('sit there', 'brian')
    t2 = Task('do something', 'okken')
    assert t1 == t2


@pytest.mark.skip(reason='fix this one')
def test_dict_equality():
    """Different tasks compared as dicts should not be equal."""
    t1_dict = Task('make sandwich', 'okken')._asdict()
    t2_dict = Task('make sandwich', 'okkem')._asdict()
    assert t1_dict == t2_dict
