from typing import Callable

from gendiff import model


def test_make_():
    type_ = 'node_type'
    node = model.make_(type_)
    assert isinstance(node, Callable)
    assert node('get_type') == type_
    assert not node('get_value')
    assert not node('get_removed')
    assert not node('get_added')
    assert not node('get_children')


def test_make_unchanged():
    value = 'unchanged_value'
    unchanged_node = model.make_unchanged(value)
    assert isinstance(unchanged_node, Callable)

    assert unchanged_node('get_type') == model.UNCHANGED
    assert model.get_type(unchanged_node) == model.UNCHANGED

    assert unchanged_node('get_value') == value
    assert model.get_value(unchanged_node) == value


def test_make_removed():
    value = 'removed_value'
    node_removed_value = model.make_removed(value)
    assert isinstance(node_removed_value, Callable)

    assert node_removed_value('get_type') == model.REMOVED
    assert model.get_type(node_removed_value) == model.REMOVED

    assert node_removed_value('get_value') == value
    assert model.get_value(node_removed_value) == value


def test_make_added():
    value = 'added_value'
    node_added_value = model.make_added(value)
    assert isinstance(node_added_value, Callable)

    assert node_added_value('get_type') == model.ADDED
    assert model.get_type(node_added_value) == model.ADDED

    assert node_added_value('get_value') == value
    assert model.get_value(node_added_value) == value


def test_make_changed():
    removed_value = 'removed_value'
    added_value = 'added_value'
    changed_node = model.make_changed(removed_value, added_value)
    assert isinstance(changed_node, Callable)

    assert changed_node('get_type') == model.CHANGED
    assert model.get_type(changed_node) == model.CHANGED

    assert changed_node('get_removed') == removed_value
    assert model.get_removed(changed_node) == removed_value

    assert changed_node('get_added') == added_value
    assert model.get_added(changed_node) == added_value


def test_make_nested():
    children = {
        'key1': model.make_unchanged('value1'),
        'key2': model.make_removed('removed_value'),
        'key3': model.make_changed('removed', 'added'),
    }
    nested_node = model.make_nested(children)
    assert isinstance(nested_node, Callable)
    assert model.get_type(nested_node) == model.NESTED
    assert model.get_children(nested_node) == children
