import openpyxl
import time

sheet_sii = openpyxl.load_workbook('Tabla_SII.xlsx', read_only=True)['Tabla_SII']

# Search for the B row that contains rut_sin_verificador
tiempo_inicio = time.time()
indice = 1
encontrado = False
valores = []
for row in sheet_sii.iter_rows(min_row=2, max_col=23):
    if str(row[1].value) == str("77460601"):
        valores = row
        encontrado = True
        break
    indice += 1 
print(indice)
for i in valores:
    print(i.value)
print(time.time() - tiempo_inicio)