import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """
    Reads the survey data from the given Excel file.
    """
    return pd.read_excel(path, sheet_name="Kysely")


def descriptive_stats(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Calculates descriptive statistics (count, mean, std, min, quartiles, max)
    for a given numeric column, renaming the output to Finnish labels.
    """
    df_time = df.dropna(subset=[col])
    desc = df_time[col].describe().rename({
        "count": "Lukumäärä",
        "mean": "Keskiarvo",
        "std": "Keskihajonta",
        "min": "Minimi",
        "25%": "25 % kvartiili",
        "50%": "Mediaani",
        "75%": "75 % kvartiili",
        "max": "Maksimi"
    })
    return desc.to_frame(name="Arvo")


def guidance_pivot(df: pd.DataFrame, index_col: str, questions: list) -> pd.DataFrame:
    """
    Creates a pivot table of average responses for the guidance questions,
    indexed by the given field (e.g., "Opiskeluala").
    """
    pivot = pd.pivot_table(
        df,
        index=index_col,
        values=questions,
        aggfunc="mean"
    )
    return pivot


if __name__ == "__main__":
    # Define file path
    path = r"D:\GitHub\PythonDataAnalytics\doc\Opinnäytetyökysely.xlsx"
    df = load_data(path)

    # 4.1 Descriptive statistics for thesis completion time
    time_var = (
        "Opinnäytetyön tekemiseen kulunut aika ensimmäisistä "
        "aihekaavailuista työn valmistumiseen:kuukautta"
    )
    stats_df = descriptive_stats(df, time_var)
    print("\n=== Descriptive Statistics for Thesis Completion Time ===")
    print(stats_df)

    # 4.2 Pivot table of guidance questions
    questions = [
        "Sain riittävästi ohjausta",
        "Ohjaajaani oli helppo lähestyä",
        "Luotin ohjaajani neuvoihin"
    ]
    pivot_df = guidance_pivot(df, "Opiskeluala", questions)
    print("\n=== Average Guidance Ratings by Field ===")
    print(pivot_df)
