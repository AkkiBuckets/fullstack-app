import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext

# Function to scrape article names
def scrape_articles():
    url = "https://finance.yahoo.com/topic/latest-news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('h3')
    
    article_titles = [article.get_text() for article in articles]
    return article_titles

# Create the main window
root = tk.Tk()
root.title("Yahoo Finance Article Titles")

# Create a scrolled text widget
result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=20)
result_text.pack(padx=10, pady=10)

# Function to display articles
def display_articles():
    article_titles = scrape_articles()
    for title in article_titles:
        result_text.insert(tk.END, title + '\n\n')  # Add double space between titles

# Display articles immediately when the window opens
display_articles()

# Run the Tkinter event loop
root.mainloop()
