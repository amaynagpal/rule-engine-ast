# tests/test_rule_combination.py

import pytest
from services.rule_service import combine_rules, RuleError

def test_combine_two_rules():
    rule1 = "age > 30"
    rule2 = "department = 'Sales'"
    combined_ast = combine_rules([rule1, rule2])
    assert combined_ast.type == "operator"
    assert combined_ast.value == "AND"
    assert combined_ast.left.type == "operand"
    assert combined_ast.right.type == "operand"

def test_combine_multiple_rules():
    rules = [
        "age > 30",
        "department = 'Sales'",
        "salary > 50000"
    ]
    combined_ast = combine_rules(rules)
    assert combined_ast.type == "operator"
    assert combined_ast.value == "AND"
    assert combined_ast.left.type == "operator"
    assert combined_ast.right.type == "operand"

def test_combine_rules_with_same_operator():
    rules = [
        "(age > 30 AND department = 'Sales')",
        "(salary > 50000 AND experience > 5)"
    ]
    combined_ast = combine_rules(rules)
    assert combined_ast.type == "operator"
    assert combined_ast.value == "AND"
    assert combined_ast.left.type == "operator"
    assert combined_ast.right.type == "operator"

def test_combine_rules_error():
    with pytest.raises(RuleError):
        combine_rules(["age > 30"])