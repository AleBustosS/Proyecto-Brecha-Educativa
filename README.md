# 📊 Brecha Educativa en México

## 🧠 Descripción del proyecto

Este proyecto analiza la **desigualdad educativa en México**, utilizando como indicador principal el *grado promedio de escolaridad de la población de 15 años y más* por entidad federativa.

A través de una aplicación web interactiva desarrollada con **Dash (Plotly)**, se transforman datos estadísticos en visualizaciones que permiten identificar diferencias regionales, brechas educativas y patrones geográficos entre estados.

La aplicación permite:

- 📌 Visualizar el nivel educativo promedio por estado  
- 📌 Analizar la brecha respecto al promedio nacional  
- 📌 Explorar la distribución geográfica de la educación  
- 📌 Comparar de forma interactiva cualquier estado con el promedio nacional  

---

## 🎯 Pregunta de investigación

> **¿Dónde naces determina tu acceso a la educación en México?**

---

## 📂 Estructura del proyecto
Proyecto/
├── app.py # Aplicación principal (Dash)
├── limpieza_de_datos.py # Script de limpieza de datos
├── data/
│ ├── escolaridad.csv # Dataset limpio
│ ├── Educacion_05.xlsx # Datos originales
│ └── mexico.json # GeoJSON para el mapa
├── assets/
│ └── styles.css # Estilos de la app
└── README.md


---

## 📊 Datos utilizados

- **INEGI (2020)** – Censo de Población y Vivienda  
  https://www.inegi.org.mx/programas/ccpv/2020/  
  Fecha de descarga: 26/04/2026  

- **GeoJSON de México**  
  https://github.com/angelnmara/geojson  

---

## 🧹 Procesamiento de datos

El archivo `limpieza_de_datos.py` se utilizó para:

- Limpiar y estructurar los datos originales  
- Eliminar información irrelevante  
- Generar el dataset final (`escolaridad.csv`)  

---

## 🌐 Aplicación en línea

🔗 https://proyecto-brecha-educativa.onrender.com/

---

## ⚙️ Requisitos

- Python 3.9 o superior  
- pip  

Instalar dependencias:

```bash
pip install dash pandas plotly