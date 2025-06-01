# Lopputehtävä: To-Do-lista

Alla on yksityiskohtainen to-do-lista, joka kattaa sekä **Suunnittelu-osion** että **Toteutus-osion** vaatimukset. Käytä tätä listaa ohjenuorana, kun suunnittelet ja toteutat lopputehtävän.

---

## 1. Suunnittelu

1. **Datan valinta ja kuvaus**  
   - [ ] Valitse analysoitava datalähde (esim. avoin julkinen data, yrityksen sisäinen aineisto tms.).  
   - [ ] Varmista, että datassa on riittävästi rivejä ja muuttujia korrelaatio- ja tilastollisten testien suorittamiseen.  
   - [ ] Kirjoita lyhyt kuvaus:
     - Mitä dataa analysoidaan (taustatiedot, lähde).  
     - Miksi tämä data on kiinnostavaa (esim. liiketoiminnallinen/akateeminen konteksti).  

2. **Tavoitteiden ja tutkimuskysymysten määrittely**  
   - [ ] Muotoile selkeästi lopputyön päämäärä(t):  
     - Mitä datasta halutaan selvittää?  
     - Mitä konkreettista tulosta tavoittelet (esim. trendianalyysi, korrelaatiot, ryhmien vertailu)?  
   - [ ] Kirjaa ylös vähintään yksi (tai useampi) tutkimuskysymys:  
     - Esim. “Onko muuttujien A ja B välillä tilastollisesti merkitsevää yhteyttä?”  
     - Esim. “Miten muuttujat C–D poikkeavat eri ryhmien välillä?”  

3. **Datan käsittely- ja analyysisuunnitelma**  
   - [ ] Kuvaile tarvittavat toimenpiteet datan etukäsittelyyn:  
     - Tarvittaessa useiden tiedostojen yhdistäminen (merge/join) tai ristiintaulukointi.  
     - Puuttuvien arvojen käsittely (poisto, täyttö keskiarvolla tms.).  
     - Uusien muuttujien luonti (esim. yhdistä olemassa olevista sarakkeista).  
     - Muuttujien uudelleennimeäminen, formaattimuunnokset (päivämäärät, numerot).  
   - [ ] Määritä tilastolliset menetelmät ja visualisoinnit, joita aiot käyttää:  
     - Korrelaatiolaskenta (Pearson, Spearman tai muu).  
     - Tilastolliset testit (t-testi, Mann–Whitney, chi-neliö tms.) ryhmävertailuihin.  
     - Aikasarja-analyysi (trendit, kausivaihtelut) ja ennuste (esim. Holt-Winters, ARIMA).  
     - Riippuvuuksien visualisointi (scatterplot, boxplot).  
     - Yhteenvetokuvioita (histogrammi, viivakaavio, pylväsdiagrammi).  

4. **Suunnitelman dokumentointi**  
   - [ ] Kirjoita suunnitelma vapaamuotoisesti (Moodle-kenttään):
     1. Data ja sen lähde.  
     2. Tutkimuskysymykset ja tavoitteet selkeästi.  
     3. Käsittelyvaiheet ja niiden perustelut (miksi oletat kunkin vaiheen tarpeelliseksi).  
   - [ ] Varmista, että suunnitelmasta käy ilmi, miksi jokainen vaihe tehdään (esim. puuttuvien arvojen vaikutus analyysiin, korrelaatioiden merkitys päätöksenteossa).  
   - [ ] Lähetä suunnitelma ohjaajalle hyväksyttäväksi ennen toteutuksen aloittamista.  

---

## 2. Toteutus

