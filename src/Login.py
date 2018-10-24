from Tkinter import *
from ttk import *
from crypto import Crypto
import CryptoCompareClient
import tkMessageBox
import UserManager
import Tkinter as tk

class LoginPage():
	def __init__(self, masterFrame, userManager):
		masterFrame.geometry("500x300")
		self.frame = masterFrame
		self.userManager = userManager
		self.frame.bind('<Return>', lambda event: self.login())

		Label(self.frame, text = "Login").pack()
		Label(self.frame, text = "Username").pack()
		self.usernameEntry = Entry(self.frame)
		self.passwordEntry = Entry(self.frame, show = "*")
		self.usernameEntry.pack()
		self.passwordEntry.pack()
		loginButton = Button(self.frame, text = "Login", command = self.login).pack()
		Button(self.frame, text = "Create Account", command = self.signUp).pack()

	def login(self):
		if self.userManager.validateUser(self.usernameEntry.get(), self.passwordEntry.get()):
			print "successful authentication"
			self.frame.destroy()
		else:
			tkMessageBox.showinfo("ERROR","Invalid username or password")

	def signUp(self):
		self.signUpPage = tk.Toplevel(self.frame)
		self.signUpPage.wm_title("Sign Up")
		self.signUpPage.geometry("300x300")
		Label(self.signUpPage, text = "Create Username: ").pack()
		self.signUpUsernameEntry = Entry(self.signUpPage)
		self.signUpUsernameEntry.pack()
		Label(self.signUpPage, text = "Enter Email: ").pack()
		self.signUpEmailEntry = Entry(self.signUpPage)
		self.signUpEmailEntry.pack()
		Label(self.signUpPage, text = "Create Password").pack()
		self.signUpPasswordEntry = Entry(self.signUpPage, show = "*")
		self.signUpPasswordEntry.pack()
		Label(self.signUpPage, text = "Confirm Password").pack()
		self.signUpPasswordConfirmEntry = Entry(self.signUpPage, show = "*")
		self.signUpPasswordConfirmEntry.pack()
		Button(self.signUpPage, text = "Confirm", command = self.validateEntries).pack()

	def validateEntries(self):
		username = self.signUpUsernameEntry.get()
		email = self.signUpEmailEntry.get()
		password = self.signUpPasswordEntry.get()
		confirm_password = self.signUpPasswordConfirmEntry.get()

		if self.userManager.validNewUser(username, email):
			if password == confirm_password:
				self.userManager.addNewUser(username, password, email)
				tkMessageBox.showinfo("Success","Account Created")
				self.signUpPage.destroy()
			else:
				tkMessageBox.showinfo("ERROR", "Please make sure passwords match.")
		else:
			tkMessageBox.showinfo("ERROR", "Username or email already exists.")



