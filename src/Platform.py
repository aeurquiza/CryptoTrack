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

class CryptoGUI():

    graph_position = [0,5]
    remove_ticker_entry_position = [6,1]
    currency_fields_position = [1,1]
    new_ticker_entry_position = [4,1]
    tracking_cryptos_chart = [1,3]
    save_button_position = []

    THEME_COLOR = "#7befb2"

    def __init__(self, master_frame, user_manager):
        master_frame.geometry("1000x600")

        #CONFIGS
        apiVersion = '2017-08-07'
        apiKey = "GENERIC"
        apiVal = "GENERIC"

        self.threshold = .0001
        self.quotes_position_counter = 1
        self.currency_type = "USD"

        #Frames
        self.frame = master_frame
        self.frame.configure( background=self.THEME_COLOR )
        self.ticker_frame = Tkinter.Frame( self.frame ) 
        self.ticker_frame.config( bg=self.THEME_COLOR )
        self.ticker_frame.grid( column = 1, row = 0, sticky= 'n', padx = (0,50))
        self.graph_frame = Tkinter.Frame( self.frame, width = 500, height = 500)
        self.graph_frame.grid( column = 5, row = 0)

        #Threads
        self.update_pricing_thread = threading.Thread( target = self.update_prices_thread_wrapper, args = () )
        self.update_pricing_thread.daemon = True

        #Clients
        self.client =  CoinbaseClient( apiKey , apiVal , api_version = apiVersion )
        self.cc_client = CryptoCompareClient.CryptoCompareClient()

        #Plot Generator
        self.plot_generator = PlotGenerator.PlotGenerator(self.graph_frame, self.cc_client)

        self.cryptos_tracking = [Crypto('BTC',0),Crypto('USDT',0),Crypto('TRX',0),Crypto('XMR',0),Crypto('DASH',0)]  
        self.ticker_chart_labels = {}

        #Currency selection
        Tkinter.Label(self.ticker_frame, bg = self.THEME_COLOR, text = "Ticker Quotes" ).grid(row  = self.currency_fields_position[0], column = self.currency_fields_position[1])
        self.currency = Tkinter.Label( self.ticker_frame, bg = self.THEME_COLOR, text = "Currency")
        self.currency.grid(row = self.currency_fields_position[0]+1, column = self.currency_fields_position[1])

        self.currency_selection_var = StringVar(self.ticker_frame)
        self.currency_selection_var.set("USD")
        self.currency_selection_var.trace('w', self.change_currency)
        self.currency_selection_dropdown = Combobox( self.ticker_frame, textvariable = self.currency_selection_var, values = self.get_currency_types())
        self.currency_selection_dropdown.grid(row = self.currency_fields_position[0]+2, column = self.currency_fields_position[1], padx = (5,0))

        self.BTC_price_label = Tkinter.Label(self.ticker_frame, bg = self.THEME_COLOR, text = "0.00")
        self.BTC_price_label.grid(row = self.currency_fields_position[0]+2, column = self.currency_fields_position[1]+1)

        #Enter new ticker to track
        Tkinter.Label(self.ticker_frame, bg = self.THEME_COLOR, text = "Enter new ticker to track:").grid( row = self.new_ticker_entry_position[0],  column = self.new_ticker_entry_position[1])
        self.ticker_entry =  Entry(self.ticker_frame)
        self.ticker_entry.grid(row = self.new_ticker_entry_position[0]+1, column = self.new_ticker_entry_position[1])
        Button(self.ticker_frame, text="Add Ticker", command=self.add_crypto).grid( row = self.new_ticker_entry_position[0]+1, column = self.new_ticker_entry_position[1]+1)

        #Remove Ticker
        Tkinter.Label(self.ticker_frame, bg = self.THEME_COLOR, text = "Enter ticker to remove:").grid( row = self.remove_ticker_entry_position[0],  column = self.remove_ticker_entry_position[1])
        self.remove_ticker_entry =  Entry(self.ticker_frame)
        self.remove_ticker_entry.grid(row = self.remove_ticker_entry_position[0]+1, column = self.remove_ticker_entry_position[1])
