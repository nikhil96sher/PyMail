from Tkinter import *
from sender import Mail

class App:

	def __init__(self, master):

		# frame = master
		# # frame = Frame(master)
		# # frame.pack()

		# self.button = Button(
		# 	frame, text="QUIT", fg="red", command=frame.quit
		# 	)
		# self.button.pack(side=LEFT)

		# self.hi_there = Button(frame, text="Hello", command=self.say_hi)
		# self.hi_there.pack(side=LEFT)

		# listbox = Listbox(master)
		# listbox.pack()
		# listbox.insert(END, "a list entry")
		# for item in ["one", "two", "three", "four"]:
		# 	listbox.insert(END, item)
		
		# lb = Listbox(master)
		# b = Button(master, text="Delete",
		#    command=lambda lb=lb: lb.delete(ANCHOR))
		# for item in ["one", "two", "three", "four"]:
		# 	lb.insert(END, item)
		# lb.pack()
		# b.pack()

		self.username = StringVar()
		self.password = StringVar()
		self.message  = StringVar()
		self.senderid = StringVar()
		self.receiverid = StringVar()
		Label(master, text="ID").grid(row=0)
		Label(master, text="Password").grid(row=1)
		Label(master, text="senderid").grid(row=2)
		Label(master, text="receiverid").grid(row=3)
		Label(master, text="message").grid(row=4)
		e1 = Entry(master, textvariable=self.username )
		e2 = Entry(master, textvariable=self.password , show="*")
		e3 = Entry(master, textvariable=self.senderid )
		e4 = Entry(master, textvariable=self.receiverid )
		e5 = Entry(master, textvariable=self.message )
		e1.grid(row=0, column=1)
		e2.grid(row=1, column=1)
		e3.grid(row=2, column=1)
		e4.grid(row=3, column=1)
		e5.grid(row=4, column=1)
		self.button = Button(
			master, text="QUIT", fg="red", command=master.quit
			)
		self.button.grid(row=5,column=0)
		self.hi_there = Button(master, text="LOGIN", command=self.say_hi)
		self.hi_there.grid(row=5,column=1)

	def say_hi(self):
		print "Logging to " + self.username.get() 
		mail = Mail("192.168.180.11", port=587, username=self.username.get(), password=self.password.get(),
            use_tls=False, use_ssl=False, debug_level=1)
		mail.send_message("TEST Message", fromaddr=self.senderid.get(), to=self.receiverid.get(), body=self.message.get())

root = Tk()

app = App(root)

root.mainloop()
root.destroy() # optional; see description below