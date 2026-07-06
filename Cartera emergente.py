#Portfolio emergente con dos activos por país
import seaborn as sns
import matplotlib.pyplot as plt
import yahooquery
import pandas as pd
import numpy as np
from yahooquery import Ticker

#Descargamos datos
tickers=['YPF','GGAL','PBR','ITUB','BSAC','SQM']
acciones= Ticker(tickers)
data = acciones.history(start="2025-01-01", end="2026-06-29")

precios=data["adjclose"].unstack(level="symbol")
precios.to_csv("precios2.csv") 



#Retornos y riesgo
retornos = precios.pct_change().dropna()

retorno_anual = retornos.mean() * 252
volatilidad_anual = retornos.std() * (252 ** 0.5)



#Varianzas y covarianzas+ gráfico
cov_anual = retornos.cov() * 252

correlacion= retornos.corr()

sns.heatmap(correlacion, annot=True, cmap="coolwarm",vmin=0, vmax=1)
plt.title("Correlación entre activos")
plt.savefig("correlacion.png",dpi=500,bbox_inches="tight")
plt.show()



#Simulación de carteras
nro_carteras = 100000
retorno_carteras=[]
riesgo_carteras = []
pesos_carteras = []

for i in range(nro_carteras):
    pesos = np.random.random (6)
    pesos = pesos / np.sum(pesos)
    
    retorno = np.dot(pesos, retorno_anual)
    riesgo = np.sqrt(np.dot(pesos.T, np.dot(cov_anual,pesos)))
    
    retorno_carteras.append(retorno)
    riesgo_carteras.append(riesgo)
    pesos_carteras.append(pesos)
    
plt.figure()
plt.scatter(riesgo_carteras, retorno_carteras, s=5)
plt.xlabel("Riesgo")
plt.ylabel("Retorno anual esperado")
plt.title ("Carteras simuladas- Retorno en Emergentes")
plt.show()


#Ratio de Sharpe.
retorno_carteras = np.array(retorno_carteras)
riesgo_carteras = np.array(riesgo_carteras)
rf=0.05
sharpe= (retorno_carteras - rf) / riesgo_carteras

idx_sharpe = np.argmax(sharpe)
idx_minvar = np.argmin(riesgo_carteras)

plt.figure()
plt.scatter(riesgo_carteras, retorno_carteras , c=sharpe, cmap="viridis", s=5)
plt.colorbar(label="Ratio de Sharpe")
plt.scatter(riesgo_carteras[idx_sharpe], retorno_carteras[idx_sharpe], c="blue", marker= "*", s=300, label="Máx Sharpe")
plt.scatter(riesgo_carteras[idx_minvar], retorno_carteras[idx_minvar], c="red", marker="*", s=300, label="Mín Varianza")
plt.xlabel("Riesgo")
plt.ylabel("Retorno anual esperado")
plt.title("Frontera eficiente emergente")
plt.legend()
plt.show()



#Optimizando
activos = retorno_anual.index
x = np.arange(len(activos))
ancho = 0.35

plt.figure()
plt.bar(x - ancho/2, pesos_carteras[idx_sharpe], ancho, label="Máx Sharpe")
plt.bar(x + ancho/2, pesos_carteras[idx_minvar], ancho, label="Mín Varianza")
plt.xticks(x,activos)
plt.ylabel("Peso en la cartera")
plt.title("Composición de las carteras óptimas")
plt.legend()
plt.show()


#Graficando retornos
base100 = precios / precios.iloc[0] * 100

plt.figure(figsize=(10,6))
for activo in base100.columns:
    plt.plot(base100.index, base100[activo],label=activo)
plt.xlabel("Fecha")
plt.ylabel("Retorno acumulado en base 100")
plt.title("Evolución de activos emergentes")
plt.legend()
plt.show()
















