# task7.py
# --------
# Tämä skripti toteuttaa Tehtävä 7:n molemmat osat:
#  1) Lentomatkustajadatan aikasarjaennuste (Holt-Winters, 2024 ennuste, hajontakaavio)
#  2) Vuosittaisen kokonaishedelmällisyysluvun (1776–2024) ennuste (Holt-Winters ilman kausikomponenttia, 2025–2034 ennuste, viivakaavio)
#
# Käyttää:
#  • pandas, numpy, matplotlib, seaborn, statsmodels, requests, sys, json
#  • Excel‐lataus: "/mnt/data/lentomatkustajat.xlsx"
#  • PX-Web JSON-stat2: "https://pxdata.stat.fi/PxWeb/api/v1/fi/StatFin/synt/statfin_synt_pxt_12dt.px"
#
# Tallennettavat kuvat:
#  • fertility_2024_scatter.png
#  • fertility_annual_forecast_2034.png
#
import sys
import json
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Visualisointien oletusasetukset
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)

# pandas näyttöasetukset, kun tulostetaan DataFrameja konsoliin
pd.set_option("display.max_rows", 12)
pd.set_option("display.max_columns", None)


def fetch_pxweb_data(url: str, payload: dict) -> pd.DataFrame:
    """
    Lähettää POST-pyynnön PXWEB_URL:ään JSON-payloadilla ja palauttaa
    JSON-stat2-vastauksen pandas DataFrameksi sarakkeilla 
    ['Year', 'Indicator', 'FertilityRate'].
    Käsittelee sekä tapaukset, joissa JSON on "dataset"-avaimen alla,
    että tapauksen missä JSON itse on dataset (class='dataset').
    """
    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        if hasattr(e, "response") and e.response is not None:
            print("\n=== VASTAUS TEKSTINÄ ===\n", e.response.text, file=sys.stderr)
        print("VIRHE: Tietojen haku epäonnistui:", e, file=sys.stderr)
        sys.exit(1)

    text = resp.text.strip()
    if len(text) == 0:
        print("\n=== VASTAUS OLI TYHJÄ ===\n", file=sys.stderr)
        sys.exit(1)

    try:
        json_data = resp.json()
    except ValueError:
        print("\n=== VASTAUS EI OLE JSONIA (raaka teksti alla) ===\n", text, file=sys.stderr)
        sys.exit(1)

    # Tapaus A: JSON on kääritty "dataset"-avaimen alle
    if "dataset" in json_data:
        ds = json_data["dataset"]
    # Tapaus B: JSON itse on dataset (class="dataset")
    elif json_data.get("class") == "dataset":
        ds = json_data
    else:
        print(
            "\n=== JSON EI SISÄLLÄ 'dataset' eikä class='dataset'. Koko JSON alla: ===\n",
            json.dumps(json_data, ensure_ascii=False, indent=2),
            file=sys.stderr
        )
        sys.exit(1)

    dims = ds["dimension"]
    dim_keys = [k for k in dims.keys() if k != "value"]  # esim. ['Vuosi','Tiedot']
    index_lists = [dims[key]["category"]["index"] for key in dim_keys]

    # Rakennetaan MultiIndex kartesiolähteenä
    mindex = pd.MultiIndex.from_product(index_lists, names=dim_keys)

    # Taulukon arvot
    values = ds["value"]

    df = pd.DataFrame({"Value": values}, index=mindex).reset_index()
    df = df.rename(columns={
        "Vuosi": "Year",
        "Tiedot": "Indicator",
        "Value": "FertilityRate"
    })
    return df