#        Button(self.ticker_frame, text="Remove Ticker", command=self.remove_crypto).grid( row = self.remove_ticker_entry_position[0]+1, column = self.remove_ticker_entry_position[1]+1)

        #Cryptos Tracking
        Tkinter.Label(self.ticker_frame, bg = self.THEME_COLOR, font='Helvetica 12 bold', text = "            Cryptos").grid( row = self.tracking_cryptos_chart[0], column = self.tracking_cryptos_chart[1] )
        Tkinter.Label(self.ticker_frame, bg = self.THEME_COLOR, font='Helvetica 12 bold', text = "  Ticker       ").grid( row = self.tracking_cryptos_chart[0]+1, column = self.tracking_cryptos_chart[1])
        Tkinter.Label(self.ticker_frame, bg = self.THEME_COLOR, font='Helvetica 12 bold', text = "Price").grid( row = self.tracking_cryptos_chart[0]+1, column = self.tracking_cryptos_chart[1]+1)

        self.update_pricing_thread.start()
        self.write_quotes()

        #Graph Settings
        self.graph_ticker_selector_var = StringVar(self.graph_frame)
        crypto_names = [ cryptoObject.get_ticker() for cryptoObject in self.cryptos_tracking ]
        self.graph_ticker_selector = OptionMenu(self.graph_frame, self.graph_ticker_selector_var, crypto_names[0], *crypto_names,
                                                         command = self.generate_plot ).grid( column = self.graph_position[0], row = self.graph_position[1], sticky = 'n' )

    def generate_plot(self):
        self.plot_generator.generate(self.graph_ticker_selector_var.get(), self.currency_selection_var.get(), 
                                                   60 ).get_tk_widget().grid( row = self.graph_position[0]+1, column = self.graph_position[1], pady = (20,0), sticky = 'n')

    def write_quotes(self):
        for crypto in self.cryptos_tracking:
            current_ticker = crypto.get_ticker()
            if current_ticker not in self.ticker_chart_labels:
                ticker_label_var = StringVar(self.ticker_frame, value = current_ticker)
                ticker_price_var = StringVar(self.ticker_frame, value = 0.0) 
                self.ticker_chart_labels[current_ticker] = { "TickerLabel":Tkinter.Label(self.ticker_frame, textvariable = ticker_label_var , font='Helvetica 12 bold', bg = self.THEME_COLOR ),
                             "TickerPrice":Tkinter.Label(self.ticker_frame, textvariable = ticker_price_var, font='Helvetica 12 bold', bg = self.THEME_COLOR ),
                            "TickerLabelVar":ticker_label_var, "TickerPriceVar":ticker_price_var}
                self.ticker_chart_labels[current_ticker]["TickerLabel"].grid( row = self.tracking_cryptos_chart[0]+1+ self.quotes_position_counter, column  = self.tracking_cryptos_chart[1])
                self.ticker_chart_labels[current_ticker]["TickerPrice"].grid( row  = self.tracking_cryptos_chart[0]+1+ self.quotes_position_counter, column = self.tracking_cryptos_chart[1]+1)
                self.quotes_position_counter +=1 
            else:
                self.ticker_chart_labels[current_ticker]["TickerPriceVar"].set(crypto.get_price())
        self.ticker_frame.after(1000, self.write_quotes)

    def update_prices(self):
        for crypto in self.cryptos_tracking:
            new_price = self.cc_client.request_price(crypto.get_ticker(), self.currency_selection_var.get())
            if crypto.price != 0.0 and new_price != crypto.price and (abs(crypto.price - new_price)/crypto.price > self.threshold): 
                self.alert_routine(crypto.get_ticker())
            crypto.price = new_price


    def alert_routine(self, crypto):
        alert_message_thread = threading.Thread( target = self.alert_dialog, args = (crypto,))
        alert_message_thread.daemon = True
        alert_sound_thread = threading.Thread( target = self.alert_sound )
        alert_sound_thread.daemon = True
        alert_message_thread.start()
        alert_sound_thread.start()

    def alert_dialog(self, crypto):
        tkMessageBox.showinfo("ALERT","%s has changed by more than %f%%"%(crypto, self.threshold*100))
    
    def alert_sound(self):
        os.system('play --no-show-progress --null --channels 1 synth 1 sine 440')


    def update_prices_thread_wrapper(self):
        self.update_prices()
        time.sleep(1)
        self.update_prices_thread_wrapper()

    def get_price(self, crypto):
        return self.cc_client.request_price(crypto, self.currency_selection_var.get())

    def add_crypto(self):
        crypto_name = self.ticker_entry.get()
        if crypto_name and crypto_name not in self.cryptos_tracking:
            if self.get_price(crypto_name) == 0.0:
                tkMessageBox.showinfo("ERROR","Coin does not exist.")
            else:
                self.cryptos_tracking.append(Crypto(crypto_name,0))


    def get_currency_types(self):
        currency_list = self.client.get_currencies()['data']
        return [ a['id'] for a in currency_list ]

    def remove_crypto(self):
        removing_ticker =  self.remove_ticker_entry_position.get()
        if removing_ticker in self.ticker_chart_labels:
            self.cryptos_tracking = filter( lambda coin: coin.get_ticker() != removing_ticker, self.cryptos_tracking)
            self.ticker_chart_labels[removing_ticker]["TickerLabel"].grid_forget()
            self.ticker_chart_labels[removing_ticker]["TickerPrice"].grid_forget()
            del self.ticker_chart_labels[removing_ticker]
            self.reframe_quotes_chart()
        else:
            tkMessageBox.showinfo("ERROR","Not tracking that coin.")

    def reframe_quotes_chart(self):
        self.quotes_position_counter = 1
        for crypto, props in self.ticker_chart_labels.iteritems():
            props["TickerLabel"].grid_forget()
            props["TickerPrice"].grid_forget()
            props["TickerLabel"].grid( row = self.tracking_cryptos_chart[0]+1+ self.quotes_position_counter, column  = self.tracking_cryptos_chart[1])
            props["TickerPrice"].grid( row = self.tracking_cryptos_chart[0]+1+ self.quotes_position_counter, column  = self.tracking_cryptos_chart[1]+1)
            self.quotes_position_counter+=1

    def change_currency(self, *args):
        self.generate_plot()
        self.currency_selection = self.currency_selection_var.get()

