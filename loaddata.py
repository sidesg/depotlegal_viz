import pandas as pd

def main() -> None:

    dqdata= load_data()

    data = socprods_explode(dqdata)
    data = data.groupby(["societe_production", "types_element"], as_index=False).size()
    
    data.to_csv("test.csv")


def load_data() -> pd.DataFrame:
    """Reads Données Québec dataset and returns raw Dataframe"""

    dqcpath = 'https://www.donneesquebec.ca/recherche/dataset/e749fe3c-de61-4ab4-809d-a3dd8a160009/resource/68121e4c-b042-4a81-9249-85c8ea7110f0/download/depot-legal.csv'

    df = pd.read_csv(dqcpath)
    df["year"] = pd.DatetimeIndex(df["date_reception"]).year

    return df

def typele_peryear(data: pd.DataFrame) -> pd.DataFrame:
    """Return Dataframe with counts of works received grouped
    by year then by type d'élément"""

    data = data.groupby(["year", "types_element"], as_index=False).size()

    return data

def typele_uniqes(data: pd.DataFrame) -> list:
    """Return a list of types d'élément received on more than one year"""
    
    data = data[data["date_reception"].notna()]

    return sorted([
        d for d in data["types_element"].unique()
        if len(data[data["types_element"] == d]["year"].unique()) > 1
    ])

def unique_socprods(df: pd.DataFrame) -> list:
    # data = df.copy()
    data = df["societe_production"].dropna()

    data = data.apply(lambda x : x.split(";")).explode()

    data = data.apply(lambda x : x.strip())

    #TODO : remove parentheses with regex?
    
    return sorted(data.unique())

def socprods_explode(df: pd.DataFrame) -> pd.DataFrame:
    # data.dropna(subset=["societe_production"], inplace=True)
    data = df.copy()
    data["societe_production"] = data["societe_production"].apply(lambda x : str(x).split(";"))

    data = data.explode("societe_production")

    data["societe_production"] = data["societe_production"].apply(lambda x: x.strip())

    return data


if __name__ == "__main__":
    main()