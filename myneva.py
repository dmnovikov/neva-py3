import serial
from protocol import NevaMt3xx

print('aaa')

port = serial.Serial(port='/dev/ttyUSB0',
					 baudrate=9600, timeout=2,
					 bytesize=serial.SEVENBITS,
					 parity=serial.PARITY_EVEN,
					 stopbits=serial.STOPBITS_ONE)

protocol = NevaMt3xx.NevaMt3xx_com(port)

# connect & login
print('SEND: /?!\\r\\n')
company, device = protocol.connect()
cmd = protocol.receive()
print('RCV:' + str(cmd))
if not cmd.is_command or cmd.command != 'P0':
	raise Exception('Command "P0" expected')
password = '00000000'
protocol.send(NevaMt3xx.NevaMt3xx.Command('P1', '(' + password + ')'))
cmd = protocol.receive()
print('RCV:' + str(cmd))

if not cmd.is_ack:
	raise Exception('Access denied')
# Дата: ГГММДД

obis_str = {'Voltage': '0C.07.00*FF', 'Current': '0B.07.00*FF', 'Active_Power': '10.07.00*FF', 'Freq': '0E.07.01*FF',
'Temp':'60.09.00*FF', 'KPower': '0D.07.FF*FF'}

table = str.maketrans("", "", '.*')

for key in obis_str:
	obis_str[key] = obis_str[key].translate(table) + '()'
	# print('SEND:' + key)
	protocol.send(NevaMt3xx.NevaMt3xx.Command('R1', obis_str[key]))
	cmd = protocol.receive()
	# print('RCV:' + str(cmd))
	if not cmd.is_message:
		raise Exception('OBIS 000902FF expected')
	print(key + ':' + str(cmd.data[8:].strip('()')))

# logout
protocol.send(NevaMt3xx.NevaMt3xx.Command('B0', ''))

# try:

# except Exception as e:
# 		print (u'ERROR: '+str(e))
