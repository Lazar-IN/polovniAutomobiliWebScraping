# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 16:19:33 2023
@author: ProBook
"""
#get hatchback cars data from polovniautomobili.com
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List
import csv
import pandas as pd
import time

#Define parameters
fromYear = '2021'
toYear = '2022'
withoutPrice = '0'
specifyNumOfPagesFlag = '1'
specificNumOfPages= 2

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
    
    # Base URL for car search
    base_url = "https://www.polovniautomobili.com/auto-oglasi/pretraga?"
    #Tpage = ""
    Tsort = "&sort=basic"
    TyearFrom = "&year_from="+fromYear
    TyearTo = "&year_to="+toYear
    Tchassis = "&chassis%5B0%5D=2631"
    TcityDistance = "&city_distance=0"
    TshowOldNew = "&showOldNew=all"
    TwithoutPrice = "&without_price="+withoutPrice
    
    #Geting number of pages
    url = base_url+"page="+str(1)+Tsort+TyearFrom+TyearTo+Tchassis+TcityDistance+TshowOldNew+TwithoutPrice
    driver.get(url)
    lss = (driver.find_element("xpath",'/html/body/div[9]/div[2]/div[2]/div[1]/div[2]/small[1]')).text.strip()
    #print(lss)
    np = lss.split('ukupno ',1)[1]
    #print(np)
    npp = int(int(np)/25)
    #print(npp)
    
    # Number of pages to scrape
    if specifyNumOfPagesFlag == '1':
        num_pages = specificNumOfPages
        print("Getting data from "+str(specificNumOfPages)+" pages...")
    else:
        if npp>1:
            num_pages = npp
            print("Getting data from "+str(npp)+" pages...")
        else:
            num_pages = 1 
            print("Getting data from only one page...")
    
    # List to store car objects
    cars = []
    
    for page in range(1, num_pages + 1):
        # Set the page parameter
        url = base_url+"page="+str(page)+Tsort+TyearFrom+TyearTo+Tchassis+TcityDistance+TshowOldNew+TwithoutPrice
        
        driver.get(url)
        #time.sleep(2)
        html = driver.page_source
        #print(driver.page_source)
        
        # Create a BeautifulSoup object with the HTML content
        soup = BeautifulSoup(html, "html.parser")
        
        # Find the car listings on the page
        car_listings = soup.find_all("div", class_="textContent")
        
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
            fuel = ((car.find("div", class_="bottom").text.strip()).split('|', 1)[0]).split(' ', 1)[0]
    
            try:
                engine_size_element = car.find("div", class_="bottom").text.strip().split('|', 1)[1].split(' ', 1)
                #engine_size = engine_size_element[1] if len(engine_size_element) > 1 else None
                if len(engine_size_element) > 1 :
                    engine_size_temp = engine_size_element[1]
                    engine_size = engine_size_temp.split(' ',1)[0]
                else:
                    None
            except IndexError:
                engine_size = None
    
            priceTemp = car.find("div", class_="price")
            priceTemp2 = (priceTemp.text.strip()).split(' ',1)[0] if priceTemp else "N/A"
            if priceTemp2 == 'Po':
                price_eur = None
            else:
                price_eur = priceTemp2
            # Create a Car object and add it to the list
            #cars.append(Car(link, full_name, year, km, body, fuel, engine_size, price_eur))
            cars.append(Car(link, full_name, year, kw, horsepower, body, fuel,engine_size, price_eur))
            

        # Add a delay between page requests to avoid overwhelming the server
        print("Added cars from page:"+str(page))
        time.sleep(0.1)
    
    # Close the Selenium WebDriver
    driver.quit()
    
    # Convert car objects to dataframe
    df = pd.DataFrame(cars)
    
    # Print head(2) of dataframe
    #print(df.head(2))
    
    # Export dataframe to csv file
    df.to_csv('outFromMultiplePagesV02.csv', index=False)
    
    print("Scraping completed. Car listings saved in outFromMultiplePagesV02.csv.")


# Execute the scraping function
scrape_cars()
