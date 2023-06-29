# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 16:19:33 2023
@author: ProBook
"""
#get cars data from polovniautomobili.com by brand
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List
import csv
import pandas as pd
import time
from datetime import datetime

#Brands list
first_list_full = ["ac", "acura", "alfa-romeo", "aro", "audi", "austin", "bentley", "bmw", "buick", "cadillac", "chery", "chevrolet", "chrysler", "citroen", "cupra", "dacia", "daewoo", "daihatsu", "dodge", "ferrari", "fiat", "ford", "gaz", "great-wall", "honda", "hummer", "hyundai", "infiniti", "isuzu", "jaguar", "jeep", "jinpeng", "kia", "ktm", "lada", "lamborghini", "lancia", "land-rover", "lexus", "lincoln", "linzda", "mahindra", "maserati", "matra", "mazda", "mercedes-benz", "mercury", "mg", "mini", "mitsubishi", "moskvitch", "nissan", "nsu", "oldsmobile", "opel", "peugeot", "piaggio", "polski-fiat", "pontiac", "porsche", "renault", "rolls-royce", "rover", "saab", "seat", "shuanghuan", "smart", "ssangyong", "subaru", "suzuki", "talbot", "tata", "tavria", "tesla", "toyota", "trabant", "triumph", "uaz", "volkswagen", "volvo", "wartburg", "zastava", "zhidou", "skoda", "ostalo"]
second_list_full = ["AC", "Acura", "Alfa Romeo", "Aro", "Audi", "Austin", "Bentley", "BMW", "Buick", "Cadillac", "Chery", "Chevrolet", "Chrysler", "Citroen", "Cupra", "Dacia", "Daewoo", "Daihatsu", "Dodge", "Ferrari", "Fiat", "Ford", "GAZ", "Great Wall", "Honda", "Hummer", "Hyundai", "Infiniti", "Isuzu", "Jaguar", "Jeep", "Jinpeng", "Kia", "KTM", "Lada", "Lamborghini", "Lancia", "Land Rover", "Lexus", "Lincoln", "Linzda", "Mahindra", "Maserati", "Matra", "Mazda", "Mercedes Benz", "Mercury", "MG", "MINI", "Mitsubishi", "Moskvitch", "Nissan", "NSU", "Oldsmobile", "Opel", "Peugeot", "Piaggio", "Polski Fiat", "Pontiac", "Porsche", "Renault", "Rolls Royce", "Rover", "Saab", "Seat", "Shuanghuan", "Smart", "SsangYong", "Subaru", "Suzuki", "Talbot", "Tata", "Tavria", "Tesla", "Toyota", "Trabant", "Triumph", "UAZ", "Volkswagen", "Volvo", "Wartburg", "Zastava", "ZhiDou", "Škoda", "Ostalo"]
first_list_test = ["ac", "acura", "alfa-romeo"]
second_list_test = ["AC", "Acura", "Alfa Romeo"]
#Set to first_list_test and second_list_test to test the code
#Set to first_list_full and second_list_full to scrape all brands
first_list = first_list_test
second_list = second_list_test

brands = [[first_list[i], second_list[i]] for i in range(len(first_list))]

#Define parameters
current_brand = brands[2][0]  #Default value
withoutPrice = '0'  #1 to include cars without price
specifyNumOfPagesFlag = '0'  #Flag to scrape just specific number of pages, if the value is at the 0, it wil scrape all pages
specificNumOfPages= 3  #Number of pages per brand, used if specifyNumOfPagesFlag='1'


@dataclass
class Car:
    link: str
    brand: str
    full_name: str
    year: int
    kw: int
    horsepower: int
    body: str
    fuel: str
    engine_size_cm3: int
    price_eur: int
    brand_code: str
    

def scrape_cars():
    # Configure Selenium WebDriver
    driver = webdriver.Chrome()  # Replace with the path to your chromedriver executable
    # List to store car objects
    cars = []
    
    print("Scraping by brand...")
    
    #Print end time
    startTime = datetime.now()
    print("Start time:", startTime.strftime("%H:%M:%S"))

    for iBrand in brands:
        current_brand = iBrand[0]
        print("Current brand:", current_brand)
        # Base URL for car search
        base_url = "https://www.polovniautomobili.com/auto-oglasi/pretraga?"
        #page
        Tsort = "&sort=basic&"
        Tbrand = "brand="+current_brand+"&"
        Tcity = "city_distance=0&"
        TshowOldNew = "showOldNew=all&"
        TwithoutPrice = "without_price="+withoutPrice
        
        
        # Number of pages to scrape
        if specifyNumOfPagesFlag == '1':
            num_pages = specificNumOfPages
            print("Getting data from "+str(specificNumOfPages)+" pages...")
        else:            
            #Geting number of pages
            url = base_url+"page="+str(1)+Tsort+Tbrand+Tcity+TshowOldNew+TwithoutPrice
            driver.get(url)
            lss = (driver.find_element("xpath",'/html/body/div[9]/div[2]/div[2]/div[1]/div[2]/small[1]')).text.strip()
            #print(lss)
            np = lss.split('ukupno ',1)[1]
            #print(np)
            npp = int(int(np)/25)
            #print(npp)
            if npp>1:
                num_pages = npp
                print("Getting data from "+str(npp)+" pages...")
            else:
                num_pages = 1 
                print("Getting data from only one page...")
             
        
        for page in range(1, num_pages + 1):
            # Set the page parameter
            url = base_url+"page="+str(page)+Tsort+Tbrand+Tcity+TshowOldNew+TwithoutPrice
            
            driver.get(url)
            #time.sleep(1)
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
                brand = iBrand[1]
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
                    try:
                        priceTemp3 = priceTemp2.replace(".", "")
                        price_eur = int(priceTemp3)
                    except ValueError:
                        price_eur = None  # Assign None if conversion fails or "Na" value is encountered
                brand_code = current_brand    
                    
                # Create a Car object and add it to the list
                #cars.append(Car(link, full_name, year, km, body, fuel, engine_size, price_eur))
                cars.append(Car(link, brand, full_name, year, kw, horsepower, body, fuel,engine_size, price_eur, brand_code))
                

            # Add a delay between page requests to avoid overwhelming the server
            print("Added cars from page:"+str(page))
            time.sleep(0.01)

    #Print end time
    endTime = datetime.now()
    print("End time:", endTime.strftime("%H:%M:%S"))

    # Calculate the time difference
    duration = endTime - startTime
    print("Duration:", duration)
      
    
    
    # Close the Selenium WebDriver
    driver.quit()
    
    # Convert car objects to dataframe
    df = pd.DataFrame(cars)
    
    # Print head(2) of dataframe
    #print(df.head(2))
    
    # Export dataframe to csv file
    df.to_csv('outV03.csv', index=False)
    
    print("Scraping completed. Car listings saved in outV03.csv.")


# Execute the scraping function
scrape_cars()
