import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------- MAIN APP ----------------
class StockPredictorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("📈 Stock Price Predictor (Tkinter)")
        self.geometry("950x680")
        self.resizable(False, False)

        self.create_widgets()

    # ---------------- UI ----------------
    def create_widgets(self):
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="x")

        ttk.Label(frame, text="Stock Ticker:").grid(row=0, column=0, sticky="w")
        self.ticker_entry = ttk.Entry(frame, width=15)
        self.ticker_entry.insert(0, "META")
        self.ticker_entry.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Forecast Days:").grid(row=0, column=2, sticky="w")
        self.forecast_spin = ttk.Spinbox(frame, from_=7, to=90, width=8)
        self.forecast_spin.set(30)
        self.forecast_spin.grid(row=0, column=3, padx=5)

        ttk.Label(frame, text="Model:").grid(row=0, column=4, sticky="w")
        self.model_choice = ttk.Combobox(
            frame,
            values=["Linear Regression", "Support Vector Regression (RBF)"],
            state="readonly",
            width=30
        )
        self.model_choice.set("Linear Regression")
        self.model_choice.grid(row=0, column=5, padx=5)

        ttk.Button(frame, text="Run Prediction", command=self.run_prediction)\
            .grid(row=0, column=6, padx=10)

        # Output info
        self.info_label = ttk.Label(self, text="", foreground="blue")
        self.info_label.pack(pady=5)

        # ✅ Table now includes DATE column
        self.table = ttk.Treeview(
            self,
            columns=("Day", "Date", "Predicted Close"),
            show="headings",
            height=8
        )
        self.table.heading("Day", text="Day")
        self.table.heading("Date", text="Date")
        self.table.heading("Predicted Close", text="Predicted Close")
        self.table.pack(padx=20, pady=10, fill="x")

        # Chart area
        self.chart_frame = ttk.Frame(self)
        self.chart_frame.pack(fill="both", expand=True)

    # ---------------- LOGIC ----------------
    def run_prediction(self):
        ticker = self.ticker_entry.get().strip().upper()
        forecast_out = int(self.forecast_spin.get())
        model_type = self.model_choice.get()

        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period="max")

            if df.empty:
                messagebox.showerror("Error", "No data found for this ticker.")
                return

            df = df[['Close']]
            df['Prediction'] = df['Close'].shift(-forecast_out)

            X = np.array(df.drop(columns=['Prediction']))[:-forecast_out]
            y = np.array(df['Prediction'])[:-forecast_out]

            x_train, x_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

            if model_type == "Linear Regression":
                model = LinearRegression()
            else:
                model = SVR(kernel='rbf', C=1e3, gamma=0.1)

            model.fit(x_train, y_train)
            confidence = model.score(x_test, y_test)

            x_forecast = np.array(df.drop(columns=['Prediction'])[-forecast_out:])
            predictions = model.predict(x_forecast)

            # ✅ Generate real forecast dates
            last_date = df.index[-1]
            future_dates = pd.date_range(
                start=last_date,
                periods=forecast_out + 1,
                freq="B"
            )[1:]

            self.info_label.config(
                text=f"Model: {model_type} | R² Score: {confidence:.3f}"
            )

            self.update_table(predictions, future_dates)
            self.update_chart(df, predictions, future_dates)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- TABLE ----------------
    def update_table(self, predictions, future_dates):
        for row in self.table.get_children():
            self.table.delete(row)

        for i, (date, value) in enumerate(zip(future_dates, predictions), start=1):
            self.table.insert(
                "",
                "end",
                values=(i, date.date(), f"{value:.2f}")
            )

    # ---------------- CHART ----------------
    def update_chart(self, df, predictions, future_dates):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        forecast_df = pd.DataFrame(
            predictions,
            index=future_dates,
            columns=["Predicted Close"]
        )

        fig, ax = plt.subplots(figsize=(8, 4))

        df["Close"].tail(200).plot(
            ax=ax,
            label="Historical Close",
            color="steelblue"
        )

        forecast_df["Predicted Close"].plot(
            ax=ax,
            label="Forecast",
            color="red",
            marker="o"
        )

        # ✅ Label only the LAST forecast point (with date context)
        last_date = forecast_df.index[-1]
        last_price = forecast_df["Predicted Close"].iloc[-1]

        ax.annotate(
            f"{last_date.date()}\n{last_price:.2f}",
            (last_date, last_price),
            textcoords="offset points",
            xytext=(0, 12),
            ha="center",
            fontsize=9,
            fontweight="bold",
            color="red"
        )

        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app = StockPredictorApp()
    app.mainloop()