import openpyxl

sheet_sii = openpyxl.load_workbook('Tabla_SII.xlsx', read_only=True)['Tabla_SII']

# Search for the B row that contains rut_sin_verificador
indice = 1
encontrado = False
for row in sheet_sii.iter_rows(min_row=2, max_col=2):
    if str(row[1].value) == str("78583850"):
        encontrado = True
        break
    indice += 1 
print(indice)