#!/usr/bin/python3
import socket, sys, threading, queue,time


'''
kody wiadomosci:
0 logowanie
'''

PORT = 1058
HOST ='localhost'
newUserComes = queue.Queue()
newMesages = queue.Queue()
activeUsers = []
#jesli ktos loguje to na poczatku wiadomosci ma login
#jesli wysyla to ma od do wiadomosc

class Server:
	users = []
	
	def __init__(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			address = HOST, PORT
			self.server.bind(address)
		except socket.error:
			print("Bindowanie nie powiodlo sie")
			return
		self.server.listen()
		
	def exit():
		self.server.close()
	
	def run(self):
		print("Czekam na polaczenie")
		while True:
			conn,addr = self.server.accept()
			threading.Thread(target=self.run_thread, args=(conn,addr)).start()
	
	def handleMessage(self):
		while not newMesages.empty():
			newMessage = newMesages.get()
			if newMessage[0] == "0":
				newMessage = newMessage.split(" ", 1)
				print ("wysylam info ze przyszedl ",newMessage[1])
				newUserComes.put(newMessage[1])
		while not newUserComes.empty():
			newUser = newUserComes.get()
			activeUsers.append(newUser)
			print("Przyszedl ", newUser)
		
	
	def run_thread(self, conn, addr):
		while True:
			message = conn.recv(1024)
			if(message.decode() != ""):
				newMesages.put(message.decode() )
			if(not newMesages.empty()):
				print ("przyszla do mnie wiadomosc")
				self.handleMessage()
			time.sleep(1)
			

newServer = Server()
newServer.run()
Server.exit()

	

