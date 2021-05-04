# Name: OWfinder.py
# Author: Nick Mynatt
# Purpose: Called by OWmenu.py, uses chromedriver to open a player's overbuff.com stat page
# Last Modified: 4/16/20

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
import os

def findSR(name):     
    # Get path to chromedriver and open it
    path = os.path.dirname(os.path.abspath(__file__))
    path = path.replace(".Programs", "Utilities\\Chromedriver\\chromedriver.exe")
    driver = webdriver.Chrome(path)

    nameList = []
    nameList = name.split('#')

    driver.get("https://www.overbuff.com/players/pc/{}-{}".format(nameList[0], nameList[1]))

    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    elo = soup.find('span', attrs={'class':'player-skill-rating'})
    
    driver.close()
    return elo.text

def main():
    root = tk.Tk()
    inputName = tk.StringVar()
    tk.Entry(root, textvariable=inputName).grid(row=0,column=0)
    tk.Button(root, text="Find SR", command=findSR(inputName)).grid(row=0,column=1)
    root.mainloop()
    
if __name__ == "__main__":
    main()
