# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 22:10:57 2020

@author: mies9001
"""

import pandas as pd
import numpy as np

data = pd.read_csv(r"C:\Users\mies9001\Documents\Documentos Esau\EMTECH\proyecto2\synergy_logistics_database.csv")

# Opción 1) Rutas de importación y exportación.

#direccion = 'Exports'# 'Imports'

rutas_index = data.groupby(['direction', 'origin', 'destination']).count().loc[:,['register_id']]
rutas_index.rename(columns={'register_id':"num_viajes"},inplace=True)
rutas_index.sort_values(by='num_viajes',ascending = False, inplace=True)

def top_rutas(direccion):
    rutas_ord = rutas_index.reset_index(drop=False)
    rutas_ord1 =rutas_ord[(rutas_ord.direction == direccion)]
    rutas_ord1.reset_index(drop=True, inplace=True)
    rutas_ord1.sort_values(by='num_viajes',ascending = False, inplace=True)
    rutas_ord1['% total de viajes']=rutas_ord1['num_viajes']/sum(rutas_ord1['num_viajes'])*100
    #print("Las rutas con mas "+direccion+" son: \n")
    #print(rutas_ord1.iloc[:,1:5])
    return rutas_ord1

#función
def paises_rutas(direccion):    
    lista_viajes2 = rutas_index.reset_index(drop=False)
    lista_viajes1 = lista_viajes2[(lista_viajes2.direction == direccion)]
    
    if direccion == 'Imports':
        lista_viajes = lista_viajes1.groupby(['destination']).sum()
    elif direccion == 'Exports':
        lista_viajes = lista_viajes1.groupby(['origin']).sum()
    
    lista_viajes['% total de viajes']=lista_viajes['num_viajes']/sum(lista_viajes['num_viajes'])*100
    lista_viajes.reset_index(drop=False, inplace=True)
    lista_viajes.sort_values(by='% total de viajes',ascending = False, inplace=True)
    lista_viajes.reset_index(drop=True, inplace=True)
    #print(lista_viajes)
    return lista_viajes

opc = int(input('Escribe que tipo de movimientos deseas ver para rutas:\n 1.-Imports\n 2.-Exports \n'))
if opc == 1:
    print("Las rutas con mas Imports son: \n")
    a = top_rutas('Imports')
    print(a.iloc[:,1:5])
    print("Paises con mas Imports son: \n")
    b = paises_rutas('Imports')
    print(b)
elif opc == 2:
    print("Las rutas con mas Exports son: \n")
    c = top_rutas('Exports')
    print(c.iloc[:,1:5])
    print("Paises con mas Exports son: \n")
    d = paises_rutas('Exports')
    print(d)
else:
    print('te equivocaste')

imports_ruta,imports_paises = top_rutas('Imports'),paises_rutas('Imports');
exports_ruta, exports_paises = top_rutas('Exports'),paises_rutas('Exports');

# Opción 2) Medio de transporte utilizado.
    
# Hago una agrupación por dirección y modo de transporte para saber el numero de viajes
medios_index = data.groupby(['direction', 'transport_mode']).count().loc[:,['register_id']]
rutas_index.rename(columns={'register_id':"num_viajes"},inplace=True)

# Y otra agrupación por dirección y modo de transporte para saber la venta total
medios_ventas = data.groupby(['direction', 'transport_mode']).sum().loc[:,['total_value']]

#Uno ambas tablas con la función merge de pandas
medios = pd.merge(medios_index,medios_ventas, left_index=True, right_index=True)

def medios_trans(direccion):
    lista_medios1 = medios.reset_index(drop=False)
    lista_medios = lista_medios1[(lista_medios1.direction == direccion)]
    
    lista_medios.sort_values(by='total_value',ascending = False, inplace=True)
    lista_medios['% de venta total']=lista_medios['total_value']/sum(lista_medios['total_value'])*100
    lista_medios['% total de viajes']=lista_medios['register_id']/sum(lista_medios['register_id'])*100
    lista_medios.reset_index(drop=True)
    #print (lista_medios)
    return lista_medios

opc_2 = int(input('Escribe que tipo de moviminetos deseas ver en medios de transporte:\n 1.-Imports\n 2.-Exports \n'))
if opc_2 == 1:
    a = medios_trans('Imports')
    print(a)
elif opc_2 == 2:
    b = medios_trans('Exports')
    print(b)
else:
    print('te equivocaste')

imports_medios =  medios_trans('Imports')
exports_medios = medios_trans('Exports');

# Opción 3) Valor total de importaciones y exportaciones.
#direccion = 'Exports'
def ventas_rutas(direccion):
    # Vamos a sacar las ventas por ruta
    ventas_x_ruta = data.groupby(['direction', 'origin', 'destination']).sum().loc[:,['total_value']]
    ventas_x_ruta.rename(columns={'total_value':"venta_total"},inplace=True)
    ventas_x_ruta.reset_index(drop=False, inplace=True)
    
    # Filtramos por direccion (Imports o Exports)
    ventas_x_ruta1 = ventas_x_ruta[(ventas_x_ruta.direction == direccion)]
    
    if direccion == 'Imports':
        ventas_x_ruta2 = ventas_x_ruta1.groupby(['destination']).sum()
    elif direccion == 'Exports':
        ventas_x_ruta2 = ventas_x_ruta1.groupby(['origin']).sum()
        
    ventas_x_ruta2.reset_index(drop=False, inplace=True)
    ventas_x_ruta2.sort_values(by='venta_total',ascending = False, inplace=True)
    ventas_x_ruta2['% de venta total']=ventas_x_ruta2['venta_total']/sum(ventas_x_ruta2['venta_total'])*100
    ventas_x_ruta2.reset_index(drop=True, inplace=True)
    #print(ventas_x_ruta2)
    return ventas_x_ruta2

opc_3 = int(input('Escribe que tipo de movimientos deseas ver en venta total:\n 1.-Imports\n 2.-Exports \n'))

if opc_3 == 1:
    print('las ventas de Imports por paises son: \n')
    a = ventas_rutas('Imports')
    print(a)
elif opc_3 == 2:
    print('las ventas de Exports por paises son: \n')
    b = ventas_rutas('Exports')
    print(b)
else:
    print('te equivocaste')
    
exports_ventas_rutas = ventas_rutas('Exports')
imports_ventas_rutas = ventas_rutas('Imports')

