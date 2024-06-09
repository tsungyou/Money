import customtkinter as ctk
from src.Searcher import Searcher
from src.Backtester import Backtester
from src.Scraper import Scraper
from src.Strategy import Strategy

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("Stock Manager")
        self.geometry("1920x1080")

        # Create a Tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(expand=True, fill='both')


        # Add tabs
        self.tabview.add("代號搜尋")
        self.tabview.add("單日漲跌幅")

        self.tabview.add("策略因子")
        self.tabview.add("回測平台")
        # Create and place pages inside tabs
        self.home_page = Searcher(self.tabview.tab("代號搜尋"))
        self.home_page.pack(expand=True, fill='both')
        

        self.stock_info_page = Scraper(self.tabview.tab("單日漲跌幅"))
        self.stock_info_page.pack(expand=True, fill='both')

        self.portfolio_page = Strategy(self.tabview.tab("策略因子"))
        self.portfolio_page.pack(expand=True, fill='both')
        
        self.settings_page = Backtester(self.tabview.tab("回測平台"))
        self.settings_page.pack(expand=True, fill='both')
    
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self):
        self.destroy()
        self.quit()
        
if __name__ == "__main__":
    app = App()
    app.mainloop()

