from multiprocessing.connection import Listener
from konlpy.tag import Kkma
	
from array import array

address = ('localhost', 65123)
password = b'1234'
listener = Listener(address, authkey=password)

#initialize
if __name__ == '__main__':
	kkma = Kkma()
	kkma.nouns('initializing')
	print('main!')

while True:
	conn = listener.accept()
	print('connection accepted from', listener.last_accepted)
	msg = conn.recv()
	sendMessage = kkma.nouns(msg)
	print(sendMessage)
	conn.send(sendMessage)
	conn.close()