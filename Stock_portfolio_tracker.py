import yfinance as yf
import tkinter as tk
from tkinter import messagebox, filedialog
import csv

class StockPortfolio:
    def __init__(self):
        """
        Initialize an empty portfolio.
        """
        self.portfolio = {}

    def add_stock(self, symbol, shares):
        """
        Add a stock to the portfolio.
        
        :param symbol: Stock symbol (e.g., "AAPL").
        :param shares: Number of shares to add.
        :return: True if successful, False otherwise.
        """
        symbol = symbol.upper()
        try:
            stock = yf.Ticker(symbol)
            price = stock.history(period="1d")["Close"].iloc[-1]  # Fetch current price
            if symbol in self.portfolio:
                self.portfolio[symbol] += shares
            else:
                self.portfolio[symbol] = shares
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def remove_stock(self, symbol):
        """
        Remove a stock from the portfolio.
        
        :param symbol: Stock symbol (e.g., "AAPL").
        :return: True if successful, False otherwise.
        """
        symbol = symbol.upper()
        if symbol in self.portfolio:
            del self.portfolio[symbol]
            return True
        else:
            return False

    def view_portfolio(self):
        """
        Get the current portfolio with real-time stock data.
        
        :return: A dictionary containing portfolio details.
        """
        portfolio_details = {
            "stocks": [],
            "total_investment": 0,
            "total_value": 0,
            "profit_loss": 0,
            "percentage_change": 0
        }

        for symbol, shares in self.portfolio.items():
            try:
                stock = yf.Ticker(symbol)
                price = stock.history(period="1d")["Close"].iloc[-1]
                value = price * shares
                portfolio_details["stocks"].append({
                    "symbol": symbol,
                    "shares": shares,
                    "price": price,
                    "value": value
                })
                portfolio_details["total_investment"] += price * shares
                portfolio_details["total_value"] += value
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")

        portfolio_details["profit_loss"] = portfolio_details["total_value"] - portfolio_details["total_investment"]
        if portfolio_details["total_investment"] > 0:
            portfolio_details["percentage_change"] = (portfolio_details["profit_loss"] / portfolio_details["total_investment"]) * 100

        return portfolio_details

    def export_to_csv(self, filename):
        """
        Export the portfolio data to a CSV file.
        
        :param filename: Name of the CSV file.
        """
        portfolio_details = self.view_portfolio()
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Symbol", "Shares", "Price ($)", "Value ($)"])
            for stock in portfolio_details["stocks"]:
                writer.writerow([stock["symbol"], stock["shares"], stock["price"], stock["value"]])
            writer.writerow([])
            writer.writerow(["Total Investment", portfolio_details["total_investment"]])
            writer.writerow(["Total Value", portfolio_details["total_value"]])
            writer.writerow(["Profit/Loss", portfolio_details["profit_loss"]])
            writer.writerow(["Percentage Change", portfolio_details["percentage_change"]])


