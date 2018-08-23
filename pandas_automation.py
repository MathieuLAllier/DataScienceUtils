import pandas as pd
from pandas.api.types import CategoricalDtype
import numpy as np


def display_all(df, rows=10):
    with pd.option_context("display.max_rows", rows, "display.max_columns", 1000):
        print(df)


def auto_change_type(df, type_dict):
    """
    :param df: Pandas DataFrame
    :param type_dict: Dictionary of column name and type to format to in the format:
            {'month': CategoricalDtype(categories=range(1,13))}
            ** Only necessary for Categorical & Boolean Columns **
    :return: Pandas DataFrame
    """
    for col in type_dict:
        df[col] = df[col].astype(type_dict[col])

    return df


def auto_dates(df, date_name='date', time=False):
    """
    :param df: Pandas DataFrame
    :param date_name: Only needed if index is not DatetimeIndex type.
                        String: Name of date column in df
    :param time: Set to True if time part is necessary
    :return: Pandas DataFrame
    """
    T = df.index.to_series() if isinstance(df.index, pd.DatetimeIndex) else df[date_name]

    if time:
        df['hour'] = T.dt.hour
        df['minute'] = T.dt.minute
        df['second'] = T.dt.second
    df['year'] = T.dt.year
    df['month'] = T.dt.month.astype(CategoricalDtype(categories=range(1, 13)))
    df['day'] = T.dt.day.astype(CategoricalDtype(categories=range(1, 32)))
    df['week'] = T.dt.weekofyear.astype(CategoricalDtype(categories=range(1, 54)))
    df['dow'] = T.dt.dayofweek.astype(CategoricalDtype(categories=range(0, 7)))
    df['doy'] = T.dt.dayofyear.astype(CategoricalDtype(categories=range(0, 366)))
    df['start_month'] = T.dt.is_month_start.astype('int')
    df['end_month'] = T.dt.is_month_end.astype('int')
    df['start_quarter'] = T.dt.is_quarter_start.astype('int')
    df['end_quarter'] = T.dt.is_quarter_end.astype('int')
    df['start_year'] = T.dt.is_year_start.astype('int')
    df['end_year'] = T.dt.is_year_end.astype('int')
    df['n_day_in_month'] = T.dt.days_in_month
    return df


def auto_remove_novariance(df):
    """
    :param df: Pandas DataFrame
    :return: Pandas DataFrame
    """
    uniques = df.apply(pd.Series.nunique)
    return df.drop(columns=list(uniques[uniques == 1].index))


def auto_dummies(df):
    """
    :param df: Pandas DataFrame
    :return: Pandas Dataframe()
    """
    return pd.get_dummies(df, columns=list(df.select_dtypes(include='category').columns), drop_first=True)


def get_category_size(df):
    cat = df.select_dtypes(include='category').columns
    return [(c, len(df[c].cat.categories), min(50, len(df[c].cat.categories) // 2)) for c in cat]


def sort_columns(df):
    return df[sorted(df.columns)]


if __name__ == '__main__':
    dates = pd.date_range('20130101', periods=5000)
    dfs = pd.DataFrame(np.random.randn(5000, 4), index=dates, columns=list('ABCD'))
    dfs = auto_dates(dfs)
    dfs = sort_columns(dfs)
