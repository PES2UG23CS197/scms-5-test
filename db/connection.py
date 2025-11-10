"""Database connection handler for SCMS, supporting both local and CI environments."""

import os
import mysql.connector

def get_connection():
    """Returns a MySQL connection based on environment (CI or local)."""
    is_ci = os.getenv("CI") == "true"

    if is_ci:
        # CI/CD environment (matches ci.yml)
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="scms"
        )

    # Local development
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="REPLACE_WITH_YOUR_LOCAL_SQL_PASSWORD",
        database="scms"
    )
