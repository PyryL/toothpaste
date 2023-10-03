from datetime import datetime

def format_date(date: datetime) -> str:
    """Returns the given datetime formatted to human-readable format."""
    return date.strftime("%Y-%m-%d at %H:%M")

def apply_jinja_function(app):
    """Make the date formatter function available in template files."""
    # https://stackoverflow.com/a/7226047
    app.jinja_env.globals.update(format_date=format_date)
