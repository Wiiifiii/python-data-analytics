import pandas as pd
from pda import ace_tools as tools

'''
Load the Excel data into a DataFrame from the "Kysely" sheet.
It is assumed that the file "Opinnäytetyökysely.xlsx" is located in the specified folder.
'''
file_path = r"D:\GitHub\PythonDataAnalytics\doc\Opinnäytetyokysely.xlsx"
df = pd.read_excel(file_path, sheet_name="Kysely", engine="openpyxl")

'''
1) Crosstab: "Opiskeluala" vs. "Sukupuoli"
'''
ct1 = pd.crosstab(df["Opiskeluala"], df["Sukupuoli"])

'''
2) Column-normalized percentage distribution (relative distribution of males and females across study fields).
Includes a marginal row "All".
'''
ct2 = (
    pd.crosstab(
        df["Opiskeluala"],
        df["Sukupuoli"],
        margins=True,
        normalize="columns",
    )
    .mul(100)
    .round(2)
)

'''
3) Row-normalized percentage distribution (gender distribution within each study field).
Add total counts as a row.
'''
ct3 = pd.crosstab(df["Opiskeluala"], df["Sukupuoli"], normalize="index").mul(100).round(2)
totals = df["Sukupuoli"].value_counts()
ct3.loc["Total count"] = totals

'''
4) Dummy variable: "Was the work done in pairs?" (1 = Yes, 0 = No).
First, calculate the counts, then the percentages, and combine them into a DataFrame.
'''
dummy_counts = (
    df["Oliko työ parityö?"]
    .value_counts()
    .rename(index={1: "Yes", 0: "No"})
)
dummy_prop = (dummy_counts / dummy_counts.sum() * 100).round(2)
dummy_table = pd.DataFrame({"Count": dummy_counts, "Percentage": dummy_prop})

'''
Display the tables to the user.
tools.display_dataframe_to_user will open the content of each DataFrame in an interactive table.
'''
tools.display_dataframe_to_user("Crosstab 1: Study Field vs. Gender", ct1)
tools.display_dataframe_to_user(
    "Crosstab 2: Relative distribution (%) of males and females", ct2
)
tools.display_dataframe_to_user(
    "Crosstab 3: Gender distribution within each study field (%) and total count", ct3
)
tools.display_dataframe_to_user("Dummy variable: Was the work done in pairs?", dummy_table)
