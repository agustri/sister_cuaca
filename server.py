import socket
import sys
import select	# buat multiclient
import pickle	# buat object serialization
from datetime import date

## Dictionary bulan ke integer
dict_bulan = {
	"Januari" 	: 1,
	"Februari" 	: 2,
	"Maret" 	: 3,
	"April" 	: 4,
	"Mei"		: 5,
	"Juni"		: 6,
	"Juli"		: 7,
	"Agustus"	: 8,
	"September"	: 9,
	"Oktober"	: 10,
	"November"	: 11,
	"Desember"	: 12
}

print "TEST : ", dict_bulan["Maret"]

## Ambil info tanggal dan cuaca
# arg = "Kamis, 14 Maret 2014 - Cerah"
def get_info(arg):
	# a = ['Kamis, 14 Maret 2014', 'Cerah']
	a = arg.split(' - ')
	# desc = 'Cerah'
	cuaca = a[1]
	# a = ['Kamis', '14 Maret 2014']
	a = a[0].split(', ')
	# a = ['14', 'Maret', '2014']
	a = a[1].split()
	hari = int(a[0])
	bulan = dict_bulan[a[1]]
	tahun = int(a[2])
	return hari, bulan, tahun, cuaca

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

## Baca file data
data = open('data.txt', 'r')
## Inisiasi list kosong
list_cuaca = []
#print data.read()
for line in data:
	## Buat object per line
	hari, bulan, tahun, cuaca = get_info(line)
	item = Cuaca(hari, bulan, tahun, cuaca)
	list_cuaca.append(item)
	print item.get_data()

print "Ukuran list_cuaca : ", len(list_cuaca)

## Dapatkan list cuaca dari string cmd
def get_list_cuaca(cmd):
	f = cmd.split('-')
	f1 = f[0].split("/")
	f2 = f[1].split("/")
	#print "f1: ", f1[0], f1[1], f1[2]
	#print "f2: ", f2[0], f2[1], f2[2]
	h1 = int(f1[0])
	b1 = int(f1[1])
	t1 = int(f1[2])
	h2 = int(f2[0])
	b2 = int(f2[1])
	t2 = int(f2[2])
	#print "start: ", h1, b1, t1, h1+b1+t1
	#print "end  : ", h2, b2, t2, h2+b2+t2
	start = date(t1, b1, h1)
	end = date(t2, b2, h2)
	hasil = []
	for item in list_cuaca :
		#print item.get_data()
		#print item.hari, item.bulan, item.tahun, item.hari+item.bulan+item.tahun
		if item.tanggal>=start and item.tanggal<=end:
			hasil.append(item)
			#print "Terpilih"

	return hasil



## Buat socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1234))
server_socket.listen(5)

## List client yang terkoneksi
input_list = [server_socket]

try:
	while 1 :
		## Melayani beberapa client yang terkoneksi satu-satu
		input, output, exception = select.select(input_list, [], [])

		for socket in input:
			## Accept client dan tambahkan client ke list
			if socket == server_socket:
				client_socket, client_address = server_socket.accept()
				input_list.append(client_socket)
				print "Accept client: ", client_address

			## Menangani pengiriman dan penerimaan pesan
			else:
				cmd = socket.recv(1024)
				if cmd:
					# pesan di-Unpickle
					print "Permintaan client : ", client_address, cmd
					message = get_list_cuaca(cmd)
					print "Ukuran message : ", len(message)
					#for item in message:
					#	print item.get_data()

					# pesan di-Pickle kemudian kirim
					message = pickle.dumps(message)
					socket.send(message)
				else:
					socket.close()
					input_list.remove(socket)

## Agar program bisa keluar pake Ctrl + C (Linux) atau Ctrl + Pause Break (Windows)
except (KeyboardInterrupt, SystemExit):
	server_socket.close()
	sys.exit(0)