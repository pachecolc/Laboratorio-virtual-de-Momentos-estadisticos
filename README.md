# Laboratorio virtual: Momentos estadísticos y medidas descriptivas

Aplicación interactiva en **Python + Streamlit + Plotly** para explorar centralidad, dispersión, cuantiles y boxplots mediante manipulación controlada de datos.

## Objetivo
Permitir que el estudiante formule una predicción, modifique una condición, observe cómo cambian las medidas descriptivas, registre resultados y construya una interpretación estadística.

## Fundamento científico
La app implementa las medidas trabajadas en la presentación `Momentos.pptx`:

- media como primer momento;
- varianza poblacional como segundo momento central;
- desviación estándar;
- mediana;
- cuartiles Q1 y Q3;
- rango intercuartílico (IQR);
- boxplot y detección descriptiva de valores atípicos mediante la regla 1.5·IQR.

La varianza se calcula con `ddof=0`, en coherencia con el código de la presentación.

## Modelo matemático

\[
\bar{x}=\frac{1}{N}\sum_{i=1}^{N}x_i
\]

\[
\sigma^2=\frac{1}{N}\sum_{i=1}^{N}(x_i-\bar{x})^2,\qquad \sigma=\sqrt{\sigma^2}
\]

La app permite tres condiciones didácticas:

1. **Sin transformación**: se conserva el conjunto original.
2. **Escala y desplazamiento**: \(x'=a x+b\).
3. **Dispersión con media constante**: \(x'=\bar{x}+k(x-\bar{x})\).

Además, puede añadirse un valor extremo para estudiar la sensibilidad de media, mediana y boxplot.

## Variables

| Variable | Tipo | Rango/interfaz | Función |
|---|---|---|---|
| Fuente de datos | Independiente | Presentación / manual / CSV-TXT | Define el conjunto de referencia |
| Factor de escala `a` | Independiente | 0.25–3.00 | Reescala los valores |
| Desplazamiento `b` | Independiente | -10–10 | Traslada los valores |
| Factor `k` | Independiente | 0.25–3.00 | Modifica dispersión conservando la media |
| Valor extremo | Independiente | Entrada numérica | Evalúa sensibilidad a outliers |
| Media, varianza, σ, mediana, Q1, Q3, IQR | Dependientes | Calculadas | Resumen descriptivo |

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución local

```bash
streamlit run app.py
```

## Estructura

```text
simulador_momentos_estadisticos/
├── app.py
├── requirements.txt
├── README.md
├── GUIA_LABORATORIO.md
├── VALIDACION.md
├── .gitignore
├── assets/
│   └── .gitkeep
├── models/
│   ├── __init__.py
│   └── estadistica.py
└── utils/
    ├── __init__.py
    └── exportacion.py
```

Para mostrar el logo del curso/proyecto, copie la imagen como `assets/logo_serendipia.png`. Si no existe, la app continúa funcionando.

## Uso para estudiantes

1. Seleccione la fuente de datos.
2. Formule una predicción sobre media y varianza.
3. Elija una manipulación.
4. Pulse **Aplicar simulación**.
5. Compare referencia y condición actual.
6. Realice un cálculo manual cuando corresponda.
7. Pulse **Registrar medición**.
8. Descargue CSV o Excel al finalizar.

## Despliegue en Streamlit Community Cloud

1. Cree un repositorio en GitHub y suba el contenido de esta carpeta.
2. En Streamlit Community Cloud seleccione **Create app**.
3. Configure:
   - Repository: su repositorio de GitHub
   - Branch: `main`
   - Main file: `app.py`
4. Despliegue la aplicación.

## Limitaciones

- Es un laboratorio de **estadística descriptiva**, no un modelo inferencial.
- La regla 1.5·IQR identifica valores atípicos de forma descriptiva; no demuestra error experimental.
- La app no infiere normalidad a partir de media, mediana o boxplot.
- Los escenarios de escala, desplazamiento y valor extremo son manipulaciones pedagógicas, no datos experimentales adicionales de la presentación.
- El método de Q1/Q3 corresponde a `numpy.percentile` con su configuración por defecto.

## Referencia principal

Material docente: **Momentos Estadísticos y Medidas Descriptivas**, Prof. Leonardo Pacheco-Londoño.
