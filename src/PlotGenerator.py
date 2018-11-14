from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import Tkinter


class PlotGenerator():
	def __init__(self,root, cc_client):
		self.root = root
		self.cc_client = cc_client

	def generate(self, ticker, currency, limit):
		histo = self.cc_client.request_historical(ticker,currency,limit)
		fig = Figure(figsize=(5, 4), dpi=100)
		t = np.arange(0, 60)
		fig.add_subplot(111).plot(t, histo)

		canvas = FigureCanvasTkAgg(fig, master=self.root)  # A tk.DrawingArea.
		canvas.draw()
		return canvas
