import os
import time
import re

try:
    import selenium
except ImportError:
    os.system("pip install selenium")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

### REAL STUFF ####

def automateKahootClient(pin, name, answerTable):
    service = Service(executable_path="chromedriver.exe", options=webdriver.ChromeOptions())
    driver = webdriver.Chrome(service=service)

    driver.get(f"https://kahoot.it/?pin={pin}&refer_method=link")

    time.sleep(2)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//input[@data-functional-selector="username-input"]'))
    )
    nameBox = driver.find_element(By.XPATH, '//input[@data-functional-selector="username-input"]')
    nameBox.send_keys(name + Keys.ENTER)

    ### ANSWERING ###



    # Loop for next questions
    while True:
        try:

             # Wait for any question element to appear
            question_locator_wait = WebDriverWait(driver, 300)
            question_locator_wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="shadow-text__Text-sc-o7uc06-1 cAcSib" and contains(text(), "Question")]')))

            # Find question element
            question_element = driver.find_element(By.XPATH, '//div[@class="shadow-text__Text-sc-o7uc06-1 cAcSib" and contains(text(), "Question")]')

            # Extract the question number from the element text
            question_number_text = question_element.text
            question_number = int(question_number_text.replace("Question", "").strip())

            print(f"Question {question_number}: {answerTable[(int(len(answerTable)/2)) + question_number]}")

            # Answer the question
            kahootClientAnswer(driver, int(answerTable[(int(len(answerTable)/2) + question_number)-1][7]))
            question_number += 1

        except Exception as e:
            # Program waits max of 5 mins for questions to appear before terminating
            print(e)
            print("program broke rip")
            break
    
    driver.quit()

    
def kahootClientAnswer(driver, option):
    if option == 1:
        buttonWait = WebDriverWait(driver, 300)
        buttonWait.until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-functional-selector="answer-0"]'))
        )
        button = driver.find_element(By.XPATH, '//button[@data-functional-selector="answer-0"]')
        button.click()
    elif option == 2:
        buttonWait = WebDriverWait(driver, 300)
        buttonWait.until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-functional-selector="answer-1"]'))
        )
        button = driver.find_element(By.XPATH, '//button[@data-functional-selector="answer-1"]')
        button.click()
    elif option == 3:
        buttonWait = WebDriverWait(driver, 300)
        buttonWait.until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-functional-selector="answer-2"]'))
        )
        button = driver.find_element(By.XPATH, '//button[@data-functional-selector="answer-2"]')
        button.click()
    elif option == 4:
        buttonWait = WebDriverWait(driver, 300)
        buttonWait.until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-functional-selector="answer-3"]'))
        )
        button = driver.find_element(By.XPATH, '//button[@data-functional-selector="answer-3"]')
        button.click()
    else:
        print("Not a real answer")


def kahootAnswersLookUp(quizid):
    """
    Takes in a quizID (in the url of a kahoot quiz) and returns a dictionary of questions mapped to correct answers
    """
    
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    
    driver.get("https://create.kahoot.it/details/" + quizid)
    waitForButton = WebDriverWait(driver, 10)
    waitForButton.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/main/div[2]/div[2]/div[2]/div/section[1]/div/button")))
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/main/div[2]/div[2]/div[2]/div/section[1]/div/button").click()

    questions_answers = []
    time.sleep(1)
    
    # List of question and correct answer elements
    
    question_elements = driver.find_elements(By.XPATH, '//span[@class="styles__Question-sc-19vxqaz-6 ejwdwI"]')
    answer_elements = answer_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "styles__Choice-sc-19vxqaz-17 illeca") and contains(@aria-label, "correct") and not(contains(@aria-label, "incorrect"))]')

    # Loop through each question
    # Uses zip() to make a tuple for each iteration
    for index, (question_elementt) in enumerate(question_elements, start=1):
        questions_answers.append(index)
    

    for index, (answer_element) in enumerate(answer_elements, start=1):
        questions_answers.append(answer_element.get_attribute("aria-label"))

    driver.quit()
    return questions_answers
    



if __name__ == "__main__":

    answerTable = []
    quizID = input ("Please enter quizID (should be in the url of hosts): ")
    quizCode = input("Enter the quiz code: ")
    nickname = input ("Enter your nickname: ")
    #randomInterval = input("Enter Y or N for random interval answering: ")
    kahootAnswersLookUp(quizID)
    automateKahootClient(quizCode, nickname, answerTable)



