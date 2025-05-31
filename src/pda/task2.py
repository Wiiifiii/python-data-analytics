import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(
    "D:/GitHub/PythonDataAnalytics/doc/Opinnäytetyökysely.xlsx",
    engine='openpyxl'
)
print("Columns available:\n", df.columns.to_list())

# 1) Histogram
guidance_col = 'Sain riittävästi ohjausta'
guidance = df[guidance_col].dropna().astype(int)
plt.figure()
plt.hist(guidance,
         bins=range(guidance.min(), guidance.max() + 2),
         edgecolor='black')
plt.xticks(range(guidance.min(), guidance.max() + 1))
plt.xlabel(guidance_col)
plt.ylabel('Count')
plt.title('Histogram of “Sain riittävästi ohjausta”')
plt.tight_layout()
plt.show()

# 2) Scatter: Influence vs Guidance
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

# 3) Scatter: Time vs Grade
time_col  = 'Opinnäytetyön tekemisaika työviikkoina (40 h) aihekuvauksen tekemisestä työn valmistumiseen:työviikkoa'
grade_col = 'Thesis grade'
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
