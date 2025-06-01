# task8.py
# --------
# Tehtävä 8: Merkitsevyystestaus käyttäen tiedostoa 'Opinnäytetyökysely.xlsx'
#
#  1) Tehtävä 1: t‐test (kulttuuri vs. tekniikka) opinnäytetyön tekemisaika (työviikkoina)
#  2) Tehtävä 2: Mann‐Whitney U (kulttuuri vs. liiketalous) seminaarien hyödyllisyys
#
# Asenna tarvittavat paketit esim.:
#   pip install pandas scipy openpyxl
#
import sys
import pandas as pd
import scipy.stats as stats

def tee_t_test(df: pd.DataFrame):
    """
    Tehtävä 1: vertaillaan kulttuuri- ja tekniikka-opiskelijoita t-testillä
    sarakkeessa 'Opinnäytetyön tekemisaika...' (työviikkoina).
    Tulostaa ryhmien keskiarvot, 95 % luottamusvälit, Levene-testin ja t-testin
    sekä johtopäätökset.
    """
    # Korjattu sarakenimi:
    sarake = "Opinnäytetyön tekemisaika työviikkoina (40 h) aihekuvauksen tekemisestä työn valmistumiseen:työviikkoa"
    alaryhma = "Opiskeluala"
    
    if sarake not in df.columns or alaryhma not in df.columns:
        print(f"VIRHE: Tehtävä 1: Sarake '{sarake}' tai '{alaryhma}' puuttuu tiedostosta.")
        return
    
    df1 = df.dropna(subset=[sarake, alaryhma]).copy()
    kult = df1[df1[alaryhma].str.lower() == "kulttuuri"][sarake].astype(float)
    teki = df1[df1[alaryhma].str.lower() == "tekniikka"][sarake].astype(float)
    
    if len(kult) == 0 or len(teki) == 0:
        print("VIRHE: Tehtävä 1: Ei löytynyt dataa joko kulttuuri- tai tekniikka-ryhmästä.")
        return
    
    def laske_95_ci(series):
        n = len(series)
        mean = series.mean()
        sem = stats.sem(series, nan_policy='omit')
        t_95 = stats.t.ppf(0.975, df=n-1)
        delta = t_95 * sem
        return mean, mean - delta, mean + delta
    
    kult_mean, kult_ci_low, kult_ci_high = laske_95_ci(kult)
    teki_mean, teki_ci_low, teki_ci_high = laske_95_ci(teki)
    
    print("=== TEHTÄVÄ 1: t-test (Kulttuuri vs. Tekniikka) ===\n")
    print(f"Kulttuuri: n = {len(kult)}, keskiarvo = {kult_mean:.2f}, 95 % CI = ({kult_ci_low:.2f}, {kult_ci_high:.2f})")
    print(f"Tekniikka: n = {len(teki)}, keskiarvo = {teki_mean:.2f}, 95 % CI = ({teki_ci_low:.2f}, {teki_ci_high:.2f})\n")
    
    levene_stat, levene_p = stats.levene(kult, teki, center='mean')
    print(f"Levene-test: stat = {levene_stat:.4f}, p = {levene_p:.4f}")
    if levene_p < 0.05:
        print("→ Varianssit eivät ole homogeeniset (p < 0.05). Käytetään t-testissä equal_var=False.\n")
        equal_var = False
    else:
        print("→ Varianssit ovat homogeeniset (p ≥ 0.05). Käytetään t-testissä equal_var=True.\n")
        equal_var = True
    
    t_stat, p_val = stats.ttest_ind(kult, teki, equal_var=equal_var, nan_policy='omit')
    print("t-test:")
    print(f"  testisuure t = {t_stat:.4f}, p = {p_val:.4f}")
    print("  Nollahypoteesi: 'Kulttuuri- ja tekniikka- ryhmien opinnäytetyön tekemisaika ei eroa'\n")
    if p_val < 0.05:
        print("  → P‐arvo < 0.05, hylätään nollahypoteesi: ryhmien välillä on tilastollisesti merkitsevä ero.")
    else:
        print("  → P‐arvo ≥ 0.05, ei voida hylätä nollahypoteesia: ryhmien välillä ei ole tilastollisesti merkitsevää eroa.")
    
    print("\nSanalliset johtopäätökset:")
    if p_val < 0.05:
        print("- Kulttuuri- ja tekniikkaopiskelijoiden opinnäytetyön tekemiseen kulunut aika eroaa tilastollisesti merkitsevästi (alpha=0.05).")
    else:
        print("- Kulttuuri- ja tekniikkaopiskelijoiden opinnäytetyön tekemiseen kulunut aika ei eroa tilastollisesti merkitsevästi (alpha=0.05).")
    print("\n" + "="*60 + "\n")


