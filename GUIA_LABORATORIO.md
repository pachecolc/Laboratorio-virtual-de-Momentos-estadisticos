# GUÍA DE LABORATORIO VIRTUAL
## Momentos estadísticos y medidas descriptivas

### 1. Datos generales
- **Área temática:** Estadística descriptiva y análisis exploratorio de datos.
- **Nivel:** Universitario introductorio/intermedio.
- **Modalidad:** Laboratorio virtual / análisis computacional.
- **Duración sugerida:** 90–120 min.
- **Aplicación:** Streamlit.

### 2. Introducción
Antes de construir o validar un modelo de inteligencia artificial es necesario describir los datos. La media resume el centro, la varianza y la desviación estándar describen dispersión, la mediana y los cuartiles aportan medidas robustas de posición, y el boxplot integra visualmente varios de estos elementos. En esta práctica se modificará controladamente un mismo conjunto de datos para observar qué medidas cambian y cuáles permanecen estables.

### 3. Objetivos
**Objetivo general:** Analizar el efecto de transformaciones y valores extremos sobre las principales medidas descriptivas de un conjunto de datos.

**Objetivos específicos:**
1. Calcular e interpretar media, varianza, desviación estándar, mediana, Q1 y Q3.
2. Comparar medidas de centralidad y dispersión entre condiciones.
3. Evaluar la sensibilidad de la media y la mediana ante un valor extremo.
4. Interpretar un boxplot y la regla descriptiva 1.5·IQR.
5. Contrastar cálculos manuales con los resultados del simulador.
6. Formular y comprobar predicciones antes de modificar los datos.

### 4. Fundamento teórico
La **media** representa el promedio aritmético de las observaciones. La **varianza poblacional** cuantifica la dispersión cuadrática respecto a la media, mientras que la **desviación estándar** expresa esa dispersión en las mismas unidades de los datos. La **mediana** divide el conjunto ordenado en dos mitades. Los cuartiles Q1 y Q3 delimitan el 50 % central de los datos y permiten calcular el rango intercuartílico, IQR = Q3 − Q1.

El boxplot usa Q1, mediana y Q3. En esta app se señalan como potencialmente atípicos los valores fuera del intervalo Q1 − 1.5·IQR a Q3 + 1.5·IQR.

### 5. Ecuaciones utilizadas
\[
\bar{x}=\frac{1}{N}\sum_{i=1}^{N}x_i
\]

\[
\sigma^2=\frac{1}{N}\sum_{i=1}^{N}(x_i-\bar{x})^2
\]

\[
\sigma=\sqrt{\sigma^2}
\]

\[
IQR=Q_3-Q_1
\]

La app utiliza varianza poblacional (`ddof=0`) y percentiles 25 y 75 mediante NumPy.

### 6. Acceso al laboratorio virtual
**URL de Streamlit:** ________________________________

**Repositorio GitHub:** ________________________________

### 7. Guía de uso
1. Seleccione **Datos de la presentación**.
2. Escriba su predicción sobre la media y la varianza.
3. Seleccione la manipulación indicada por el experimento.
4. Ajuste sus parámetros.
5. Pulse **Aplicar simulación**.
6. Examine las métricas, los datos ordenados y el boxplot.
7. Abra la pestaña **Comparar** para contrastar referencia vs condición actual.
8. Pulse **Registrar medición** después de cada condición.
9. Al finalizar, descargue el archivo CSV o Excel.

### 8. Variables experimentales
| Variable | Símbolo | Unidad | Tipo | Rango | Función |
|---|---|---|---|---|---|
| Factor de escala | a | adimensional | Independiente | 0.25–3.00 | Reescala todos los datos |
| Desplazamiento | b | unidad de los datos | Independiente | -10 a 10 | Traslada todos los datos |
| Factor de dispersión | k | adimensional | Independiente | 0.25–3.00 | Cambia dispersión alrededor de la media |
| Valor extremo | — | unidad de los datos | Independiente | entrada numérica | Evalúa sensibilidad a outliers |
| Media | x̄ | unidad de los datos | Dependiente | calculada | Centralidad |
| Varianza | σ² | unidad² | Dependiente | calculada | Dispersión cuadrática |
| Desv. estándar | σ | unidad de los datos | Dependiente | calculada | Dispersión |
| Mediana | — | unidad de los datos | Dependiente | calculada | Posición robusta |
| Q1, Q3 | — | unidad de los datos | Dependiente | calculada | Posición |

## 9. Experimento 1 — Condición basal
**Objetivo:** Caracterizar el conjunto de datos de la presentación.

**Configuración:**
- Fuente: `Datos de la presentación`.
- Manipulación: `Sin transformación`.
- Valor extremo: desactivado.

**Antes de simular:** ¿espera que media y mediana sean exactamente iguales? Justifique.

**Procedimiento:**
1. Seleccione la configuración anterior.
2. Pulse **Aplicar simulación**.
3. Registre n, media, varianza, σ, mediana, Q1, Q3 e IQR.
4. Interprete el boxplot.
5. Pulse **Registrar medición**.

| Medida | Resultado |
|---|---:|
| n | |
| Media | |
| Varianza | |
| Desv. estándar | |
| Mediana | |
| Q1 | |
| Q3 | |
| IQR | |

## 10. Experimento 2 — Efecto de una traslación
**Objetivo:** Determinar qué medidas cambian al sumar una constante a todos los datos.

