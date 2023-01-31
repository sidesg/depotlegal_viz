import pandas as pd

dqcpath = 'https://www.donneesquebec.ca/recherche/dataset/e749fe3c-de61-4ab4-809d-a3dd8a160009/resource/68121e4c-b042-4a81-9249-85c8ea7110f0/download/depot-legal.csv'

dqdata = pd.read_csv(dqcpath)

def typele_peryear(data: pd.DataFrame) -> pd.DataFrame:
    data["year"]  = pd.DatetimeIndex(data["date_reception"]).year

    data = data.groupby(["year", "types_element"], as_index=False).size()

    return data

def main() -> None:

    df = typele_peryear(dqdata)

    print(type(df))

    print(df[df.types_element.isin(["LTO-5", "LTO-7"])])

if __name__ == "__main__":
    main()