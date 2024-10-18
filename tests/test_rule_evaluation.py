# tests/test_rule_evaluation.py

import pytest
from services.rule_service import create_rule, evaluate_rule, RuleError

def test_evaluate_simple_rule():
    rule = create_rule("age > 30")
    assert evaluate_rule(rule, {"age": 35}) == True
    assert evaluate_rule(rule, {"age": 25}) == False

def test_evaluate_complex_rule():
    rule = create_rule("(age > 30 AND department = 'Sales') OR (salary > 50000)")
    assert evaluate_rule(rule, {"age": 35, "department": "Sales", "salary": 40000}) == True
    assert evaluate_rule(rule, {"age": 25, "department": "Marketing", "salary": 60000}) == True
    assert evaluate_rule(rule, {"age": 25, "department": "Marketing", "salary": 40000}) == False

def test_evaluate_missing_data():
    rule = create_rule("age > 30")
    assert evaluate_rule(rule, {}) == False

def test_evaluate_invalid_operator():
    with pytest.raises(RuleError):
        rule = create_rule("age @ 30")
        evaluate_rule(rule, {"age": 35})