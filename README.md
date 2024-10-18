# Rule Engine with AST

## Overview
This project implements a simple 3-tier rule engine application using Abstract Syntax Trees (AST) to determine user eligibility based on attributes like age, department, income, and experience. The system allows for dynamic creation, combination, and modification of conditional rules.

## Features

- Create complex rules using a simple string syntax
- Combine multiple rules into a single rule
- Evaluate rules against user data
- Modify existing rules
- Optimize rules to reduce redundant checks
- Validate rules against a predefined attribute catalog

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/amaynagpal/rule-engine-ast.git
   ```
   OR You can download the zip file and open it in your VS Code. 

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```
   python app.py
   ```

## Screenshots of Project
### Landing Page
<img width="960" alt="image" src="https://github.com/user-attachments/assets/b2362c12-1894-4868-9bde-1f243f707c2d">

### Create Rule Page
<img width="960" alt="image" src="https://github.com/user-attachments/assets/4fe1e1e3-8e69-4a2f-9b68-93a8e948ccb8">
<br>
<img width="960" alt="image" src="https://github.com/user-attachments/assets/21ec383f-d957-47b7-831c-56a78533aff6">

### Combine Rule
<img width="960" alt="image" src="https://github.com/user-attachments/assets/5d7d8631-193e-48f6-8e15-9695d6503ef6">
<br>
<img width="960" alt="image" src="https://github.com/user-attachments/assets/828c69c3-470c-484c-8c5a-d2949c87a9c7">

### Evaluate Rule
<img width="960" alt="image" src="https://github.com/user-attachments/assets/b91dcb62-1818-4976-931a-8a1773676cba">
<br>
<img width="960" alt="image" src="https://github.com/user-attachments/assets/bdcd4353-3355-48e6-81c2-a7b5283bcf80">

### Modify Rule
<img width="960" alt="image" src="https://github.com/user-attachments/assets/4db1db98-dd35-413c-b015-ffc60e78dcb7">
<br>
<img width="960" alt="image" src="https://github.com/user-attachments/assets/79ce414d-f357-41de-aa4e-706341989fe0">

## Usage
### Creating a Rule

To create a rule, use the following syntax:
```
(condition1 AND condition2) OR condition3
```
Example:
```
(age > 30 AND department = Sales) OR (salary > 50000)
```


### Combining Rules

You can combine multiple rules using the `combine_rules` function:

```python
from services.rule_service import combine_rules
rule1 = "age > 30"
rule2 = "department = 'Sales'"
combined_rule = combine_rules([rule1, rule2])
```

### Evaluating Rules

To evaluate a rule against user data:

```python
from services.rule_service import create_rule, evaluate_rule
rule = create_rule("age > 30 AND department = Sales")
user_data = {"age": 35, "department": "Sales"}
result = evaluate_rule(rule, user_data)
```

### Modifying Rules

To modify a rule against user data:

```python
from services.rule_service import create_rule, evaluate_rule
rule = create_rule("age > 30 AND department = Sales")
user_data = {"age": 35, "department": "Sales"}
result = evaluate_rule(rule, user_data)
```

