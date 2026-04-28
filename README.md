# 📊 Brecha Educativa en México

## 🧠 Descripción del proyecto

Este proyecto analiza la **desigualdad educativa en México** a partir del *grado promedio de escolaridad por entidad federativa*.

La aplicación está desarrollada con **Dash (Plotly)** y permite visualizar:

- 📌 El nivel educativo por estado  
- 📌 La brecha respecto al promedio nacional  
- 📌 La distribución geográfica de la educación  
- 📌 Comparación interactiva entre estados  

---

## 🎯 Pregunta de investigación

> **¿Dónde naces determina tu acceso a la educación en México?**

---

## 📂 Estructura del proyecto

Proyecto/
│
├── app.py
├── limpieza_de_datos.py
├── data/
│ ├── escolaridad.csv
│ ├── Educacion_05.xlsx
│ └── mexico.json
│
├── assets/
│ └── styles.css
│
└── README.md
---

## 📊 Datos utilizados

Los datos provienen de fuentes oficiales:

- INEGI (2020): Grado promedio de escolaridad por entidad federativa  
- GeoJSON: Límites territoriales de México  

---

## ⚙️ Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instalado:

- Python 3.9+
- pip

Instala las dependencias:

```bash
pip install dash pandas plotly