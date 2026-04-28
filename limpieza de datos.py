import pandas as pd

df = pd.read_excel(
    "data/Educacion_05.xlsx", 
    skiprows=7, 
    usecols="A:B",
    header=None,
    names=["estado", "escolaridad"]
)

# 1. Eliminar fila nacional 
df = df[df["estado"] != "Estados Unidos Mexicanos"]

# 2. Eliminar toda la "basura" del final (fuentes, notas, definiciones)
df = df.dropna(subset=["escolaridad"])

# 3. Resetear el índice para que quede limpio
df = df.reset_index(drop=True)

print(df)

df.to_csv("data/escolaridad.csv", index=False)