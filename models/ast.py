# models/ast.py
class Node:
    def __init__(self, type, value=None, left=None, right=None):
        self.type = type
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        if self.type == 'operand':
            return f"{self.value[0]} {self.value[1]} {self.value[2]}"
        return f"({self.left} {self.value} {self.right})"

def parse_rule(rule_string):
    tokens = tokenize(rule_string)
    if not tokens:
        raise ValueError("Empty rule string")
    return parse_expression(tokens)

def tokenize(rule_string):
    return rule_string.replace('(', ' ( ').replace(')', ' ) ').split()

def parse_expression(tokens):
    if not tokens:
        raise ValueError("Unexpected end of expression")
    if tokens[0] == '(':
        tokens.pop(0)  # Remove opening parenthesis
        left = parse_expression(tokens)
        if not tokens:
            raise ValueError("Unexpected end of expression")
        operator = tokens.pop(0)
        right = parse_expression(tokens)
        if not tokens or tokens[0] != ')':
            raise ValueError("Missing closing parenthesis")
        tokens.pop(0)  # Remove closing parenthesis
        return Node('operator', operator, left, right)
    else:
        return parse_operand(tokens)

def parse_operand(tokens):
    if len(tokens) < 3:
        raise ValueError("Invalid operand format")
    attribute = tokens.pop(0)
    operator = tokens.pop(0)
    value = tokens.pop(0)
    return Node('operand', (attribute, operator, value))