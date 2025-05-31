# task6.py
# --------
# 1) Fetch “Kokonaishedelmällisyysluku” (Total fertility rate) for all years 1776–2024
#    via PX-Web JSON-stat2 from:
#      https://pxdata.stat.fi/PxWeb/api/v1/fi/StatFin/synt/statfin_synt_pxt_12dt.px
# 2) Convert JSON-stat2 into a pandas DataFrame.
# 3) Print the DataFrame (top 10 rows).
# 4) Draw three different chart types (line, bar, pie) and save them.

import requests
import pandas as pd
import matplotlib.pyplot as plt
import sys
import json


# -----------------------------------------------
# 1) WORKING PX-WEB URL
# -----------------------------------------------
PXWEB_URL = (
    "https://pxdata.stat.fi/PxWeb/api/v1/fi/StatFin/"
    "synt/statfin_synt_pxt_12dt.px"
)

# -----------------------------------------------
# 2) COPY-PASTE the “Vuosi” index EXACTLY from metadata
#    This array runs from 1776 through 2024.
# -----------------------------------------------
all_years = [
    "1776","1777","1778","1779","1780","1781","1782","1783","1784","1785","1786","1787","1788","1789","1790","1791","1792","1793","1794","1795","1796","1797","1798","1799","1800","1801","1802","1803","1804","1805","1806","1807","1808","1809","1810","1811","1812","1813","1814","1815","1816","1817","1818","1819","1820","1821","1822","1823","1824","1825","1826","1827","1828","1829","1830","1831","1832","1833","1834","1835","1836","1837","1838","1839","1840","1841","1842","1843","1844","1845","1846","1847","1848","1849","1850","1851","1852","1853","1854","1855","1856","1857","1858","1859","1860","1861","1862","1863","1864","1865","1866","1867","1868","1869","1870","1871","1872","1873","1874","1875","1876","1877","1878","1879","1880","1881","1882","1883","1884","1885","1886","1887","1888","1889","1890","1891","1892","1893","1894","1895","1896","1897","1898","1899","1900","1901","1902","1903","1904","1905","1906","1907","1908","1909","1910","1911","1912","1913","1914","1915","1916","1917","1918","1919","1920","1921","1922","1923","1924","1925","1926","1927","1928","1929","1930","1931","1932","1933","1934","1935","1936","1937","1938","1939","1940","1941","1942","1943","1944","1945","1946","1947","1948","1949","1950","1951","1952","1953","1954","1955","1956","1957","1958","1959","1960","1961","1962","1963","1964","1965","1966","1967","1968","1969","1970","1971","1972","1973","1974","1975","1976","1977","1978","1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024"
]

# -----------------------------------------------
# 3) JSON-stat2 Payload: request all_years & Tiedot = ["tfr"]
#    (Note the dimension name is now "Tiedot", not "Tieto".)
# -----------------------------------------------
query_payload = {
    "query": [
        {
            "code": "Vuosi",
            "selection": {
                "filter": "item",
                "values": all_years
            }
        },
        {
            "code": "Tiedot",                 # <-- CORRECTED HERE
            "selection": {
                "filter": "item",
                "values": ["tfr"]
            }
        }
    ],
    "response": {
        "format": "json-stat2"
    }
}


def fetch_pxweb_data(url: str, payload: dict) -> pd.DataFrame:
    """
    Sends a POST to PXWEB_URL with the JSON payload,
    then parses the JSON-stat2 response into a pandas DataFrame
    with columns ['Year', 'Indicator', 'FertilityRate'].

    If the returned JSON does not contain "dataset", print out the entire JSON/text
    for debugging and exit.
    """
    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
    except requests.RequestException as e:
        # HTTP‐level errors (404, 400, etc.) are caught here.
        if hasattr(e, "response") and e.response is not None:
            print("\n=== RESPONSE TEXT ===\n", e.response.text, file=sys.stderr)
        print("ERROR: Failed to fetch data:", e, file=sys.stderr)
        sys.exit(1)

    # Try to parse JSON
    text = resp.text.strip()

    # If the response is empty, that’s not valid JSON-stat2
    if len(text) == 0:
        print("\n=== RESPONSE WAS EMPTY ===\n", file=sys.stderr)
        sys.exit(1)

    try:
        json_data = resp.json()
    except ValueError:
        # Not valid JSON—maybe HTML or plain text?
        print("\n=== RESPONSE IS NOT JSON (raw text below) ===\n", text, file=sys.stderr)
        sys.exit(1)

    # If "dataset" is not a key, then it’s not the JSON-stat2 we expect
    if "dataset" not in json_data:
        print(
            "\n=== JSON did not contain 'dataset'. Full JSON below: ===\n",
            json.dumps(json_data, ensure_ascii=False, indent=2),
            file=sys.stderr
        )
        sys.exit(1)

    ds = json_data["dataset"]
    dims = ds["dimension"]

    # dims.keys() should be {'Vuosi','Tiedot','value'}
    dim_keys = [k for k in dims.keys() if k != "value"]  # -> ['Vuosi','Tiedot']

    # 1) For each dimension, grab the "index" array:
    index_lists = [dims[key]["category"]["index"] for key in dim_keys]
    #    dims['Vuosi']['category']['index'] == all_years
    #    dims['Tiedot']['category']['index'] == ['tfr']

    # 2) Build a MultiIndex from the Cartesian product of those two lists:
    mindex = pd.MultiIndex.from_product(index_lists, names=dim_keys)

    # 3) Flatten the "value" array (length = len(all_years) * 1)
    values = ds["value"]

    # 4) Create a DataFrame, then rename columns:
    df = pd.DataFrame({"Value": values}, index=mindex).reset_index()
    df = df.rename(columns={
        "Vuosi": "Year",
        "Tiedot": "Indicator",
        "Value": "FertilityRate"
    })

    return df


