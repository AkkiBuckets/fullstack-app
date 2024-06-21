import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import mplfinance as mpf
import openai
import base64
import tkinter as tk
from tkinter import Label, Text, Scrollbar, Entry, Button
from PIL import Image, ImageTk
import logging
import ta

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# OpenAI API key
openai.api_key = 'sk-proj-18nozHrAveRdu6zDQarpT3BlbkFJ84CfWjoNNAVcpWlUt3nm'

# Fetch historical data using yfinance
def get_historical_data(symbol, period='5d', timeframe='1h'):
    try:
        logging.info(f"Fetching historical data for {symbol} for the last {period}")
        data = yf.download(symbol, period=period, interval=timeframe)
        if data.empty:
            logging.warning(f"No data found for {symbol}")
            return None
        data = data.rename(columns={"Open": "Open", "High": "High", "Low": "Low", "Close": "Close", "Volume": "Volume"})
        return data
    except Exception as e:
        logging.warning(f"Failed to fetch historical data for {symbol}: {e}")
        return None

# Plot candlestick chart
def plot_candlestick_chart(data, symbol, indicator=None):
    try:
        save_path = f"{symbol}_chart.png"
        logging.info(f"Plotting candlestick chart for {symbol}")
        additional_plots = []
        data = data.copy()  # Ensure we are working with a copy of the DataFrame
        if indicator is not None:
            if 'SMA' in indicator:
                data['SMA'] = ta.trend.sma_indicator(data['Close'], window=20)
                additional_plots.append(mpf.make_addplot(data['SMA']))
            elif 'EMA' in indicator:
                data['EMA'] = ta.trend.ema_indicator(data['Close'], window=20)
                additional_plots.append(mpf.make_addplot(data['EMA']))
            elif 'MACD' in indicator:
                macd = ta.trend.macd(data['Close'])
                macd_signal = ta.trend.macd_signal(data['Close'])
                additional_plots.append(mpf.make_addplot(macd, panel=1))
                additional_plots.append(mpf.make_addplot(macd_signal, panel=1))
            elif 'BB' in indicator:
                data['BB_High'] = ta.volatility.bollinger_hband(data['Close'])
                data['BB_Low'] = ta.volatility.bollinger_lband(data['Close'])
                additional_plots.append(mpf.make_addplot(data['BB_High']))
                additional_plots.append(mpf.make_addplot(data['BB_Low']))
        mpf.plot(data, type='candle', style='charles', title=f'{symbol} Candlestick Chart', ylabel='Price', savefig=save_path, addplot=additional_plots)
        return save_path
    except Exception as e:
        logging.error(f"Failed to plot candlestick chart for {symbol}: {e}")
        return None

# Encode image to base64
def encode_image(save_path):
    try:
        with open(save_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Failed to encode image {save_path}: {e}")
        return None

# Analyze chart with GPT-4o
def analyze_chart_with_gpt4o(encoded_image, symbol, custom_prompt):
    try:
        prompt = f"{custom_prompt}\n![chart](data:image/png;base64,{encoded_image})"
        logging.info(f"Sending analysis request to GPT-4o for {symbol}")
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        analysis = response.choices[0].message['content'].strip()
        logging.info(f"Received analysis from GPT-4o for {symbol}")
        return analysis
    except Exception as e:
        logging.error(f"Failed to analyze with GPT-4o: {e}")
        return None

# Display result in a new Tkinter window
def display_result(image_path, analysis, symbol, data):
    result_root = tk.Toplevel()  # Create a new window
    result_root.title("Candlestick Chart Analysis")

    img = Image.open(image_path)
    img = img.resize((800, 600), Image.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)

    label_img = Label(result_root, image=img_tk)
    label_img.image = img_tk  # Keep a reference to avoid garbage collection
    label_img.pack()

    def show_indicator(indicator):
        chart_path = plot_candlestick_chart(data, symbol, indicator)
        if chart_path:
            new_img = Image.open(chart_path)
            new_img = new_img.resize((800, 600), Image.LANCZOS)
            new_img_tk = ImageTk.PhotoImage(new_img)
            label_img.config(image=new_img_tk)
            label_img.image = new_img_tk

    button_frame = tk.Frame(result_root)
    button_frame.pack()

    indicators = ['SMA', 'EMA', 'MACD', 'BB']
    for ind in indicators:
        button = Button(button_frame, text=f"Show {ind}", command=lambda ind=ind: show_indicator(ind))
        button.pack(side=tk.LEFT)

    text_frame = tk.Frame(result_root)
    text_frame.pack(fill=tk.BOTH, expand=True)

    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_analysis = Text(text_frame, wrap='word', yscrollcommand=scrollbar.set)
    text_analysis.insert('1.0', analysis)
    text_analysis.pack(fill=tk.BOTH, expand=True)

    scrollbar.config(command=text_analysis.yview)
    result_root.mainloop()

# Handle user input and display chart and analysis for assets
def handle_asset_input(symbol):
    data = get_historical_data(symbol, period='5d', timeframe='1h')
    if data is not None and not data.empty:
        # Filter the data to the last trading hours
        last_trading_hours = data.between_time('09:30', '16:00')
        if not last_trading_hours.empty:
            data = last_trading_hours.tail(48)  # Get the last two days of trading hours

        chart_path = plot_candlestick_chart(data, symbol)
        if chart_path:
            encoded_image = encode_image(chart_path)
            if encoded_image:
                analysis = analyze_chart_with_gpt4o(encoded_image, symbol, f"Analyze this chart for {symbol}. Provide a discussion on the price action.")
                if analysis:
                    display_result(chart_path, analysis, symbol, data)
                else:
                    logging.error(f"Analysis failed for {symbol}")
            else:
                logging.error(f"Image encoding failed for {symbol}")
        else:
            logging.error(f"Chart plotting failed for {symbol}")
    else:
        logging.info(f"No historical data to display for {symbol}")

# Create Tkinter window for user input
def create_main_input_window():
    input_root = tk.Tk()
    input_root.title("Trading App")

    # Asset input
    label_asset = Label(input_root, text="Enter Asset Symbol:")
    label_asset.pack()
    entry_asset = Entry(input_root)
    entry_asset.pack()
    submit_button_asset = Button(input_root, text="Submit Asset", command=lambda: handle_asset_input(entry_asset.get().upper()))
    submit_button_asset.pack()

    input_root.mainloop()

if __name__ == '__main__':
    # Step 1: Create the main input window
    create_main_input_window()
