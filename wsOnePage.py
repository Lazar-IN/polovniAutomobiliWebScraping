# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 16:19:33 2023
@author: ProBook
"""

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List
import csv
import pandas as pd
import time

@dataclass
class Car:
    link: str
    full_name: str
    year: int
    kw: int
    horsepower: int
    body: str
    fuel: str
    engine_size_cm3: int
    price_eur: int
    

def scrape_cars():
    # Configure Selenium WebDriver
    driver = webdriver.Chrome()  # Replace with the path to your chromedriver executable
    
    # URL for car search
    url = "https://www.polovniautomobili.com/auto-oglasi/pretraga?brand=&price_to=&year_from=2015&year_to=2020&chassis%5B%5D=2631&showOldNew=all&submit_1=&without_price=1"
    
    
    # Send a GET request to the website
    driver.get(url)
    #time.sleep(2)
    html = driver.page_source
    #print(driver.page_source)
    
    # Create a BeautifulSoup object with the HTML content
    soup = BeautifulSoup(html, "html.parser")
    
    # Find the car listings on the page
    car_listings = soup.find_all("div", class_="textContent")
    
    # List to store car objects
    cars = []
    
    # Extract information from each car listing
    for car in car_listings:
        #print(car)  # Print the car listing HTML to inspect its structure
        
        # Extract the information using the correct class names
        link = "https://www.polovniautomobili.com"+car.find("a", class_="ga-title")["href"]
        full_name = car.find("a", class_="ga-title").text.strip()
        year = int((car.find("div", class_="top").text.strip()).split('.',1)[0])
        kw = int((car.find("div", class_="bottom uk-hidden-medium uk-hidden-small").text.strip()).split('k',1)[0])
        horsepower = int(((car.find("div", class_="bottom uk-hidden-medium uk-hidden-small").text.strip()).split('K',1)[0]).split('(',1)[1])
        body = ((car.find("div", class_="top").text.strip()).split('.',1)[1]).split(' ',1)[1]
        fuel = ((car.find("div", class_="bottom").text.strip()).split('|',1)[0]).split(' ',1)[0]
        engine_size = (((car.find("div", class_="bottom").text.strip()).split('|',1)[1]).split(' ',1)[1]).split(' ',1)[0]
        priceTemp = car.find("div", class_="price")
        priceTemp2 = (priceTemp.text.strip()).split(' ',1)[0] if priceTemp else "N/A"
        if priceTemp2 == 'Po':
            price_eur = None
        else:
            price_eur = priceTemp2
        # Create a Car object and add it to the list
        #cars.append(Car(link, full_name, year, km, body, fuel, engine_size, price_eur))
        cars.append(Car(link, full_name, year, kw, horsepower, body, fuel, engine_size, price_eur))

    
    # Close the Selenium WebDriver
    driver.quit()
    
    # Convert car objects to dataframe
    df = pd.DataFrame(cars)
    # Print head(2) of dataframe
    print(df.head(2))
    # Export dataframe to csv file
    df.to_csv('outFromSinglePages.csv', index=False)
    
    print("Scraping completed. Car listings saved in outFromSinglePages.csv.")


    
    
# Execute the scraping function
scrape_cars()

