import pandas as pd


def task1_corr(df: pd.DataFrame) -> None:
    """
    Task 1: Calculate correlation coefficients and R-squared for two variable pairs.
    """
    # Pair 1: Active info seeking vs. Interest in topic
    var1a = "Hankin itse aktiivisesti tietoa työni aiheesta"
    var1b = "Tutkimusaiheeni kiinnosti minua"
    corr1 = df[var1a].corr(df[var1b])
    r2_1 = corr1 ** 2

    # Pair 2: Received enough guidance vs. Time to complete thesis
    var2a = "Sain riittävästi ohjausta"
    var2b = (
        "Opinnäytetyön tekemiseen kulunut aika ensimmäisistä"
        " aihekaavailuista työn valmistumiseen:kuukautta"
    )
    corr2 = df[var2a].corr(df[var2b])
    r2_2 = corr2 ** 2

    print("\n=== Task 1: Correlations and R-squared ===")
    print(f"1) Corr({var1a}, {var1b}) = {corr1:.2f}, R^2 = {r2_1:.2f}")
    print(f"2) Corr({var2a}, {var2b}) = {corr2:.2f}, R^2 = {r2_2:.2f}")


def task2_corr(df: pd.DataFrame) -> None:
    """
    Task 2: Create new column for overall satisfaction and compute correlation.
    """
    # List of guidance satisfaction questions
    satisfaction_questions = [
        "Ohjaajani panos tuki työtäni",
        "Saamani ohjaus oli asiantuntevaa",
        "Saamani ohjaus oli motivoivaa",
        "Työni ohjaaja vastasi nopeasti tiedusteluihini",
        "Ohjaustilanteet eivät tuntuneet minusta pelottavilta",
        "Ohjaajaani oli helppo lähestyä",
        "Luotin ohjaajani neuvoihin"
    ]
    # Compute row-wise mean
    df["Kokonaistyytyväisyys ohjaukseen"] = df[satisfaction_questions].mean(axis=1)

    # Correlation with ability to choose supervisor
    var_choice = "Pystyin itse vaikuttamaan opinnäytetyöni ohjaajan valintaan"
    var_sat = "Kokonaistyytyväisyys ohjaukseen"
    corr = df[var_choice].corr(df[var_sat])
    r2 = corr ** 2

    print("\n=== Task 2: Satisfaction Correlation ===")
    print(f"Corr({var_choice}, {var_sat}) = {corr:.2f}, R^2 = {r2:.2f}")


def task3_corr_matrix(df: pd.DataFrame) -> None:
    """
    Task 3: Correlation matrix for enthusiasm and various guidance support columns.
    """
    cols = [
        "Olin innostunut opinnäytetyötä tehdessäni",
        "Ohjaajan tuki opinnäytetyön eri vaiheissa:aiheen valinnassa",
        "Ohjaajan tuki opinnäytetyön eri vaiheissa:tutkimuskysymysten tai kehittämistehtävän rajauksessa",
        "Ohjaajan tuki opinnäytetyön eri vaiheissa:menetelmien valinnassa",
        "Ohjaajan tuki opinnäytetyön eri vaiheissa:aineiston analyysissa",
        "Ohjaajan tuki opinnäytetyön eri vaiheissa:johtopäätösten ja yhteenvedon tekemisessa",
        "Ohjaajan tuki opinnäytetyön eri vaiheissa:raportoinnissa"
    ]
    df_sub = df[cols].copy()
    corr_matrix = df_sub.corr()

    print("\n=== Task 3: Correlation Matrix ===")
    print(corr_matrix)


if __name__ == "__main__":
    # Define file path
    path = r"D:\GitHub\PythonDataAnalytics\doc\Opinnäytetyökysely.xlsx"
    df = pd.read_excel(path, sheet_name="Kysely")

    # Run Task 1
    task1_corr(df)

    # Run Task 2
    task2_corr(df)

    # Run Task 3
    task3_corr_matrix(df)
