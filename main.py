import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def prepare_data():
    data = pd.read_csv('2972656.csv')

    # convering to DATE column to `datetime` object and setting to be the index index
    data.index = data['DATE']
    del data['DATE']
    data.index = pd.to_datetime(data.index, format='%Y-%m-%d')

    # creating two required tables, removing rows, containing NaNs
    tmax = pd.DataFrame(index=data.index)
    tmax['TMAX'] = data['TMAX']
    tmax.dropna(inplace=True)

    snow = pd.DataFrame(index=data.index)
    snow['SNOW'] = data['SNOW']
    snow.dropna(inplace=True)

    # droping all months in each year with less than 28 records
    tmax = tmax.groupby(by=[tmax.index.month, tmax.index.year]).filter(lambda x: len(x) > 28)
    snow = snow.groupby(by=[snow.index.month, snow.index.year]).filter(lambda x: len(x) > 28)

    return tmax, snow


def show_monthly_temp_one_plot(tmax):
    avg = pd.DataFrame(tmax.groupby(by=[tmax.index.month, tmax.index.year]).mean())
    avg.reset_index(inplace=True, level=1)
    avg.rename(columns={'DATE': 'year'}, inplace=True)
    avg.reset_index(inplace=True)
    avg.rename(columns={'DATE': 'month'}, inplace=True)
    sns.barplot(x='month', y='TMAX', data=avg)
    plt.show()


def show_monthly_temp(tmax):
    avg = pd.DataFrame(tmax.groupby(by=[tmax.index.month, tmax.index.year]).mean())
    avg.reset_index(inplace=True, level=1)
    avg.rename(columns={'DATE': 'year'}, inplace=True)
    avg.reset_index(inplace=True)
    avg.rename(columns={'DATE': 'month'}, inplace=True)

    fig = plt.figure()
    for i in range(1, 13):
        avg_monthly = avg[avg['month'] == i]  # select dataframe with month = i
        ax = fig.add_subplot(12, 1, i)  # add subplot in the i-th position on a grid 12x1
        ax.plot(avg_monthly['year'], avg_monthly['TMAX'])
    plt.show()


if __name__ == '__main__':
    tmax, snow = prepare_data()
    show_monthly_temp(tmax)
