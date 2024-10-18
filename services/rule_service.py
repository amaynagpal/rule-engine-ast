# services/rule_service.py

from models.ast import Node, parse_rule
from models.catalog import AttributeCatalog

catalog = AttributeCatalog()

class RuleError(Exception):
    pass

def create_rule(rule_string):
    try:
        ast = parse_rule(rule_string)
        validate_rule(ast)
        return ast
    except Exception as e:
        raise RuleError(f"Invalid rule string: {str(e)}")

def validate_rule(ast):
    if ast.type == 'operand':
        attribute, _, value = ast.value
        catalog.validate(attribute, value)
    elif ast.type == 'operator':
        validate_rule(ast.left)
        validate_rule(ast.right)

def combine_rules(rules):
    if len(rules) < 2:
        raise RuleError("At least two rules are required to combine")
    
    try:
        combined_ast = parse_rule(rules[0])
        for rule in rules[1:]:
            rule_ast = parse_rule(rule)
            combined_ast = Node('operator', 'AND', combined_ast, rule_ast)
        return combined_ast
    except Exception as e:
        raise RuleError(f"Error combining rules: {str(e)}")

def evaluate_rule(ast, data):
    try:
        if ast.type == 'operand':
            attribute, operator, value = ast.value
            if attribute not in data:
                return False
            if operator == '=':
                return str(data[attribute]) == value.strip("'\"")
            elif operator == '>':
                return float(data[attribute]) > float(value)
            elif operator == '<':
                return float(data[attribute]) < float(value)
            else:
                raise RuleError(f"Unknown operator: {operator}")
        elif ast.type == 'operator':
            if ast.value == 'AND':
                return evaluate_rule(ast.left, data) and evaluate_rule(ast.right, data)
            elif ast.value == 'OR':
                return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)
            else:
                raise RuleError(f"Unknown operator: {ast.value}")
    except Exception as e:
        raise RuleError(f"Error evaluating rule: {str(e)}")

def modify_rule(ast, path, new_value):
    if not path:
        return Node('operand', new_value) if isinstance(new_value, tuple) else Node('operator', new_value)
    
    current, *remaining = path
    if current == 'left':
        ast.left = modify_rule(ast.left, remaining, new_value)
    elif current == 'right':
        ast.right = modify_rule(ast.right, remaining, new_value)
    elif current == 'value':
        if ast.type == 'operand':
            attribute, operator, _ = ast.value
            ast.value = (attribute, operator, new_value)
        else:
            ast.value = new_value
    else:
        raise ValueError(f"Invalid path: {current}")
    
    return ast

def optimize_rule(ast):
    if ast.type == 'operator':
        ast.left = optimize_rule(ast.left)
        ast.right = optimize_rule(ast.right)
        
        if ast.value == 'AND':
            if ast.left.type == 'operand' and ast.right.type == 'operand':
                if ast.left.value[0] == ast.right.value[0]:  # Same attribute
                    attr, op1, val1 = ast.left.value
                    _, op2, val2 = ast.right.value
                    if op1 == '>' and op2 == '>':
                        return Node('operand', (attr, '>', max(float(val1), float(val2))))
                    elif op1 == '<' and op2 == '<':
                        return Node('operand', (attr, '<', min(float(val1), float(val2))))
        
        elif ast.value == 'OR':
            if ast.left.type == 'operand' and ast.right.type == 'operand':
                if ast.left.value[0] == ast.right.value[0]:  # Same attribute
                    attr, op1, val1 = ast.left.value
                    _, op2, val2 = ast.right.value
                    if op1 == '>' and op2 == '>':
                        return Node('operand', (attr, '>', min(float(val1), float(val2))))
                    elif op1 == '<' and op2 == '<':
                        return Node('operand', (attr, '<', max(float(val1), float(val2))))
    
    return ast