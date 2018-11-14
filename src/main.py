import Platform
import Login
import UserManager
import Tkinter
from ttk import *

if __name__=="__main__":
	userManager = UserManager.UserManager()
	if not userManager.validateUser('aurqui8','aeurquiza'):
		loginroot = Tkinter.Tk()
		loginroot.style = Style()
		loginroot.style.theme_use("clam")
		LoginPage = Login.LoginPage(loginroot, userManager)
		loginroot.mainloop()

	if userManager.userLoggedIn():
		CryptoGuiRoot = Tkinter.Tk()
		CryptoGuiRoot.style = Style()
		CryptoGuiRoot.style.theme_use("clam")
		PlatformPage = Platform.CryptoGUI(CryptoGuiRoot, userManager)
		CryptoGuiRoot.mainloop()
		CryptoGuiRoot.destroy()
		
	loginroot.destroy()

