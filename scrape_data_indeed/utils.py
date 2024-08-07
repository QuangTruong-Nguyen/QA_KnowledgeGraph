from selenium import webdriver
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import datetime
import json    
import os
from datetime import datetime, timedelta



def init_driver():
    
    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]
    
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    for option in options:
        chrome_options.add_argument(option)

    driver = webdriver.Edge(options=chrome_options)
    
    return driver


#____________________________________________

def access(driver,url):
    print("_"*30, "ACCESS URL","_"*30)
    driver.get(url)
    sleep(15)


def search(driver, job, location):
    print("_"*30, "SEARCH","_"*30)
    
    search_box_job = driver.find_element(By.XPATH, '//input[@id="text-input-what"]')
    search_box_location=driver.find_element(By.XPATH, '//input[@id="text-input-where"]')
    search_box_job.send_keys(job)
    search_box_location.send_keys(location)

    search_box_location.send_keys(Keys.RETURN)
    driver.implicitly_wait(8)
    


def save_data(dict_jd):
    directory = './data'
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    today = datetime.today().strftime('%Y_%m_%d')
    filename = f"{directory}/data_{today}.json"
    
    json_file = json.dumps(dict_jd, indent= 4, ensure_ascii=False)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(json_file)
    

def info_job(driver):
    
    # id=0

    num_job= driver.find_element(By.XPATH, '//div[@class="jobsearch-JobCountAndSortPane-jobCount css-13jafh6 eu4oa1w0"]//span').text
    num_job_=re.sub(r'\D', '', num_job)
    num_job=int(num_job_)
    num_next= num_job//15
    

    if num_next >15 :
        num_next=15
    
    dict_job={}
    for i in range(0,num_next-2):
        info_jobs = driver.find_elements(By.XPATH, '//div[@class="job_seen_beacon"]')
        print("_"*30, "START","_"*30)
        
        
        try:
            close = driver.find_element(By.XPATH, '//button[@aria-label="close"]')
            close.click()
        except NoSuchElementException:
            pass
        
        for element in info_jobs:
            element.click()  
            try:              
                today = datetime.today()
                date_post= element.find_element(By.XPATH, './/span[@data-testid="myJobsStateDate"]').text
                date_post_=re.sub(r'\D', '', date_post)
                if date_post_ != "":
                    
                    posted_date = today - timedelta(days=int(date_post_))
                    posted_date_str = posted_date.strftime('%Y-%m-%d')
                else:
                    posted_date_str=today.strftime('%Y-%m-%d')
               
                
                
                
                name_job_ = driver.find_element(By.XPATH, '//h2[@data-testid="jobsearch-JobInfoHeader-title"]/span').text
                name_job = name_job_.replace("- job post", "").strip()
                
                name_company = driver.find_element(By.XPATH, '//div[@data-testid="inlineHeader-companyName"]/span/a').text

                location = driver.find_element(By.XPATH, '//div[@data-testid="inlineHeader-companyLocation"]/div').text
                
                
        
                job_description = driver.find_elements(By.XPATH, '//div[@id="jobDescriptionText"]')

                
                content_jd = ""
                for jd in job_description:
                    get_html = jd.get_attribute("innerHTML")             
                    parser = BeautifulSoup(get_html, 'html.parser')        
                    jd = parser.get_text()    
                    content_jd += jd.replace("\n"," ").replace("   ","")
                # id+=1
                id=name_company+'@'+name_job
                
                try:
                    dict_job[id]
                except KeyError:
                    dict_job[id] = {
                        "ID":id,
                        "job":name_job,
                        "company": name_company,
                        "location": location,
                        "job_description":content_jd,
                        "date_post": posted_date_str
                        
                    }
                
                sleep(4)
            except NoSuchElementException:
                pass
        
        try:
            next = driver.find_element(By.XPATH, '//a[@data-testid="pagination-page-next"]')
            next.click()
            sleep(4)
        except NoSuchElementException:
            break;
        try:
            close = driver.find_element(By.XPATH, '//button[@aria-label="close"]')
            close.click()
        except NoSuchElementException:
            pass
    
    driver.quit() 
    return dict_job
        

