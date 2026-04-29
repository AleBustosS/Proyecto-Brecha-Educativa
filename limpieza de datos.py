import pandas as pd

df = pd.read_excel(
    "data/Educacion_05.xlsx", 
    skiprows=7, 
    usecols="A:B",
    header=None,
    names=["estado", "escolaridad"]
)


df = df[df["estado"] != "Estados Unidos Mexicanos"]


df = df.dropna(subset=["escolaridad"])


df = df.reset_index(drop=True)

print(df)

df.to_csv("data/escolaridad.csv", index=False)