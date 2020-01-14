obis_str={'Voltage':'0C.07.00*FF', 'Current': '0B.07.00*FF', 'Active_Power': '10.07.00*FF'}
table = str.maketrans("", "", '.*')

for k in obis_str:
    obis_str[k]=obis_str[k].translate(table)+'()'



#obis_str['Voltage'] = obis_str['Voltage'].translate(table)+'()'


print (obis_str)