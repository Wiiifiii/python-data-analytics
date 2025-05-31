import pandas as pd
from pda import ace_tools as tools

# Load the survey data
df = pd.read_excel("D:/GitHub/PythonDataAnalytics/doc/Opinnäytetyökysely.xlsx", sheet_name="Kysely")

# Task 1: Crosstabulation 1 - Opiskeluala vs. Sukupuoli
ct1 = pd.crosstab(df['Opiskeluala'], df['Sukupuoli'])

# Task 2: Relative distribution of men and women across fields (percentages, column-normalized)
ct2 = pd.crosstab(df['Opiskeluala'], df['Sukupuoli'], margins=True, normalize='columns').mul(100).round(2)

# Task 3: Relative distribution with row sums = 100% (row-normalized percentages),
# and total counts of each gender as a final row
ct3 = pd.crosstab(df['Opiskeluala'], df['Sukupuoli'], normalize='index').mul(100).round(2)
totals = df['Sukupuoli'].value_counts()
ct3.loc['Total count'] = totals

# Dummy variable: Oliko työ parityö? (1 = Kyllä, 0 = Ei)
dummy_counts = df['Oliko työ parityö?'].value_counts().rename(index={1: 'Kyllä', 0: 'Ei'})
dummy_prop = (dummy_counts / dummy_counts.sum() * 100).round(2)
dummy_table = pd.DataFrame({'Count': dummy_counts, 'Percentage': dummy_prop})

# Display the tables to the user
tools.display_dataframe_to_user('Ristiintaulukointi 1: Opiskeluala vs. Sukupuoli', ct1)
tools.display_dataframe_to_user('Ristiintaulukointi 2: Miesten ja naisten suhteellinen jakautuminen (%)', ct2)
tools.display_dataframe_to_user('Ristiintaulukointi 3: Sukupuolijakauma aloittain (%) ja kokonaismäärä', ct3)
tools.display_dataframe_to_user('Dummy-muuttuja: Oliko työ parityö?', dummy_table)
