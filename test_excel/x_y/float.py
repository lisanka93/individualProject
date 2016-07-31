import openpyxl
import os




#store two decimals, should be enough
a = 8.93759327523
a = round(a,2)
b = 7.23
c = 0.67
d = 1
e = 0             #gets tsored as int

#trying with string
vector_string = str(a) + "," + str(b) + "," + str(c) + "," + str(d) + "," + str(e)
vector_list = [a, b, c, d, e]



filename =  "/home/user/Documents/IndProject/Data_and_Code/test_excel/x_y/x.xlsx"
wb1 = openpyxl.load_workbook(filename)
sheet1 = wb1.get_sheet_by_name('Sheet1')

sheet1.cell(row = 1, column = 1).value = vector_string

wb1.save(filename)
