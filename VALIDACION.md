# Validación científica y computacional

Se utilizó el conjunto de 50 valores de la presentación y las mismas definiciones implementadas por NumPy (`ddof=0` y percentiles 25/75).

| Caso | Entradas | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|
| Basal | Sin transformación | Media ≈ 10.1233; var ≈ 3.6110; σ ≈ 1.9003 | Coincide | OK |
| Traslación | a=1, b=+3 | Media +3; varianza y σ sin cambio | Coincide | OK |
| Escalamiento | a=2, b=0 | Media ×2; varianza ×4; σ ×2 | Coincide | OK |
| Dispersión | k=2 alrededor de la media | Media constante; varianza ×4; σ ×2 | Coincide | OK |
| Valor extremo | Añadir 30 | n=51; media ≈ 10.5131; 30 detectado por 1.5·IQR | Coincide | OK |

Valores basales calculados:

- n = 50
- media = 10.12332
- varianza poblacional = 3.6109702176
- desviación estándar = 1.9002553033
- mediana = 10.2305
- Q1 = 8.851
- Q3 = 11.4685
- IQR = 2.6175
- valores atípicos por 1.5·IQR = 0

## Controles de robustez
- Se rechazan conjuntos con menos de dos observaciones.
- Se rechazan NaN e Infinity.
- La exportación Excel utiliza `BytesIO` + `openpyxl`.
- La app continúa funcionando si falta el logo.
- No se realizan divisiones por cero durante el cálculo de % error; en ese caso se devuelve NaN.
