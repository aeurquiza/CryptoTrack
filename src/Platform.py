from coinbase.wallet.client import Client as CoinbaseClient
import Tkinter
import time
import threading
from Tkinter import *
from ttk import *
from crypto import Crypto
import CryptoCompareClient
import tkMessageBox
import os
import PlotGenerator

remove_ticker_entry = [6,1]

class CryptoGUI():
    graph_position = [0,5]
    THEME_COLOR = "#7befb2"

    def __init__(self, masterFrame, userManager):
        masterFrame.geometry("1000x600")

        #CONFIGS
        apiVersion = '2017-08-07'
        apiKey = "GENERIC"
        apiVal = "GENERIC"

        currency_fields = [1,1]
        new_ticker_entry = [4,1]
        save_button_position = []
        self.tracking_cryptos_chart = [1,3]
        self.threshold = .0001
        self.quotes_position_counter = 1
        self.currencyType = "USD"

        #Frames
        self.frame = masterFrame
        self.frame.configure( background=self.THEME_COLOR )
        self.tickerFrame = Tkinter.Frame( self.frame ) 
        self.tickerFrame.config( bg=self.THEME_COLOR )
        self.tickerFrame.grid( column = 1, row = 0, sticky= 'n', padx = (0,50))
        self.graphFrame = Tkinter.Frame( self.frame, width = 500, height = 500)
        self.graphFrame.grid( column = 5, row = 0)

        #Plot Generator
        self.plotGenerator = PlotGenerator.PlotGenerator(self.graphFrame)

        #Threads
        self.updatePricingThread = threading.Thread( target = self.updatePricesThreadWrapper, args = () )
        self.updatePricingThread.daemon = True

        #Clients
        self.client =  CoinbaseClient( apiKey , apiVal , api_version = apiVersion )
        self.cc_client = CryptoCompareClient.CryptoCompareClient()

        self.cryptosTracking = [Crypto('BTC',0),Crypto('USDT',0),Crypto('TRX',0),Crypto('XMR',0),Crypto('DASH',0)]  
        self.ticker_chart_labels = {}

        #Currency selection
        Tkinter.Label(self.tickerFrame, bg = self.THEME_COLOR, text = "Ticker Quotes" ).grid(row  = currency_fields[0], column = currency_fields[1])
        self.currency = Tkinter.Label( self.tickerFrame, bg = self.THEME_COLOR, text = "Currency")
        self.currency.grid(row = currency_fields[0]+1, column = currency_fields[1])

        self.currencySelectionVar = StringVar(self.tickerFrame)
        self.currencySelectionVar.set("USD")
        self.currencySelectionVar.trace('w', self.changeCurrency)
        self.currencySelectionDropdown = Combobox( self.tickerFrame, textvariable = self.currencySelectionVar, values = self.getCurrencyTypes())
        self.currencySelectionDropdown.grid(row = currency_fields[0]+2, column = currency_fields[1], padx = (5,0))

        self.BTCPriceLabel = Tkinter.Label(self.tickerFrame, bg = self.THEME_COLOR, text = "0.00")
        self.BTCPriceLabel.grid(row = currency_fields[0]+2, column = currency_fields[1]+1)

        #Enter new ticker to track
        Tkinter.Label(self.tickerFrame, bg = self.THEME_COLOR, text = "Enter new ticker to track:").grid( row = new_ticker_entry[0],  column = new_ticker_entry[1])
        self.ticker_entry =  Entry(self.tickerFrame)
        self.ticker_entry.grid(row = new_ticker_entry[0]+1, column = new_ticker_entry[1])
        Button(self.tickerFrame, text="Add Ticker", command=self.addCrypto).grid( row = new_ticker_entry[0]+1, column = new_ticker_entry[1]+1)

        #Remove Ticker
        Tkinter.Label(self.tickerFrame, bg = self.THEME_COLOR, text = "Enter ticker to remove:").grid( row = remove_ticker_entry[0],  column = remove_ticker_entry[1])
        self.remove_ticker_entry =  Entry(self.tickerFrame)
        self.remove_ticker_entry.grid(row = remove_ticker_entry[0]+1, column = remove_ticker_entry[1])
        Button(self.tickerFrame, text="Remove Ticker", command=self.removeCrypto).grid( row = remove_ticker_entry[0]+1, column = remove_ticker_entry[1]+1)

        #Cryptos Tracking
        Tkinter.Label(self.tickerFrame, bg = self.THEME_COLOR, font='Helvetica 12 bold', text = "            Cryptos").grid( row = self.tracking_cryptos_chart[0], column = self.tracking_cryptos_chart[1] )
        Tkinter.Label(self.tickerFrame, bg = self.THEME_COLOR, font='Helvetica 12 bold', text = "  Ticker       ").grid( row = self.tracking_cryptos_chart[0]+1, column = self.tracking_cryptos_chart[1])
        Tkinter.Label(self.tickerFrame, bg = self.THEME_COLOR, font='Helvetica 12 bold', text = "Price").grid( row = self.tracking_cryptos_chart[0]+1, column = self.tracking_cryptos_chart[1]+1)

        self.updatePricingThread.start()
        self.writeQuotes()

        #Graph Settings
        self.graphTickerSelectorVar = StringVar(self.graphFrame)
        cryptoNames = [ cryptoObject.get_ticker() for cryptoObject in self.cryptosTracking ]
        self.graphTickerSelector = OptionMenu(self.graphFrame, self.graphTickerSelectorVar, cryptoNames[0], *cryptoNames,
                                                         command = self.generatePlot ).grid( column = self.graph_position[0], row = self.graph_position[1], sticky = 'n' )

    def generatePlot(self):
        self.plotGenerator.generatePlot(self.graphTickerSelectorVar).get_tk_widget().grid( row = self.graph_position[0]+1, column = self.graph_position[1], pady = (20,0), sticky = 'n')

    def writeQuotes(self):
        for crypto in self.cryptosTracking:
            current_ticker = crypto.get_ticker()
            if current_ticker not in self.ticker_chart_labels:
                ticker_label_var = StringVar(self.tickerFrame, value = current_ticker)
                ticker_price_var = StringVar(self.tickerFrame, value = 0.0) 
                self.ticker_chart_labels[current_ticker] = { "TickerLabel":Tkinter.Label(self.tickerFrame, textvariable = ticker_label_var , font='Helvetica 12 bold', bg = self.THEME_COLOR ),
                             "TickerPrice":Tkinter.Label(self.tickerFrame, textvariable = ticker_price_var, font='Helvetica 12 bold', bg = self.THEME_COLOR ),
                            "TickerLabelVar":ticker_label_var, "TickerPriceVar":ticker_price_var}
                self.ticker_chart_labels[current_ticker]["TickerLabel"].grid( row = self.tracking_cryptos_chart[0]+1+ self.quotes_position_counter, column  = self.tracking_cryptos_chart[1])
                self.ticker_chart_labels[current_ticker]["TickerPrice"].grid( row  = self.tracking_cryptos_chart[0]+1+ self.quotes_position_counter, column = self.tracking_cryptos_chart[1]+1)
                self.quotes_position_counter +=1 
            else:
                self.ticker_chart_labels[current_ticker]["TickerPriceVar"].set(crypto.get_price())
        self.tickerFrame.after(1000, self.writeQuotes)

    def updatePrices(self):
        for crypto in self.cryptosTracking:
            new_price = self.cc_client.request_price(crypto.get_ticker(), self.currencySelectionVar.get())
            if crypto.price != 0.0 and new_price != crypto.price and (abs(crypto.price - new_price)/crypto.price > self.threshold): 
                self.alertRoutine(crypto.get_ticker())
            crypto.price = new_price


    def alertRoutine(self, crypto):
        alertMessageThread = threading.Thread( target = self.alertDialog, args = (crypto,))
        alertMessageThread.daemon = True
        alertSoundThread = threading.Thread( target = self.alertSound )
        alertSoundThread.daemon = True
        alertMessageThread.start()
        alertSoundThread.start()

    def alertDialog(self, crypto):
        tkMessageBox.showinfo("ALERT","%s has changed by more than %f%%"%(crypto, self.threshold*100))
    
    def alertSound(self):
        os.system('play --no-show-progress --null --channels 1 synth 1 sine 440')


    def updatePricesThreadWrapper(self):
        self.updatePrices()
        time.sleep(1)
        self.updatePricesThreadWrapper()

    def getPrice(self, crypto):
        return self.cc_client.request_price(crypto, self.currencySelectionVar.get())

    def addCrypto(self):
        crypto_name = self.ticker_entry.get()
        if crypto_name and crypto_name not in self.cryptosTracking:
            if self.getPrice(crypto_name) == 0.0:
                tkMessageBox.showinfo("ERROR","Coin does not exist.")
            else:
                self.cryptosTracking.append(Crypto(crypto_name,0))


    def getCurrencyTypes(self):
        currencyList = self.client.get_currencies()['data']
        return [ a['id'] for a in currencyList ]

    def removeCrypto(self):
        removing_ticker =  self.remove_ticker_entry.get()
        if removing_ticker in self.ticker_chart_labels:
            self.cryptosTracking = filter( lambda coin: coin.get_ticker() != removing_ticker, self.cryptosTracking)
            self.ticker_chart_labels[removing_ticker]["TickerLabel"].grid_forget()
            self.ticker_chart_labels[removing_ticker]["TickerPrice"].grid_forget()
            del self.ticker_chart_labels[removing_ticker]
            self.reframeQuotesChart()
        else:
            tkMessageBox.showinfo("ERROR","Not tracking that coin.")

    def reframeQuotesChart(self):
        self.quotes_position_counter = 1
        for crypto, props in self.ticker_chart_labels.iteritems():
            props["TickerLabel"].grid_forget()
            props["TickerPrice"].grid_forget()
            props["TickerLabel"].grid( row = self.tracking_cryptos_chart[0]+1+ self.quotes_position_counter, column  = self.tracking_cryptos_chart[1])
            props["TickerPrice"].grid( row = self.tracking_cryptos_chart[0]+1+ self.quotes_position_counter, column  = self.tracking_cryptos_chart[1]+1)
            self.quotes_position_counter+=1

    def changeCurrency(self, *args):    
        self.currencySelection = self.currencySelectionVar.get()
        self.rewritePrice()

    def rewritePrice(self):
        self.BTCPriceLabel.configure( text = self.getCoinPrice() )
        self.BTCPriceLabel.after(1000, self.rewritePrice )