if __name__ == "__main__":
    # --------------------------------------------------
    # 1) Fetch & build DataFrame
    # --------------------------------------------------
    df_fertility = fetch_pxweb_data(PXWEB_URL, query_payload)

    # --------------------------------------------------
    # 2) Print the DataFrame (top 10 rows)
    # --------------------------------------------------
    pd.set_option("display.max_rows", 10)
    pd.set_option("display.max_columns", None)
    print("\n=== Sample of the Fertility DataFrame (Top 10 rows) ===\n")
    print(df_fertility.head(10))
    print("\n(total rows returned = {})\n".format(len(df_fertility)))
    # You should see 249 rows (one for each year 1776…2024), all with Indicator='tfr'.

    # --------------------------------------------------
    # 3) Draw three different chart types
    # --------------------------------------------------

    # —— a) LINE PLOT: Fertility Rate over Time (1776–2024) ——
    df_line = df_fertility.copy()
    df_line["Year_dt"] = pd.to_datetime(df_line["Year"], format="%Y")
    df_line = df_line.sort_values("Year_dt")

    plt.figure(figsize=(10, 5))
    plt.plot(
        df_line["Year_dt"],
        df_line["FertilityRate"],
        marker="o",
        linestyle="-"
    )
    plt.title("Finland: Total Fertility Rate (1776–2024)")
    plt.xlabel("Year")
    plt.ylabel("Fertility Rate")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("fertility_rate_trend_line.png")
    plt.show()

    # —— b) BAR PLOT: Last 10 years (2015–2024) ——
    years_subset = [str(y) for y in range(2015, 2025)]
    df_bar = df_fertility[df_fertility["Year"].isin(years_subset)]

    plt.figure(figsize=(8, 4))
    plt.bar(df_bar["Year"], df_bar["FertilityRate"])
    plt.title("Fertility Rate by Year (Finland, 2015–2024)")
    plt.xlabel("Year")
    plt.ylabel("Fertility Rate")
    for i, val in enumerate(df_bar["FertilityRate"]):
        plt.text(i, val + 0.01, f"{val:.3f}", ha="center")
    plt.tight_layout()
    plt.savefig("fertility_rate_by_year_bar.png")
    plt.show()

    # —— c) PIE CHART: Share of Total Fertility (split into three centuries) ——
    buckets = {
        "18th Century (1776–1799)": [str(y) for y in range(1776, 1800)],
        "19th Century (1800–1899)": [str(y) for y in range(1800, 1900)],
        "20th Century (1900–1999)": [str(y) for y in range(1900, 2000)],
        "21st Century (2000–2024)": [str(y) for y in range(2000, 2025)]
    }
    bucket_sums = []
    bucket_labels = []
    for label, years_list in buckets.items():
        mask = df_fertility["Year"].isin(years_list)
        total_for_bucket = df_fertility.loc[mask, "FertilityRate"].sum()
        bucket_sums.append(total_for_bucket)
        bucket_labels.append(label)

    plt.figure(figsize=(7, 7))
    plt.pie(
        bucket_sums,
        labels=bucket_labels,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"edgecolor": "k"}
    )
    plt.title("Share of Total Fertility Rate by Century (Finland 1776–2024)")
    plt.tight_layout()
    plt.savefig("fertility_rate_century_buckets_pie.png")
    plt.show()

    print(
        "\nCharts have been saved as:\n"
        "  • fertility_rate_trend_line.png\n"
        "  • fertility_rate_by_year_bar.png\n"
        "  • fertility_rate_century_buckets_pie.png\n"
    )
