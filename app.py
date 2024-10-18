from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from models.database import db, Rule, CombinedRule
from services.rule_service import create_rule, combine_rules, evaluate_rule, modify_rule, optimize_rule
from models.ast import parse_rule
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_rule', methods=['GET', 'POST'])
def create_rule_view():
    if request.method == 'POST':
        rule_string = request.form.get('rule')
        if not rule_string:
            flash("Rule string is required", "error")
            return redirect(url_for('create_rule_view'))
        try:
            ast = create_rule(rule_string)
            flash(f"Rule created successfully: {ast}", "success")
        except Exception as e:
            flash(f"Error creating rule: {str(e)}", "error")
        return redirect(url_for('create_rule_view'))
    return render_template('create_rule.html')

@app.route('/combine_rules', methods=['GET', 'POST'])
def combine_rules_view():
    if request.method == 'POST':
        rules = request.form.getlist('rules')
        if len(rules) < 2:
            flash("At least two rules are required to combine", "error")
            return redirect(url_for('combine_rules_view'))
        try:
            combined_ast = combine_rules(rules)
            optimized_ast = optimize_rule(combined_ast)
            flash(f"Combined Rule: {optimized_ast}", "success")
        except Exception as e:
            flash(f"Error combining rules: {str(e)}", "error")
        return redirect(url_for('combine_rules_view'))
    return render_template('combine_rules.html')

@app.route('/evaluate_rule', methods=['GET', 'POST'])
def evaluate_rule_view():
    if request.method == 'POST':
        rule_string = request.form.get('rule')
        age = request.form.get('age')
        department = request.form.get('department')
        salary = request.form.get('salary')
        experience = request.form.get('experience')

        if not rule_string:
            flash("Rule string is required", "error")
            return redirect(url_for('evaluate_rule_view'))

        try:
            data = {
                "age": int(age) if age else None,
                "department": department,
                "salary": int(salary) if salary else None,
                "experience": int(experience) if experience else None
            }
            ast = parse_rule(rule_string)
            result = evaluate_rule(ast, data)
            flash(f"Evaluation Result: {'Eligible' if result else 'Not Eligible'}", "success")
        except Exception as e:
            flash(f"Error evaluating rule: {str(e)}", "error")
        return redirect(url_for('evaluate_rule_view'))
    return render_template('evaluate_rule.html')

@app.route('/modify_rule', methods=['GET', 'POST'])
def modify_rule_view():
    if request.method == 'POST':
        rule_string = request.form.get('rule')
        path = request.form.get('path').split(',')
        new_value = request.form.get('new_value')

        if not rule_string or not path or not new_value:
            flash("Rule string, path, and new value are required", "error")
            return redirect(url_for('modify_rule_view'))

        try:
            ast = parse_rule(rule_string)
            modified_ast = modify_rule(ast, path, new_value)
            flash(f"Modified Rule: {modified_ast}", "success")
        except Exception as e:
            flash(f"Error modifying rule: {str(e)}", "error")
        return redirect(url_for('modify_rule_view'))
    return render_template('modify_rule.html')

@app.route('/save_rule', methods=['POST'])
def save_rule():
    name = request.form.get('name')
    rule_string = request.form.get('rule')
    if not name or not rule_string:
        flash('Name and rule are required', 'error')
        return redirect(url_for('create_rule_view'))
    
    new_rule = Rule(name=name, rule_string=rule_string)
    db.session.add(new_rule)
    db.session.commit()
    flash('Rule saved successfully', 'success')
    return redirect(url_for('create_rule_view'))

@app.route('/save_combined_rule', methods=['POST'])
def save_combined_rule():
    name = request.form.get('name')
    rule_ids = request.form.getlist('rule_ids')
    if not name or not rule_ids:
        flash('Name and at least two rules are required', 'error')
        return redirect(url_for('combine_rules_view'))
    
    rules = Rule.query.filter(Rule.id.in_(rule_ids)).all()
    rule_strings = [rule.rule_string for rule in rules]
    combined_ast = combine_rules(rule_strings)
    optimized_ast = optimize_rule(combined_ast)
    combined_rule_string = str(optimized_ast)
    
    new_combined_rule = CombinedRule(name=name, rule_ids=','.join(rule_ids), combined_rule_string=combined_rule_string)
    db.session.add(new_combined_rule)
    db.session.commit()
    flash('Combined rule saved successfully', 'success')
    return redirect(url_for('combine_rules_view'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)