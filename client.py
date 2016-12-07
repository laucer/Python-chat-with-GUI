#!/usr/bin/python3
import socket, sys, threading, tkinter as tk, time,queue

PORT = 1058
HOST ='localhost'
messageToSend = queue.Queue()


class ClientSender(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	
	
	def setMessage(self, message):
		self.message = message
	
	def run(self):
		print("Gotowy do nadawania")
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		address = HOST, PORT
		self.socket.connect(address)
		self.socket.send(self.message.encode())
		print(self.message)
		return



class ClientListener(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	
	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		address = HOST, PORT
		self.socket.connect(address)
		while(True):
			print("Nasluchuje")
			if not messageToSend.empty():
				sendMsg()
			time.sleep(1)
		
		
class Gui(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		
	def exitClick(self, event):
		exit(0)
	
	def sendMessageClick(self, event, textField):
		print(textField.get())
		textField.delete(0, "end") #clears textField
	
	def run(self):
		root = tk.Tk()
		root.title("Laucer's chat")
		root.minsize(600,400)
		root.bind("<Return>", lambda event: self.sendMessageClick(event,textField) ) #enter
		
		mainFrame = tk.Frame(root)
		mainFrame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
		
		root.rowconfigure(0, weight=1)
		root.columnconfigure(0, weight=1)
		
		
		#ChatField
		chat = tk.Text(mainFrame)
		chat.insert('end', 'some text')
		chat.configure(state = "disabled") #nie mozna po tym pisac
		chat.grid(column=0, row=0, sticky=tk.N + tk.S + tk.W + tk.E)
		
		#TextFieldToSend
		textField = tk.Entry(mainFrame)
		textField.grid(column=0, row=1, sticky=tk.N + tk.S + tk.W + tk.E)
		
		#SendMessageButton
		buttonSend = tk.Button(mainFrame)
		buttonSend["text"] = "Send Message"
		buttonSend.grid(column=0, row=2, sticky=tk.N + tk.S + tk.W + tk.E)
		buttonSend.bind("<Button-1>", lambda event: self.sendMessageClick(event,textField))
		
		
		#usersPanel
		usersPanel= tk.Listbox(mainFrame)
		usersPanel.insert(1, "ALL")
		usersPanel.grid(column=2, row=0, sticky=tk.N + tk.S + tk.W + tk.E)
		
		#ExitButton
		buttonExit = tk.Button(mainFrame)
		buttonExit["text"] = "Exit"
		buttonExit["background"] = "gray"
		buttonExit.grid(column=2, row=2, sticky=tk.N + tk.S + tk.W + tk.E)
		buttonExit.bind("<Button-1>", self.exitClick)
		
		root.mainloop()
		
class getUsername(threading.Thread):
	def __init__(self):
		window = tk.Tk()
		window.title = ("Log-In")
		usernametext = tk.Label(window, text="Username")
		usernameguess = tk.Entry(window)
		loginButton = tk.Button(text = "Login")
		loginButton.bind("<Button-1>", lambda event: self.loginClick(event,usernameguess,window))
		usernametext.pack()
		usernameguess.pack()
		loginButton.pack()
		window.mainloop()
	
	def loginClick(self, event, usernameguess,window):
		message = "0 "
		message += usernameguess.get()
		messageToSend.put(message)
		window.destroy()
		
		
def sendMsg():
	message = messageToSend.get()
	clientSender = ClientSender()
	clientSender.setMessage(message)
	clientSender.start()

getUsr = getUsername()
GuiThread = Gui()
GuiThread.start()
clientListenerThread = ClientListener()
clientListenerThread.daemon = True
clientListenerThread.start()

