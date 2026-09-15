from collections import Counter
import numpy as np

DATOS_PRESENTACION = np.array([
    10.251,9.736,11.281,10.210,8.929,10.723,12.608,11.894,8.593,7.469,
    8.753,10.083,5.350,9.562,7.508,8.535,8.911,9.367,10.823,12.085,
    12.225,8.831,12.471,10.023,7.919,13.130,11.132,5.372,10.720,10.018,
    7.481,9.263,11.136,9.315,15.053,8.496,12.337,11.320,10.323,11.550,
    8.811,7.285,11.673,11.518,11.147,12.200,10.381,12.050,9.746,10.569
], dtype=float)

def validar_datos(datos):
    x=np.asarray(datos,dtype=float).ravel()
    if x.size<2: raise ValueError("Se requieren al menos dos observaciones.")
    if not np.all(np.isfinite(x)): raise ValueError("Los datos contienen NaN o Infinity.")
    return x

def aplicar_transformacion(datos, modo="Sin transformación", escala=1.0, desplazamiento=0.0,
                            factor_dispersion=1.0, agregar_atipico=False, valor_atipico=30.0):
    x=validar_datos(datos).copy()
    if modo=="Escala y desplazamiento": x=escala*x+desplazamiento
    elif modo=="Dispersión con media constante":
        mu=float(np.mean(x)); x=mu+factor_dispersion*(x-mu)
    elif modo!="Sin transformación": raise ValueError("Modo de transformación no reconocido.")
    if agregar_atipico:
        if not np.isfinite(valor_atipico): raise ValueError("El valor atípico debe ser finito.")
        x=np.append(x,float(valor_atipico))
    return x

def mascara_atipicos(datos):
    x=validar_datos(datos)
    q1,q3=np.percentile(x,[25,75]); iqr=q3-q1
    li,ls=q1-1.5*iqr,q3+1.5*iqr
    return (x<li)|(x>ls),float(li),float(ls)

def _moda_texto(x):
    counts=Counter(np.round(x,12)); m=max(counts.values())
    if m<=1: return "Sin moda repetida"
    vals=sorted(k for k,v in counts.items() if v==m)
    return ", ".join(f"{v:g}" for v in vals)+f" (f={m})"

def resumen_estadistico(datos):
    x=validar_datos(datos)
    q1,q3=np.percentile(x,[25,75]); iqr=q3-q1
    mask,li,ls=mascara_atipicos(x)
    return {
        "n":int(x.size),"media":float(np.mean(x)),"varianza":float(np.var(x,ddof=0)),
        "desv_std":float(np.std(x,ddof=0)),"mediana":float(np.median(x)),
        "q1":float(q1),"q3":float(q3),"iqr":float(iqr),"min":float(np.min(x)),"max":float(np.max(x)),
        "limite_inferior":li,"limite_superior":ls,"n_atipicos":int(mask.sum()),"moda":_moda_texto(x)
    }
