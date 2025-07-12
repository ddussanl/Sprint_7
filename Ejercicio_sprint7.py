import pandas as pd
clientes = pd.read_csv(r"C:\Data_Analytics\Sprint_7\datos_clientes.csv")
fechas = pd.read_csv(r"C:\Data_Analytics\Sprint_7\DATOS_fechas.csv")
transacciones = pd.read_csv(r"C:\Data_Analytics\Sprint_7\DATOS_transacciones.csv")

# 1. ¿Quien es el cliente con la mayor cantidad de `StockCode`?.
# convertir a int la columna CustomerID
transacciones['CustomerID'] = transacciones['CustomerID'].astype('int')

# unir el df clientes con el df transacciones
df_completo = pd.merge(transacciones,clientes, on='CustomerID', how='inner')

clientes_top = df_completo.groupby(['CustomerID','Nombre'])['StockCode'].count().sort_values(ascending=False).reset_index()
clientes_top = clientes_top.rename(columns={'StockCode' : 'Cant_StockCode'})

id_clientes = clientes_top.loc[0,"CustomerID"]
nombre_clientes = clientes_top.loc[0,"Nombre"]
cantidad_stock = clientes_top.loc[0,"Cant_StockCode"]

print(f"El cliente con mayor la mayor cantidad de StockCode es {nombre_clientes}, identificada con ID {id_clientes} y con una cantidad de {cantidad_stock} unidades.")

# 2. calcular la edad promedio de los clientes
# primero verificar si existen valores nulos

clientes.isnull().sum()
edad_promedio = clientes['Edad'].mean()
print(f"La edad promedio de los clientes es de {edad_promedio} años.")

# 3. ¿Cuantos clientes tenemos con nombres repetidos y con nombres únicos?
nombres_repetidos = df_completo['Nombre'].duplicated().sum()
print(f'Existen {nombres_repetidos} nombres de clientes repetidos')

nombres_unicos = df_completo['Nombre'].nunique()
print(f'Existen {nombres_unicos} clientes con nombres unicos')

#4. ¿Quien es el cliente que más compra ha hecho segun nuestra base de datos de fechas y cual es el més en que mayor cantidad de compras hizo?
# cambiar el tipo de dato de la columna FechaCompra. Debe ser formato fecha
fechas['FechaCompra'] = pd.to_datetime(fechas['FechaCompra'])

# Contar compras por cliente
compras_por_cliente = fechas['CustomerID'].value_counts().reset_index()
compras_por_cliente.columns = ['CustomerID', 'CantidadCompras']

# obtener fila del cliente con más compras
top_cliente = compras_por_cliente.iloc[0]
id_top_cliente = top_cliente['CustomerID']
cantidad_top = top_cliente['CantidadCompras']

# agregar columna de mes
fechas['Mes'] = fechas['FechaCompra'].dt.month

# filtrar solo las compras del cliente con más compras
compras_cliente = fechas[fechas['CustomerID'] == id_top_cliente]

mes_mayor_compra = compras_cliente['Mes'].value_counts().reset_index()
mes_mayor_compra.columns = ['Mes', 'CantidadCompras']

mes_top = mes_mayor_compra.iloc[0]['Mes']
cantidad_compras_mes = mes_mayor_compra.iloc[0]['CantidadCompras']

print(f"El cliente que más compras ha hecho es {id_top_cliente} con {cantidad_top} compras realizadas")
print(f"El mes en que más compras hizo fue el mes {mes_top} con {cantidad_compras_mes} compras.")

# 5. Van a crear un nuevo DataFrame con la siguiente info:
# `Nombre`, `Edad`, `StockCode`, `Description` y `Quantity`. Estos nuevos DataFrames deben ser coherentes con los datos ya entregados.

# unir fechas con transacciones
df_temporal = pd.merge(fechas, transacciones, on='CustomerID', how='inner')

# unir df_temporal con clientes
df_nuevo = pd.merge(df_temporal, clientes, on='CustomerID', how='inner')

# seleccionar las columnas que se requieren
df_final = df_nuevo[['Nombre', 'Edad', 'StockCode', 'Description', 'Quantity']].copy()

print(df_final.head())

# 6. Con el DataFrame anterior van a crear dos columnas nuevas que son: grupo_edad y grupo_cantidad

# se deben crear rangos de edad para clasificar clientes por edad
# se deben crear rangos de cantidad para clasificar las cantidades de compras realizadas

def clasificar_edad(edad):
    if edad <= 17:
        return 'Adolescente'
    elif edad <= 30:
        return 'Joven'
    elif edad <= 50:
        return 'Adulto'
    else:
        return 'Senior'
    
df_final['grupo_edad'] = df_final['Edad'].apply(clasificar_edad)

def clasificar_compras(cantidad):
    if cantidad <= 5:
        return 'Bajo'
    elif cantidad <= 20:
        return 'Medio'
    else:
        return 'Alto'
    
df_final['grupo_cantidad'] = df_final['Quantity'].apply(clasificar_compras)

print(df_final.head())