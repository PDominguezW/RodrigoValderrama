import xlwings as xw
book = xw.Book("modelo_evaluacion.xlsx")
book.app.calculate()
book.save("modelo_evaluacion_result.xlsx")