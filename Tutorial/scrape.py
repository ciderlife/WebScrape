
import json
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import time

driver_location = "/Users/Ted/Documents/chromedriver/chromedriver"
driver = webdriver.Chrome(executable_path=driver_location)
driver.get("http://www.google.com")
driver.find_element_by_class_name('gb_Me').click()
inputElement = driver.find_element_by_id("Email")
inputElement.send_keys('bsmithfun2016@gmail.com')
inputElement.send_keys(Keys.ENTER)

time.sleep(3)

inputElement = driver.find_element_by_id("Passwd")
inputElement.send_keys('qwerty123!!!')
inputElement.send_keys(Keys.ENTER)

with open("quora_june.json", 'r') as f:
    data  = json.load(f)

all_results = []
for d in data:
    all_results.extend(d['results'])

questions = []
for i, result in enumerate(all_results):
    link = result['link']
    http_index = link.find('http')
    if http_index > 0 and '&' in link:
    	and_index = link.find('&')
    	link = link[http_index:and_index]
    print(i, link)
    driver.get(link)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    question_area = soup.find("div", { "class" : "QuestionArea" })
    question_span = question_area.find("span", {"class": "rendered_qtext"})
    answers = soup.find("div", {"class", "QuestionPageAnswerHeader"})
    answers_num = answers.text.split()[0]
    follows_num = soup.find('span', {'class', 'count'}).text
    questions.append([question_span.text, follows_num, answers_num])

df_questions = pd.DataFrame(questions, columns=['Question', 'Follows', 'Answers'])
df_questions['Follows'] = df_questions['Follows'].map(lambda x: int(float(x[:-1]) * 1000) if x[-1] == 'k' else int(x))
df_questions['Answers'] = df_questions['Answers'].map(lambda x: 100 if '+' in x else int(x))
df_questions.to_csv('questions_test.csv', index=False)
