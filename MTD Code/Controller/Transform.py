# from Model.Libraries import *
import logging
import pandas as pd


def dataframe(data, columns):
    df = pd.DataFrame(data, columns= columns)
    return df


def typecasting(df, column):
    df[column] = df[column].astype(int)
    return df


def leftjoin(left_df, right_df, column):
    merged_df = pd.merge(left_df, right_df, left_on=column, right_on=column, how="left")
    return merged_df

def leftjoin2(left_df, right_df, left_on, right_on):
    merged_df = pd.merge(left_df, right_df, left_on=left_on, right_on=right_on, how="left")
    return merged_df


def addingdate(df, column, dt):
    df[column] = dt
    return df


def datetimefunc(df, column):
    df[column] = pd.to_datetime(df[column], format='%Y-%m-%d')
    return df


def fill(df):
    df.fillna(0, inplace=True)
    return df


def formatting(df, columns_to_keep):
    df = df.loc[:, columns_to_keep]
    return df

def dropcolumn(df, column):
    df = df.drop(columns=column)
    return df

