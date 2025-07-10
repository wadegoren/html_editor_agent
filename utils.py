def fill_template(html, data):
    """
    Replace placeholders in the HTML with values from data dict.
    Placeholders should be in the form {{name}}, {{date}}, etc.
    """
    for key, value in data.items():
        html = html.replace(f"{{{{{key}}}}}", str(value))
    return html
