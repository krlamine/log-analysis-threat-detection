import pyodbc


def get_connection():
    """
    Update the connection string below according to your local SQL Server setup.
    
    Example:
    - SERVER=localhost\\SQLEXPRESS
    - DATABASE=log_threat_detection
    """

    connection_string = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=log_threat_detection;"
        "Trusted_Connection=yes;"
    )

    return pyodbc.connect(connection_string)