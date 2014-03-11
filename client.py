import socket
import pickle
import fileinput
import sys
from datetime import date

## Class cuaca
class Cuaca:
	def __init__(self, hari, bulan, tahun, cuaca):
		self.hari = hari
		self.bulan = bulan
		self.tahun = tahun
		self.tanggal = date(tahun, bulan, hari)
		self.cuaca = cuaca
	def get_data(self):
		return str(self.hari) + "/" + str(self.bulan) + "/" + str(self.tahun) + " :" + self.cuaca

## Membuat socket untuk client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

## Koneksi client ke server
client_socket.connect(('localhost', 1234))

## Meminta input tanggal
print "Contoh format input yang sah:"
print " 1. 30/1/2014"
print " 2. 30/1/2014-5/2/2014"
cmd = raw_input("Masukkan tanggal:")
print cmd

f1 = cmd.split('/')
f2 = cmd.split('-')
if len(f1) == 3:
	print "Format input sah"
	cmd = cmd + "-" + cmd
elif len(f2) == 2:
	print "Format input sah"
else:
	print "Format input tidak bisa diproses"
	sys.exit(0)

## Kirim pesan ke server
#REM: message = "Hi server ... "
#REM: message = pickle.dumps(message)
#REM: client_socket.send(message)
client_socket.send(cmd)

## Terima pesan dari server
message = client_socket.recv(1024)
message = pickle.loads(message)

## Print pesan dari server
#print "From server: " + message
print "From server: "
for item in message:
	print item.get_data()

## Close koneksi
client_socket.close()