import pandas as pd

# Data Loading
DEFAULT_FILE_NAME = "./data/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012.xlsx"

def read_police_data_by_year(year,
                             filename = DEFAULT_FILE_NAME):
    df = pd.read_excel(filename, f"Services PN {year}", header=None)
    df_claims = df[3:].copy()
    df_claims.columns = df[2:3].to_numpy()[0]
    df_claims.index = df_claims.iloc[:, 0]
    df_libelle = df_claims.iloc[:, 1]
    df_claims = df_claims.iloc[:, 2:].transpose()
    
    df_csp = df[:3].copy()
    df_csp.columns = df_csp.iloc[2, :]
    df_csp.index = df_csp.iloc[:, 1]
    df_csp = df_csp.iloc[:, 2:].transpose()

    df_claims = df_claims.merge(df_csp, right_index=True, left_index=True)
    
    return df_claims, df_libelle, df_csp

def read_police_data(filename = DEFAULT_FILE_NAME):
    data = []
    for year in range(2012, 2021):
        df_claims, df_libelle, df_csp = read_police_data_by_year(year)
        df_claims["year"] = year
        data.append(df_claims)
    return pd.concat(data), df_libelle
