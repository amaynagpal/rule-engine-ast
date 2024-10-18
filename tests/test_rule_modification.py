# tests/test_rule_modification.py

import pytest
from services.rule_service import create_rule, modify_rule

def test_modify_operator():
    rule = create_rule("age > 30 AND department = 'Sales'")
    modified_rule = modify_rule(rule, ['value'], 'OR')
    assert str(modified_rule) == "(age > 30 OR department = 'Sales')"

def test_modify_nested_rule():
    rule = create_rule("(age > 30 AND department = 'Sales') OR (salary > 50000)")
    modified_rule = modify_rule(rule, ['left', 'right', 'value'], '40000')
    assert str(modified_rule) == "((age > 30 AND department = '40000') OR (salary > 50000))"

def test_modify_invalid_path():
    rule = create_rule("age > 30")
    with pytest.raises(ValueError):
        modify_rule(rule, ['invalid'], 'new_value')

def test_modify_invalid_value():
    rule = create_rule("age > 30")
    modified_rule = modify_rule(rule, ['value'], 'invalid_operator')
    assert str(modified_rule) == "age > invalid_operator"