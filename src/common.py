import sys

sys.path.insert(0, "/Users/louisrae/Documents/dev/dfy_setters")

from src.constants import *
import pandas as pd
from sqlalchemy import create_engine


def parse_csv_of_roles():
    """Uses postgres to pull through all members

    Returns:
        dataframe: Returns two columns, name and role
    """
    engine = create_engine(DATABASE_URI)

    myQuery = "SELECT full_name,role FROM team"
    df = pd.read_sql_query(myQuery, engine)
    return df
