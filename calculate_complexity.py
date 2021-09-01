"""
Make data uniform and Calculate complexity of data
"""
import cmas
import pandas as pd


def main():
    data = pd.read_csv('./data/'+input("\nGive Name of data: ")+'.csv')
    data = cmas.reform_data(data, file='reddit_data_fixed')
    cmas.calculate_complexity(data)


if __name__ == "__main__":
    main()