def tee_mannwhitney(df: pd.DataFrame):
    """
    Tehtävä 2: vertaillaan kulttuuri- ja liiketalous-opiskelijoita Mann-Whitney U -testillä
    sarakkeessa 'Hyödyllisyys: Seminaarit'. Jos saraketta ei löydy, tulostetaan huomautus.
    """
    sarake = "Hyödyllisyys: Seminaarit"
    alaryhma = "Opiskeluala"
    
    if sarake not in df.columns or alaryhma not in df.columns:
        print(f"HUOM: Tehtävä 2: Sarake '{sarake}' tai '{alaryhma}' puuttuu tiedostosta. Skippaan Tehtävä 2:n.\n")
        return
    
    df2 = df.dropna(subset=[sarake, alaryhma]).copy()
    kult = df2[df2[alaryhma].str.lower() == "kulttuuri"][sarake].astype(float)
    liik = df2[df2[alaryhma].str.lower() == "liiketalous"][sarake].astype(float)
    
    if len(kult) == 0 or len(liik) == 0:
        print("Huom: Tehtävä 2: Ei löytynyt dataa joko kulttuuri- tai liiketalous-ryhmästä. Skippaan Tehtävä 2:n.\n")
        return
    
    kult_mean = kult.mean()
    liik_mean = liik.mean()
    
    print("=== TEHTÄVÄ 2: Mann-Whitney U (Kulttuuri vs. Liiketalous) ===\n")
    print(f"Kulttuuri: n = {len(kult)}, keskiarvo = {kult_mean:.2f}")
    print(f"Liiketalous: n = {len(liik)}, keskiarvo = {liik_mean:.2f}\n")
    
    u_stat, p_val = stats.mannwhitneyu(kult, liik, alternative='two-sided')
    print("Mann-Whitney U -testi:")
    print(f"  U = {u_stat:.4f}, p = {p_val:.4f}")
    print("  Nollahypoteesi: 'Kulttuuri- ja liiketalouden opiskelijoiden seminaarien hyödyllisyyden arviot eivät eroa jakaumiltaan'\n")
    if p_val < 0.05:
        print("  → P‐arvo < 0.05, hylätään nollahypoteesi: ryhmien välillä on tilastollisesti merkitsevä ero.")
    else:
        print("  → P‐arvo ≥ 0.05, ei voida hylätä nollahypoteesia: ryhmien välillä ei ole tilastollisesti merkitsevää eroa.")
    
    print("\nSanalliset johtopäätökset:")
    if p_val < 0.05:
        print("- Kulttuuri- ja liiketalouden opiskelijoiden arviot seminaarien hyödyllisyydestä eroavat tilastollisesti merkitsevästi (alpha=0.05).")
    else:
        print("- Kulttuuri- ja liiketalouden opiskelijoiden arviot seminaarien hyödyllisyydestä eivät erotu tilastollisesti merkitsevästi (alpha=0.05).")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    excel_path = "D:/GitHub/PythonDataAnalytics/doc/Opinnäytetyökysely.xlsx"
    try:
        df = pd.read_excel(excel_path, sheet_name=0)
    except Exception as e:
        print(f"VIRHE: Excel‐tiedoston lukeminen epäonnistui: {e}", file=sys.stderr)
        sys.exit(1)
    
    print("Ladatut sarakkeet:", df.columns.tolist(), "\n")
    
    tee_t_test(df)
    tee_mannwhitney(df)
    
    print("Tehtävä 8 suoritettu.")
