import tkinter as tk
from tkinter import ttk
from utils import save_parameters_to_file, load_parameters_from_file


class TradingDashboardGUI:
    def __init__(self, root, strategies, update_interval=5000):
        self.root = root
        self.strategies = strategies
        self.update_interval = update_interval
        self.coin_widgets = {}

        default_parameters = {
            "BUY_MARGIN": 0.02,
            "SELL_MARGIN": 0.02,
            "TRADE_QUANTITY": 0.30,
        }
        loaded_parameters = load_parameters_from_file(default_parameters)
        self.parameters = {
            "BUY_MARGIN": tk.DoubleVar(value=loaded_parameters["BUY_MARGIN"]),
            "SELL_MARGIN": tk.DoubleVar(value=loaded_parameters["SELL_MARGIN"]),
            "TRADE_QUANTITY": tk.DoubleVar(value=loaded_parameters["TRADE_QUANTITY"]),
        }

        self.create_gui()
        self.update_dashboard()

    def create_gui(self):
        self.root.title("Crypto Trading Dashboard")
        self.root.geometry("800x900")

        ttk.Label(self.root, text="Crypto Trading Dashboard", font=("Helvetica", 16)).pack(pady=10)

        # Coin Frame
        self.coin_frame = ttk.Frame(self.root)
        self.coin_frame.pack(fill="both", expand=True)

        # Parameters Frame
        self.param_frame = ttk.LabelFrame(self.root, text="Adjust Parameters", padding=10)
        self.param_frame.pack(fill="x", padx=10, pady=10)

        # Add parameter controls
        for param, var in self.parameters.items():
            frame = ttk.Frame(self.param_frame)
            frame.pack(fill="x", pady=5)
            ttk.Label(frame, text=f"{param}:").pack(side="left", padx=5)
            ttk.Entry(frame, textvariable=var, width=10).pack(side="left", padx=5)

        ttk.Button(self.param_frame, text="Save Changes", command=self.save_parameters).pack(pady=5)

    def update_dashboard(self):
        for coin, strategy in self.strategies.items():
            try:
                bid, ask, current_price = strategy.fetch_and_update_prices()
                if not all((bid, ask, current_price)):
                    continue

                buy_threshold, sell_threshold = strategy.calculate_thresholds()
                if coin not in self.coin_widgets:
                    self.create_coin_widget(coin)

                # Update widgets
                self.coin_widgets[coin]["current_price"].config(text=f"Price: {current_price:.2f}")
                self.coin_widgets[coin]["buy_threshold"].config(text=f"Buy: {buy_threshold:.2f}")
                self.coin_widgets[coin]["sell_threshold"].config(text=f"Sell: {sell_threshold:.2f}")

            except Exception as e:
                print(f"Error updating {coin}: {e}")

        self.root.after(self.update_interval, self.update_dashboard)

    def create_coin_widget(self, coin):
        frame = ttk.LabelFrame(self.coin_frame, text=coin, padding=10)
        frame.pack(fill="x", pady=10)
        self.coin_widgets[coin] = {
            "current_price": ttk.Label(frame, text=""),
            "buy_threshold": ttk.Label(frame, text=""),
            "sell_threshold": ttk.Label(frame, text=""),
        }
        for widget in self.coin_widgets[coin].values():
            widget.pack(side="left", padx=5)

    def save_parameters(self):
        parameters_to_save = {param: var.get() for param, var in self.parameters.items()}
        save_parameters_to_file(parameters_to_save)