if __name__ == "__main__":
    # --------------------------------------------------
    # TEHTÄVÄ 1: Lentomatkustajadatan aikasarjaennuste
    # --------------------------------------------------

    # 1.1) Ladataan Excel‐tiedosto
    excel_path = r"D:\GitHub\PythonDataAnalytics\doc\lentomatkustajat.xlsx"
    try:
        df_all = pd.read_excel(excel_path, sheet_name=0)
    except Exception as e:
        print(f"VIRHE: Excel-tiedoston lukeminen epäonnistui: {e}", file=sys.stderr)
        sys.exit(1)

    print("Ladatut sarakkeet:", df_all.columns.tolist())
    # print(df_all.head())

    # 1.2) Muunnetaan 'Kuukausi' merkkijono datetime‐muotoon ja asetetaan indeksiksi
    df_all["Pvm"] = pd.to_datetime(df_all["Kuukausi"], format="%YM%m")
    df_all = df_all.set_index("Pvm").sort_index()

    # 1.3) Muodostetaan koko aikasarja ts_all
    ts_all = df_all["Matkustajat"].copy()
    ts_all.index.freq = "MS"

    print("\n--- Koko kuukausitasoinen aikasarja (esim. 2019–2024) ---")
    print(ts_all.head(), "\n...", ts_all.tail(), sep="\n")

    # 1.4) Sovitetaan Holt–Winters ‐malli koko aikasarjalle (add trend, add season, period=12)
    try:
        hw_model_all = ExponentialSmoothing(
            ts_all,
            trend="add",
            seasonal="add",
            seasonal_periods=12
        ).fit(optimized=True)
    except ValueError as e:
        print(f"VIRHE Holt-Wintersin sovituksessa: {e}", file=sys.stderr)
        sys.exit(1)

    # 1.5) Ennustetaan vuoden 2024 12 kuukautta
    forecast_2024 = hw_model_all.forecast(12)
    forecast_2024.index = pd.date_range(start="2024-01-01", periods=12, freq="MS")
    forecast_2024.name = "Ennuste2024"

    print("\n--- Ennustetut arvot vuodelle 2024 ---")
    print(forecast_2024.to_frame())

    # 1.6) Suodatetaan vuoden 2024 todelliset tiedot
    ts_2024 = df_all[df_all.index.year == 2024]["Matkustajat"].copy()
    ts_2024.index.freq = "MS"

    print("\n--- Todelliset arvot vuodelle 2024 ---")
    print(ts_2024.to_frame())

    # 1.7) Yhdistetään ennuste ja todelliset samalle DataFrameen, lasketaan erotus
    df_compare = pd.DataFrame({
        "Todellinen2024": ts_2024,
        "Ennuste2024": forecast_2024
    })
    df_compare["Erotus"] = df_compare["Ennuste2024"] - df_compare["Todellinen2024"]

    print("\n--- Vertailu DataFrame (2024) ---")
    print(df_compare)

    # 1.8) Piirretään hajontakaavio: Todellinen vs. Ennustettu 2024
    plt.figure(figsize=(6, 6))
    sns.scatterplot(
        x="Todellinen2024",
        y="Ennuste2024",
        data=df_compare,
        s=50,
        color="tab:blue"
    )
    # Lisätään y=x -viiva
    lims = [
        min(df_compare[["Todellinen2024", "Ennuste2024"]].min()) * 0.9,
        max(df_compare[["Todellinen2024", "Ennuste2024"]].max()) * 1.1
    ]
    plt.plot(lims, lims, ls="--", color="gray")
    plt.xlabel("Todellinen (2024)")
    plt.ylabel("Ennustettu (2024)")
    plt.title("Hajontakaavio: Todellinen vs. Ennustettu (2024)")
    plt.tight_layout()
    plt.savefig("fertility_2024_scatter.png")
    plt.show()

    # --------------------------------------------------
    # TEHTÄVÄ 2: Vuosittaisen kokonaishedelmällisyysluvun ennustaminen
    # --------------------------------------------------

    # 2.1) Asetetaan vuodet 1776–2024 ja PXWeb-osoite
    all_years = [
        "1776","1777","1778","1779","1780","1781","1782","1783","1784","1785","1786","1787","1788","1789","1790","1791","1792","1793","1794","1795","1796","1797","1798","1799",
        "1800","1801","1802","1803","1804","1805","1806","1807","1808","1809","1810","1811","1812","1813","1814","1815","1816","1817","1818","1819",
        "1820","1821","1822","1823","1824","1825","1826","1827","1828","1829","1830","1831","1832","1833","1834","1835","1836","1837","1838","1839",
        "1840","1841","1842","1843","1844","1845","1846","1847","1848","1849","1850","1851","1852","1853","1854","1855","1856","1857","1858","1859",
        "1860","1861","1862","1863","1864","1865","1866","1867","1868","1869","1870","1871","1872","1873","1874","1875","1876","1877","1878","1879",
        "1880","1881","1882","1883","1884","1885","1886","1887","1888","1889","1890","1891","1892","1893","1894","1895","1896","1897","1898","1899",
        "1900","1901","1902","1903","1904","1905","1906","1907","1908","1909","1910","1911","1912","1913","1914","1915","1916","1917","1918","1919",
        "1920","1921","1922","1923","1924","1925","1926","1927","1928","1929","1930","1931","1932","1933","1934","1935","1936","1937","1938","1939",
        "1940","1941","1942","1943","1944","1945","1946","1947","1948","1949","1950","1951","1952","1953","1954","1955","1956","1957","1958","1959",
        "1960","1961","1962","1963","1964","1965","1966","1967","1968","1969","1970","1971","1972","1973","1974","1975","1976","1977","1978","1979",
        "1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999",
        "2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019",
        "2020","2021","2022","2023","2024"
    ]

    PXWEB_URL = (
        "https://pxdata.stat.fi/PxWeb/api/v1/fi/StatFin/"
        "synt/statfin_synt_pxt_12dt.px"
    )

    query_payload_annual = {
        "query": [
            {"code": "Vuosi",  "selection": {"filter": "item", "values": all_years}},
            {"code": "Tiedot", "selection": {"filter": "item", "values": ["tfr"]}}
        ],
        "response": {"format": "json-stat2"}
    }

    # 2.2) Haetaan vuosittainen DataFrame JSON-stat2‐rajapinnasta
    df_annual = fetch_pxweb_data(PXWEB_URL, query_payload_annual)

    # Muunnetaan Year sarake datetime‐indeksiksi
    df_annual["Year_dt"] = pd.to_datetime(df_annual["Year"], format="%Y")
    df_annual = df_annual.set_index("Year_dt").sort_index()

    ts_annual = df_annual["FertilityRate"].copy()
    ts_annual.index.freq = "YS"  # Year Start

    print("\n--- Vuosittainen aikasarja (1776–2024) ---")
    print(ts_annual.head(), "\n...", ts_annual.tail(), sep="\n")

    # 2.3) Sovitetaan Holt-Winters ilman kausikomponenttia (trend="add", seasonal=None)
    hw_model_annual = ExponentialSmoothing(
        ts_annual,
        trend="add",
        seasonal=None,
        seasonal_periods=None
    ).fit(optimized=True)

    # Ennustetaan 10 vuotta (2025–2034)
    forecast_years = 10
    forecast_index = pd.date_range(start="2025-01-01", periods=forecast_years, freq="YS")
    forecast_annual = hw_model_annual.forecast(forecast_years)
    forecast_annual.index = forecast_index
    forecast_annual.name = "EnnusteFertility"

    print("\n--- Ennuste vuosille 2025–2034 ---")
    print(forecast_annual.to_frame())

    # 2.4) Yhdistetään historia ja ennuste DataFrameksi ja piirretään viivakaavio
    df_hist = ts_annual.to_frame(name="HistorianFertility")
    df_fore = forecast_annual.to_frame(name="EnnusteFertility")
    df_full = pd.concat([df_hist, df_fore], axis=0)

    print("\n--- Koottu DataFrame (historia + ennuste) ---")
    print(df_full.head(5), "\n...", df_full.tail(5), sep="\n")

    plt.figure(figsize=(10, 5))
    plt.plot(df_full.index, df_full["HistorianFertility"], label="HistorianFertility")
    plt.plot(df_full.index, df_full["EnnusteFertility"], label="EnnusteFertility", linestyle="--")
    plt.title("Vuosittainen kokonaishedelmällisyysluku (1776–2034)")
    plt.xlabel("Vuosi")
    plt.ylabel("Kokonaishedelmällisyysluku")
    plt.legend()
    plt.tight_layout()
    plt.savefig("fertility_annual_forecast_2034.png")
    plt.show()

    print("\n--- Tehtävä 7 suoritettu: kuvat tallennettu. ---")
