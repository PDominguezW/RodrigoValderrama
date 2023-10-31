import openpyxl
import json

def calculate_score(rut, data):

    # Read 'modelo_evaluacion.xlsx' with openpyxl
    workbook = openpyxl.load_workbook('modelo_evaluacion.xlsx')

    # Get the sheet you want to edit
    sheet = workbook['1.Datos']

    # LEEMOS E INGRESAMOS DATOS TABLA SII
    try:
        # Read excel in read only mode
        sheet_sii = openpyxl.load_workbook('Tabla_SII.xlsx', read_only=True)['Tabla_SII']

    except Exception as e:
        print(e)

    # Ingresamos rut en la partye superior
    sheet['B2'] = rut

    # Search for the B row that contains rut
    rut_formateado = rut.replace('.', '')
    rut_sin_verificador = rut_formateado.split('-')[0]

    fila = 0

    if fila != 0:
        # Llenamos B6 
        sheet['B6'] = rut.split('-')[1]
        sheet['B7'] = sheet_sii[f'H{fila + 1}'].value
        sheet['B8'] = 0

        sheet['B10'] = rut
        sheet['B11'] = sheet_sii[f'D{fila + 1}'].value
        sheet['B12'] = sheet_sii[f'I{fila + 1}'].value
        sheet['B13'] = sheet_sii[f'F{fila + 1}'].value
        sheet['B14'] = sheet_sii[f'G{fila + 1}'].value
        sheet['B15'] = sheet_sii[f'E{fila + 1}'].value
        sheet['B15'] = sheet_sii[f'E{fila + 1}'].value

    # INGRESAMOS DATA EXPERIAN
    sheet['B21'] = data["experian"]["resumen_avaluo_bienes_raices"]["total_protestos_y_documentos"]
    sheet['B22'] = data["experian"]["resumen_avaluo_bienes_raices"]["total_en_pesos"]
    # sheet['B23'] = data["experian"]["resumen_morosidad"]["nro_acreedores"]
    # sheet['B24'] = data["experian"]["resumen_morosidad"]["total_doc_impagos"]
    # sheet['B25'] = data["experian"]["resumen_morosidad"]["total_pesos"]

    sheet['B23'] = data["experian"]["resumen_morosidad"]["nro_acreedores"]
    sheet['B24'] = data["experian"]["resumen_morosidad"]["total_pesos"]
    sheet['B25'] = data["experian"]["resumen_morosidad"]["total_doc_impagos"]

    if data["experian"]["resumen_socios_sociedades"]["rut_socio"]:
        sheet['B28'] = data["experian"]["resumen_socios_sociedades"]["rut_socio"].split('-')[0]
        sheet['B29'] = data["experian"]["resumen_socios_sociedades"]["rut_socio"].split('-')[1]

    sheet['B30'] = data["experian"]["resumen_socios_sociedades"]["data"]["resumen_avaluo_bienes_raices"]["total_protestos_y_documentos"]
    sheet['B31'] = data["experian"]["resumen_socios_sociedades"]["data"]["resumen_avaluo_bienes_raices"]["total_en_pesos"]
    sheet['B32'] = data["experian"]["resumen_socios_sociedades"]["data"]["resumen_morosidad"]["nro_acreedores"]
    sheet['B33'] = data["experian"]["resumen_socios_sociedades"]["data"]["resumen_morosidad"]["total_pesos"]
    sheet['B34'] = data["experian"]["resumen_socios_sociedades"]["data"]["resumen_morosidad"]["total_doc_impagos"]

    # INGRESAMOS DATA DEALERNET

    periodos = list(data["dealernet"]["empresa"]["AL DIA E IMPAGOS <30 DIAS"].keys())
    periodos_letras = ['B', 'C', 'D', 'E']

    sheet['B40'] = periodos[0]
    sheet['C40'] = periodos[1]
    sheet['D40'] = periodos[2]
    sheet['E40'] = periodos[3]

    sheet['B65'] = periodos[0]
    sheet['C65'] = periodos[1]
    sheet['D65'] = periodos[2]
    sheet['E65'] = periodos[3]

    columnas = [
        'AL DIA E IMPAGOS <30 DIAS',
        'IMPAGOS 30 Y 90 DIAS',
        'IMPAGOS 90 Y 180 DIAS',
        'IMPAGOS 180 DIAS Y 3 ANOS',
        'IMPAGOS >= 3 ANOS',
        'CREDITOS DE CONSUMO',
        'NRO. ENTIDADES CRED.CONSUMO',
        'CREDITOS PARA VIVIENDA',
        'OPERACIONES FINANCIERAS',
        'INSTRUM. DEUDAS ADQUIRIDOS',
        'CREDITOS COMERCIALES',
        'DEUDA COM. VIGENTE MEX',
        'DEUDA COM. VENCIDA MEX',
        'INDIRECTA IMPAGOS <30 DIAS',
        'INDIRECTA IMPAGOS 30 DIAS Y 3 ANOS',
        'INDIRECTA IMPAGOS >= 3 ANOS',
        'LINEA CREDITO DISPONIBLE',
        'CREDITOS CONTINGENTES',
        'NRO. ENTIDADES.CRED.COM ER.',
        'CREDITOS LEASING AL DIA',
        'CREDITOS LEASING IMPAGO'
    ]

    # Dealernet empresa
    for columna in columnas:
        for i in range(4):
            sheet[f'{periodos_letras[i]}{columnas.index(columna) + 41}'] = data["dealernet"]["empresa"][columna][periodos[i]]

    if data["experian"]["resumen_socios_sociedades"]["rut_socio"]:
        # Dealernet socio
        for columna in columnas:
            for i in range(4):
                sheet[f'{periodos_letras[i]}{columnas.index(columna) + 66}'] = data["dealernet"]["socio"][columna][periodos[i]]

    # Save the changes to the workbook
    workbook.save('modelo_evaluacion_result.xlsx')

    return 'modelo_evaluacion_result.xlsx'

if __name__ == "__main__":

    # Read the file 'new_data.json'
    with open('new_data.json') as json_file:
        data = json.load(json_file)

    # Run Flask app 76109342
    calculate_score("76109013", data)