**Configuración exacta:**
- Fuente: `Datos de la presentación`.
- Manipulación: `Escala y desplazamiento`.
- `a = 1.00`.
- `b = +3.0`.
- Valor extremo: desactivado.

**Predicción:** Indique qué espera para media, mediana, varianza y desviación estándar.

| Medida | Basal | b = +3 | Cambio |
|---|---:|---:|---:|
| Media | | | |
| Mediana | | | |
| Varianza | | | |
| Desv. estándar | | | |

## 11. Experimento 3 — Misma media, distinta dispersión
**Objetivo:** Modificar la dispersión manteniendo la media del conjunto de referencia.

**Configuración exacta:**
- Fuente: `Datos de la presentación`.
- Manipulación: `Dispersión con media constante`.
- `k = 2.00`.
- Valor extremo: desactivado.

1. Prediga el efecto sobre la media.
2. Prediga el efecto sobre la varianza y σ.
3. Simule y registre.
4. Compare los boxplots de referencia y condición actual.

## 12. Experimento 4 — Valor extremo
**Objetivo:** Comparar la sensibilidad de la media y la mediana.

**Configuración exacta:**
- Fuente: `Datos de la presentación`.
- Manipulación: `Sin transformación`.
- Active `Agregar un valor extremo`.
- Valor extremo: `30`.

| Medida | Sin valor extremo | Con 30 | Cambio absoluto |
|---|---:|---:|---:|
| Media | | | |
| Mediana | | | |
| Varianza | | | |
| IQR | | | |

**Análisis:** ¿qué medida de centralidad fue más resistente al cambio? ¿El boxplot identificó el nuevo valor como atípico?

## 13. Experimento 5 — Escalamiento
**Objetivo:** Analizar el efecto de multiplicar todos los datos por una constante.

**Configuración exacta:**
- Fuente: `Datos de la presentación`.
- Manipulación: `Escala y desplazamiento`.
- `a = 2.00`.
- `b = 0`.

Registre media, varianza, σ, mediana e IQR. Compare las razones condición/basal.

## 14. Experimento libre
Diseñe una manipulación propia utilizando los controles disponibles.

- Pregunta de investigación:
- Hipótesis:
- Variable independiente:
- Variables dependientes:
- Variables controladas:
- Configuración:
- Resultado:
- Conclusión:

## 15. Cálculo manual
Use el conjunto basal y calcule manualmente la media y la varianza poblacional. Luego utilice la pestaña **Modelo y cálculo manual**.

| Medida | Valor manual | Simulador | Diferencia | % error |
|---|---:|---:|---:|---:|
| Media | | | | |
| Varianza | | | | |

## 16. Registro de datos
Después de cada condición pulse **Registrar medición**. Al finalizar, descargue:

- `experimentos_momentos_estadisticos.csv`, o
- `experimentos_momentos_estadisticos.xlsx`.

Nombre recomendado para entrega: `Grupo_Apellido_Momentos.xlsx`.

## 17. Preguntas de análisis
1. ¿Por qué dos conjuntos con la misma media pueden tener comportamientos diferentes?
2. ¿Qué información añade la desviación estándar que la media no proporciona?
3. En el experimento 2, ¿qué medidas conservaron su valor? Explique por qué.
4. En el experimento 3, ¿cómo cambió la forma visual del boxplot al aumentar k?
5. ¿Por qué el experimento 3 puede cambiar la varianza sin cambiar la media?
6. En el experimento 4, compare el cambio absoluto de la media con el de la mediana.
7. ¿Por qué un valor atípico no debe eliminarse automáticamente solo por aparecer fuera de 1.5·IQR?
8. ¿Qué ventaja tiene comparar media y mediana antes de entrenar un modelo de IA?
9. ¿Cómo puede una gran diferencia de escala entre variables afectar un análisis posterior?
10. ¿Qué información del conjunto original se pierde al resumirlo solo con media y varianza?
11. ¿Qué limitación tiene interpretar un boxplot sin conocer el contexto de adquisición de los datos?
12. ¿Qué evidencia adicional necesitaría para afirmar que una variable sigue una distribución normal?

## 18. Preguntas de pensamiento crítico
1. ¿Puede un conjunto muy asimétrico tener media y mediana cercanas? ¿Qué otra evidencia revisaría?
2. ¿Qué cambiaría si la varianza se estimara como varianza muestral (`ddof=1`) en lugar de poblacional?
3. Diseñe una estrategia para detectar si un valor extremo corresponde a error de medición o a una observación real.

## 19. Conclusiones
Redacte entre 3 y 5 conclusiones basadas exclusivamente en sus resultados. Cada conclusión debe relacionar una manipulación con un cambio observado en una medida o gráfica.

## 20. Actividad final
Usando los experimentos 2–5, explique qué medidas descriptivas son invariantes o sensibles ante traslación, escalamiento, modificación de dispersión y adición de un valor extremo.

## 21. Producto a entregar
- Guía respondida.
- Archivo Excel o CSV exportado desde la app.
- Tabla de cálculo manual vs simulador.
- Interpretación de al menos dos boxplots.
- Respuestas de análisis.
- 3–5 conclusiones.

## 22. Criterios de evaluación
| Criterio | Peso |
|---|---:|
| Predicciones e hipótesis | 15 % |
| Registro correcto de datos | 20 % |
| Cálculos manuales | 20 % |
| Interpretación de gráficas y medidas | 25 % |
| Preguntas de análisis | 10 % |
| Conclusiones | 10 % |
