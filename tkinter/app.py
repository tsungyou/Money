import customtkinter as ctk
from src.HomePage import HomePage
from src.Screener import Screener
from src.Strategy import Strategy
from src.Cluster  import Cluster
import matplotlib
matplotlib.use("MacOSX")




class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Stock Manager")
        self.geometry("1920x1080")

        # Create a Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill='both')

        # Add tabs
        self.tabview.add("Home")
        self.tabview.add("Strategy")
        self.tabview.add("Cluster")
        self.tabview.add("Screener")

        # Create and place pages inside tabs
        self.home_page = HomePage(self.tabview.tab("Home"))
        self.home_page.pack(expand=True, fill='both')

        self.stock_info_page = Strategy(self.tabview.tab("Strategy"))
        self.stock_info_page.pack(expand=True, fill='both')

        self.portfolio_page = Cluster(self.tabview.tab("Cluster"))
        self.portfolio_page.pack(expand=True, fill='both')
        
        self.settings_page = Screener(self.tabview.tab("Screener"))
        self.settings_page.pack(expand=True, fill='both')
        
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
        self.destroy()
        self.quit()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