class StockPortfolioApp:
    def __init__(self, root):
        """
        Initialize the Stock Portfolio Tracker GUI.
        
        :param root: The root window of the application.
        """
        self.root = root
        self.root.title("Stock Portfolio Tracker")
        self.root.geometry("600x400")

        self.portfolio = StockPortfolio()

        # Login Frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, padx=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, padx=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5)

        tk.Button(self.login_frame, text="Login", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)

        # Main Frame (hidden until login)
        self.main_frame = tk.Frame(self.root)

        tk.Label(self.main_frame, text="Stock Symbol:").grid(row=0, column=0, padx=5)
        self.symbol_entry = tk.Entry(self.main_frame)
        self.symbol_entry.grid(row=0, column=1, padx=5)

        tk.Label(self.main_frame, text="Shares:").grid(row=1, column=0, padx=5)
        self.shares_entry = tk.Entry(self.main_frame)
        self.shares_entry.grid(row=1, column=1, padx=5)

        tk.Button(self.main_frame, text="Add Stock", command=self.add_stock).grid(row=2, column=0, padx=5, pady=10)
        tk.Button(self.main_frame, text="Remove Stock", command=self.remove_stock).grid(row=2, column=1, padx=5, pady=10)
        tk.Button(self.main_frame, text="View Portfolio", command=self.view_portfolio).grid(row=3, column=0, padx=5, pady=10)
        tk.Button(self.main_frame, text="Export to CSV", command=self.export_to_csv).grid(row=3, column=1, padx=5, pady=10)
        tk.Button(self.main_frame, text="Logout", command=self.logout).grid(row=4, column=0, columnspan=2, pady=10)

        # Portfolio Display
        self.portfolio_text = tk.Text(self.main_frame, height=10, width=50)
        self.portfolio_text.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def login(self):
        """
        Handle user login.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Simple authentication (for demonstration purposes)
        if username == "user" and password == "password":
            self.login_frame.pack_forget()
            self.main_frame.pack(pady=20)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def logout(self):
        """
        Handle user logout.
        """
        self.main_frame.pack_forget()
        self.login_frame.pack(pady=20)
        self.portfolio = StockPortfolio()  # Reset portfolio

    def add_stock(self):
        """
        Add a stock to the portfolio.
        """
        symbol = self.symbol_entry.get()
        shares = self.shares_entry.get()

        if not symbol or not shares:
            messagebox.showerror("Error", "Please enter both stock symbol and shares.")
            return

        try:
            shares = int(shares)
            if shares <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Shares must be a positive integer.")
            return

        if self.portfolio.add_stock(symbol, shares):
            messagebox.showinfo("Success", f"Added {shares} shares of {symbol} to the portfolio.")
        else:
            messagebox.showerror("Error", "Failed to add stock. Please check the symbol and try again.")

    def remove_stock(self):
        """
        Remove a stock from the portfolio.
        """
        symbol = self.symbol_entry.get()

        if not symbol:
            messagebox.showerror("Error", "Please enter a stock symbol.")
            return

        if self.portfolio.remove_stock(symbol):
            messagebox.showinfo("Success", f"Removed {symbol} from the portfolio.")
        else:
            messagebox.showerror("Error", f"{symbol} not found in the portfolio.")

    def view_portfolio(self):
        """
        Display the current portfolio.
        """
        portfolio_details = self.portfolio.view_portfolio()
        self.portfolio_text.delete(1.0, tk.END)

        if not portfolio_details["stocks"]:
            self.portfolio_text.insert(tk.END, "Your portfolio is empty.")
            return

        self.portfolio_text.insert(tk.END, "Stock Portfolio:\n")
        self.portfolio_text.insert(tk.END, "-" * 50 + "\n")
        self.portfolio_text.insert(tk.END, f"{'Symbol':<10}{'Shares':<10}{'Price ($)':<15}{'Value ($)':<15}\n")
        self.portfolio_text.insert(tk.END, "-" * 50 + "\n")

        for stock in portfolio_details["stocks"]:
            self.portfolio_text.insert(tk.END, f"{stock['symbol']:<10}{stock['shares']:<10}{stock['price']:<15.2f}{stock['value']:<15.2f}\n")

        self.portfolio_text.insert(tk.END, "-" * 50 + "\n")
        self.portfolio_text.insert(tk.END, f"Total Investment: ${portfolio_details['total_investment']:.2f}\n")
        self.portfolio_text.insert(tk.END, f"Total Value: ${portfolio_details['total_value']:.2f}\n")
        self.portfolio_text.insert(tk.END, f"Profit/Loss: ${portfolio_details['profit_loss']:.2f}\n")
        self.portfolio_text.insert(tk.END, f"Percentage Change: {portfolio_details['percentage_change']:.2f}%\n")
        self.portfolio_text.insert(tk.END, "-" * 50 + "\n")

    def export_to_csv(self):
        """
        Export the portfolio data to a CSV file.
        """
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            self.portfolio.export_to_csv(filename)
            messagebox.showinfo("Success", f"Portfolio data exported to {filename}.")


if __name__ == "__main__":
    root = tk.Tk()
    app = StockPortfolioApp(root)
    root.mainloop()