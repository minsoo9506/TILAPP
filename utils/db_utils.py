from sqlalchemy import inspect


def row_to_dict(row) -> dict:
    """Convert a SQLAlchemy row object to a dictionary."""
    return {c.key: getattr(row, c.key) for c in inspect(row).mapper.column_attrs}
