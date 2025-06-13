import html

def get_percentage(form_json):
    """Calculate the percentage of fields filled in the selected forms."""
    filled = sum(1 for key, val in form_json.items() if key != "form_name" and val not in [None, ""])
    total = len(form_json) - 1 if "form_name" in form_json else len(form_json)
    return round((filled / total) * 100, 0) if total else 0


def generate_html_form(form_data: dict) -> str:
    html_parts = []

    # Header and open form tag
    form_name = html.escape(form_data.get("form_name", ""))
    html_parts.append(f'<h2>{form_name}</h2>')
    html_parts.append('<form id="sample-form" method="POST" action="/save_html">')

    # Generate input fields
    for key, value in form_data.items():
        if key == "form_name":
            continue
        input_type = "date" if "date" in key.lower() or "dob" in key.lower() else "text"
        label = key.replace('_', ' ').title()
        value_attr = f'value="{html.escape(str(value))}"' if value else ''
        html_parts.append(f'  <label>{label}: <input name="{html.escape(key)}" type="{input_type}" {value_attr}></label>')

    # Save button
    html_parts.append('''
  <button type="button" id="save-form-btn" disabled>
    <span class="btn-text">Save</span>
    <span class="loader" style="display: none;"></span>
  </button>
''')
    html_parts.append('</form>')

    return "".join(html_parts)