import socket, threading, time

key = 0

server = ('192.168.1.49',9090) # default server
host = socket.gethostbyname(socket.gethostname())
#host = '192.168.1.49'

port = 0

shutdown = False
join = False

def receiving (name, sock):
	while not shutdown:
		try:
			while True:
				data, addr = sock.recvfrom(1024)
				my_time = time.ctime()
				
				# decription
				decrypt = ""; k = False
				for i in data.decode("utf-8"):
					if i == ":":
						k = True
						decrypt += i
					elif k == False or i == " ":
						decrypt += i
					else:
						decrypt += chr(ord(i)^key)

				print("[" + str(my_time) + "] " + decrypt)
					
				time.sleep(0.2)
		except:
			pass


my_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
my_socket.bind((host,port))
my_socket.setblocking(0)

print("You joined to " + str(server))

# поиск имени в конфиге
userC = open('user_settings.txt', 'r')
user_name = userC.readline()
if user_name == "":
    user_name = str(input("Please, write your nickname...    "))
    u = open('user_settings.txt', 'w')
    u.write(user_name)
    u.close()
userC.close()

thread = threading.Thread(target = receiving, args = ("RecvThread", my_socket))
thread.start()

while shutdown == False:
	if join == False:
		my_socket.sendto((user_name + " => join chat ").encode("utf-8"), server)
		join = True
	else:
		try:
			message = input()

			# Begin
			crypt = ""
			for i in message:
				crypt += chr(ord(i)^key)
			message = crypt
			# End

			if message != "":
				
				my_socket.sendto((user_name + ":: "+message).encode("utf-8"), server)
			
			time.sleep(0.2)
			
		except:
			my_socket.sendto((user_name + " <= left chat ").encode("utf-8"), server)
			shutdown = True

thread.join()
my_socket.close()
