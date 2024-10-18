# tests/test_rule_creation.py

import pytest
from services.rule_service import create_rule, RuleError

def test_create_simple_rule():
    rule_string = "age > 30"
    ast = create_rule(rule_string)
    assert ast.type == "operand"
    assert ast.value == ("age", ">", "30")

def test_create_complex_rule():
    rule_string = "(age > 30 AND department = 'Sales') OR (salary > 50000)"
    ast = create_rule(rule_string)
    assert ast.type == "operator"
    assert ast.value == "OR"
    assert ast.left.type == "operator"
    assert ast.left.value == "AND"
    assert ast.right.type == "operand"


def test_invalid_rule():
    with pytest.raises(RuleError):
        create_rule("invalid rule")

def test_invalid_attribute():
    with pytest.raises(RuleError):
        create_rule("invalid_attribute > 30")

def test_invalid_value():
    with pytest.raises(RuleError):
        create_rule("age > invalid_value")