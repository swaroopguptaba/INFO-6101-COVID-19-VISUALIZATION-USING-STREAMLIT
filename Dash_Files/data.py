import pandas as pd
import os

os.chdir('/'.join((os.path.abspath(__file__)).split('/')[:-1]))


def get_ny_times_state_wise_date():
    df = pd.read_csv(
        'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    return df


def usa_data():
    # os.chdir('/'.join((os.path.abspath(__file__)).split('/')[:-1]))
    # df = pd.read_csv(
    #     'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv')
    df = get_ny_times_state_wise_date().groupby(['state', 'fips'])["cases", "deaths"].apply(
        lambda x: x.astype(float).sum())
    fips_df = pd.read_csv('data/fips_code_mapping.csv')
    final_df = pd.merge(df, fips_df, on='fips', how='inner')
    return final_df


def get_state_wise_timeseries_date():
    df = pd.read_csv(
        "https://raw.githubusercontent.com/nytimes/covid-19-data/bc60b7c7cefbc17a4e3fe6c3a6e86c65f88ca91d/us-states.csv", error_bad_lines=False)
    return df


def get_unique_states():
    fips_df = pd.read_csv('data/fips_code_mapping.csv')
    return fips_df['Name'].unique()


if __name__ == "__main__":
    get_unique_states()