1. **Projektin alustus ja kansiorakenne**  
   - [ ] Luo paikallinen git-repo (tai varmista, että projektihakemisto on versionhallinnassa).  
   - [ ] Luo kansiorakenne:
     ```
     /projektin-juuri
       ├─ data/               # Raw-data (Excel/CSV/tms.)
       ├─ notebooks/          # Jupyter Notebookit (Suunnitelma, Analyysi)
       ├─ scripts/            # Valmiit .py-skriptit (data-lataus, pkt, testit)
       ├─ output/             # Tallennetut kuvat (png/pdf), taulukot (csv)
       ├─ raportti/           # Savonia-pohjainen raportti (Word/LaTeX)
       └─ requirements.txt    # Python-kirjastot (pandas, numpy, scipy, matplotlib, statsmodels, jne.)
     ```
   - [ ] Luo virtuaaliympäristö ja tallenna asennetut paketit `requirements.txt`-tiedostoon:
     ```bash
     python -m venv .venv
     source .venv/bin/activate      # Windows: .venv\Scripts\activate
     pip install pandas numpy scipy matplotlib seaborn statsmodels openpyxl
     pip freeze > requirements.txt
     ```

2. **Datan lataus ja esikatselu**  
   - [ ] Tee Python-skripti tai Notebook-solut, jotka lukevat alkuperäiset tiedostot (Excel/CSV) kansiosta `/data`.  
   - [ ] Tulosta DataFramen `head()`, `tail()`, sarakenimet ja `dtypes` varmistaaksesi, että tiedot latautuvat oikein.  
   - [ ] Tallenna esikatselulistat lokiin tai Notebook-näyttöön.

3. **Datan puhdistus ja muunnokset**  
   - [ ] Tarkista ja poista tai korvaa puuttuvat arvot (esim. `df.dropna()`, `df.fillna()`).  
   - [ ] Muokkaa tai poista virheelliset havainnot (epätodelliset luvut, outlierit).  
   - [ ] Tarvittaessa luo uusi muuttuja yhdistämällä tai muokkaamalla vanhoja (esim. päivämäärä → vuosi/kk-erottelu).  
   - [ ] Tallennettava siivottu data: tallenna puhdistettu DataFrame csv-tiedostona `/output/cleaned_data.csv`.

4. **Kuvaajien piirtäminen**  
   - [ ] Piirrä vähintään kolme erilaista kaaviota, jotka tukevat tutkimuskysymyksiä:
     1. **Histogrammi** keskeiselle numeeriselle muuttujalle (esim. jakauman tarkastelu).  
     2. **Viivakaavio** jos data on aikasarjamuotoa, tai trendin esittäminen ajan suhteen.  
     3. **Pylväsdiagrammi / boxplot** ryhmävertailuihin (esim. mediaaniarvot eri kategorioissa).  
     4. **Scatterplot ja korrelaatiolaskelma** kahden muuttujan välille (riippuvuuden selvittäminen).
   - [ ] Aseta kaikille kaavioille selkeät otsikot, x- ja y-akselien nimet sekä legendat tarvittaessa.  
   - [ ] Tallenna kuvat `/output/`-kansioon esimerkiksi PNG- tai PDF-muodossa:
     ```
     output/
       ├─ hist_numeerinen.png
       ├─ viivakaavio_aikasarja.png
       ├─ boxplot_ryhmat.png
       └─ scatter_korrelaatio.png
     ```

5. **Tilastolliset analyysit**  
   - [ ] **Korrelaation laskeminen**: valitse kaksi numeerista muuttujaa ja laske Pearsonin tai Spearmanin korrelaatiokerroin.
     ```python
     corr_coef, corr_p = stats.pearsonr(df["muuttuja1"], df["muuttuja2"])
     ```
   - [ ] **Ryhmävertailutestit**:
     - Tarvittaessa jaa aineisto kahteen ryhmään (esim. opiskeluala, sukupuoli).
     - **t-testi** (independent‐samples) tai **Mann–Whitney U** tilanteen mukaan (normaalijakauma vs. ei-parametrinen).  
       ```python
       t_stat, p_val = stats.ttest_ind(df_group1["arvo"], df_group2["arvo"], equal_var=False)
       ```
     - **Chi-neliö-testi** kategoriseen muuttujaan, jos sopii:
       ```python
       chi2, p, dof, expected = stats.chi2_contingency(table)
       ```
   - [ ] **Tilastolliset johtopäätökset**:
     - Tulkitse testien p-arvot ja tee selkeät johtopäätökset (p < 0.05 ⇒ merkitsevä ero/riippuvuus).  
     - Kirjaa jokaisen testin nollahypoteesi ja tulos lyhyesti pysyväiseen lokiin tai Notebookiin.

