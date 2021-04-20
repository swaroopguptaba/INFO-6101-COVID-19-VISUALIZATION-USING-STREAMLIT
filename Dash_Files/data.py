import pandas as pd


def usa_data():
    df = pd.read_csv(
        'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    df = df.groupby(['state', 'fips'])["cases", "deaths"].apply(
        lambda x: x.astype(float).sum())
    fips_df = pd.read_csv(
        "data/fips_code_mapping.csv")
    final_df = pd.merge(df, fips_df, on='fips', how='inner')
    return final_df
