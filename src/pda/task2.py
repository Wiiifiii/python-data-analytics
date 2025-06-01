import pandas as pd
import matplotlib.pyplot as plt

'''
Load the Excel data into a DataFrame.
It is assumed that the file "Opinnäytetyokysely.xlsx" is located in the specified folder.
'''
file_path = r"D:\GitHub\PythonDataAnalytics\doc\Opinnäytetyokysely.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')

print("Columns available:\n", df.columns.to_list())

'''
1) Histogram for the "Sain riittävästi ohjausta" column
'''
guidance_col = 'Sain riittävästi ohjausta'
guidance = df[guidance_col].dropna().astype(int)

plt.figure()
plt.hist(
    guidance,
    bins=range(guidance.min(), guidance.max() + 2),
    edgecolor='black'
)
plt.xticks(range(guidance.min(), guidance.max() + 1))
plt.xlabel(guidance_col)
plt.ylabel('Count')
plt.title('Histogram of "Sain riittävästi ohjausta"')
plt.tight_layout()
plt.show()

'''
2) Scatter plot: "Pystyin itse vaikuttamaan opinnäytetyöni ohjaajan valintaan" vs. "Sain riittävästi ohjausta"

This plot compares the responses between influencing the choice of thesis supervisor and receiving sufficient supervision.
'''
influence_col = 'Pystyin itse vaikuttamaan opinnäytetyöni ohjaajan valintaan'
influence = df[influence_col].dropna().astype(int)
paired_guidance = df.loc[influence.index, guidance_col].astype(int)

plt.figure()
plt.scatter(influence, paired_guidance, alpha=0.7)
plt.xlabel(influence_col)
plt.ylabel(guidance_col)
plt.title('Influence vs. Received Supervision')
plt.tight_layout()
plt.show()

'''
3) Scatter plot: "Opinnäytetyön tekemisaika työviikkoina (40 h) aihekuvauksen tekemisestä työn valmistumiseen:työviikkoa" vs. "Thesis grade"

First, remove rows where the grade is missing.
'''
time_col  = 'Opinnäytetyön tekemisaika työviikkoina (40 h) aihekuvauksen tekemisestä työn valmistumiseen:työviikkoa'
grade_col = 'Thesis grade'

# Remove cases with missing grades
df2 = df.dropna(subset=[grade_col]).copy()
df2[time_col]  = df2[time_col].astype(float)
df2[grade_col] = df2[grade_col].astype(float)

plt.figure()
plt.scatter(df2[time_col], df2[grade_col], alpha=0.7)
plt.xlabel(time_col)
plt.ylabel(grade_col)
plt.title('Duration vs. Thesis Grade')
plt.tight_layout()
plt.show()
