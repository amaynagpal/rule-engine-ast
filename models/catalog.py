class AttributeCatalog:
    def __init__(self):
        self.attributes = {
            'age': {'type': 'int', 'min': 0, 'max': 120},
            'department': {'type': 'str', 'allowed': ['Sales', 'Marketing', 'IT', 'HR']},
            'salary': {'type': 'int', 'min': 0},
            'experience': {'type': 'int', 'min': 0},
        }

    def validate(self, attribute, value):
        if attribute not in self.attributes:
            raise ValueError(f"Invalid attribute: {attribute}")

        attr_info = self.attributes[attribute]
        if attr_info['type'] == 'int':
            try:
                float_value = float(value)
                int_value = int(float_value)
                if float_value != int_value:
                    raise ValueError(f"{attribute} must be an integer")
                if 'min' in attr_info and int_value < attr_info['min']:
                    raise ValueError(f"{attribute} must be at least {attr_info['min']}")
                if 'max' in attr_info and int_value > attr_info['max']:
                    raise ValueError(f"{attribute} must be at most {attr_info['max']}")
            except ValueError:
                raise ValueError(f"{attribute} must be an integer")
        elif attr_info['type'] == 'str':
            # Remove quotes from the value if present
            cleaned_value = value.strip("'\"")
            if 'allowed' in attr_info and cleaned_value not in attr_info['allowed']:
                raise ValueError(f"{attribute} must be one of {', '.join(attr_info['allowed'])}")