6. **Yhteenvetona DataFrame-taulukot**  
   - [ ] Luo tarvittaessa tiivistävä DataFrame-taulukko, jossa esitetään keskiarvot, mediaanit, hajonnat ryhmittäin.  
   - [ ] Tallenna tämä taulukko CSV-muodossa (esim. `/output/summary_table.csv`) ja liitä raporttiin.

7. **Raportin kirjoittaminen (Savonia-pohja)**  
   - [ ] Aloita Savonia-raporttipohjan lataminen (Word/LaTeX).  
   - [ ] **Johdanto**:  
     - Esittele tutkittava data ja tutkimuskysymykset.  
     - Perustele, miksi valitsit kyseisen aineiston ja minkälaisia tuloksia odotat.  
   - [ ] **Menetelmät**:  
     - Kuvaile, miten dataa siivottiin ja mikä oli analyysiprosessi.  
     - Luettele käyttämäsi tilastolliset menetelmät ja niiden perustelut.  
   - [ ] **Tulokset**:  
     - Liitä Notebookista kaaviot ja taulukot PDF-kuvina raporteille.  
     - Kerro selkeästi, mitä kussakin kuvassa/taulukossa näkyy.  
     - Esitä numerot (keskiarvot, p-arvot, korrelaatiot) ja niiden tulkinnat.  
   - [ ] **Johtopäätökset**:  
     - Yhteenveto tärkeimmistä löydöksistä.  
     - Mitä nämä tulokset kertovat ja miten niitä voisi hyödyntää päätöksenteossa.  
   - [ ] **Liite**:  
     - Liitä kokonaiset Python-koodit (Notebook-versio liitteenä).  
     - Huolehdi, että koodi on kommentoitua ja luettavaa.  
   - [ ] Tarkista raportin **luettavuus, johdonmukaisuus** ja varmista, että kaikki kuvat, taulukot ja koodiliitteet ovat mukana.

8. **Lopputarkistus ja palautus**  
   - [ ] Varmista, että sekä suunnittelu- että toteutusosio (raportti + koodiliite) on tallennettu PDF- ja/tai Word-muodossa Moodleen.  
   - [ ] Tarkista, että kuvat on tallennettu `/output/`-hakemistoon ja sisällytetty raporttiin.  
   - [ ] Tee viimeinen tarkistusversionhallinnan avulla (git commit ja git push, jos käytät GitHubia).  

---

### Aikataulu-ehdotus (esimerkki)

1. **Viikko 1–2**  
   - Datan valinta ja suunnittelun kirjoittaminen.  
   - Palauta suunnitelma hyväksyttäväksi.

2. **Viikko 3–4**  
   - Toteuta datan lataus, siivous ja röyhväkuviot.  
   - Tee ensimmäiset tilastolliset testit ja visualisoinnit.

3. **Viikko 5**  
   - Kirjoita raportin luonnos (Johdanto, Menetelmät, Ensitulokset).  
   - Hio visualisoinnit ja varmista kaavioiden laatu julkaisuun.

4. **Viikko 6**  
   - Viimeistele raportin Tulokset ja Johtopäätökset.  
   - Liitä koodiliite ja tarkista, että kaikki osiot ovat mukana.  
   - Palauta lopullinen PDF/Word.

---

Tämä to-do-lista auttaa pitämään työvaiheet järjestyksessä ja varmistaa, että kaikki **Suunnittelu­­­­** ja **Toteutus­­­­** -osion vaatimuslistan kohdat tulevat katetuiksi ja dokumentoiduiksi. Onnea tehtävän tekoon!
