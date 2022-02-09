import pandas as pd


def parse_csv_of_roles(file_path):
    """Uses csv as a database to pull through data for each team member

    Returns:
        dataframe: Returns two columns, name and role
    """
    df = pd.read_csv(file_path)
    return df
