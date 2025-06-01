# task1.py

import pandas as pd

def main():
    ''' 
    1) Load the Excel file

    Replace the path below with your own file path if needed.
    For example, on Windows:
        r"D:\GitHub\PythonDataAnalytics\doc\Opinnäytetyokysely.xlsx"

    It is assumed that 'Opinnäytetyokysely.xlsx' is located in the specified folder.
    '''
    file_path = r"D:\GitHub\PythonDataAnalytics\doc\Opinnäytetyokysely.xlsx"
    df = pd.read_excel(file_path)

    ''' 
    2) Inspect the beginning and end of the data
    '''
    print("First 5 rows (head):")
    print(df.head(), end="\n\n")

    print("Last 5 rows (tail):")
    print(df.tail(), end="\n\n")

    ''' 
    3) Display column names with their non-null counts
       (i.e. the number of non-missing values per column)
    '''
    print("Column names with non-null counts:")
    print(df.count(), end="\n\n")

    ''' 
    4) Count missing values (NaN) per column
    '''
    print("Missing values per column:")
    print(df.isnull().sum(), end="\n\n")

    '''
    5) Display the data types of each column
    '''
    print("Data types of each column:")
    print(df.dtypes, end="\n\n")

    '''
    6) Example frequency table for the 'Opiskeluala' column

    If you want to use another column, replace 'Opiskeluala'
    with the desired column name.
    '''
    print("Frequency table for 'Opiskeluala':")
    freq = df["Opiskeluala"].value_counts(dropna=False)
    print(freq, end="\n\n")

if __name__ == "__main__":
    main()
