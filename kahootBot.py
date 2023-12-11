import os
import time

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

### CODE ####

def automateKahootClient(pin, name, answerTable):
    """
    Takes in a pin, name, and answer table and joins the kahoot game and automatically answers questions
    """
    print("Joining Kahoot game...")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get(f"https://kahoot.it/?pin={pin}&refer_method=link")

    time.sleep(2)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div/div[1]/div/div/div/div[3]/div[2]/main/div/form/input"))
    )
    nameBox = driver.find_element(By.XPATH, "/html/body/div/div[1]/div/div/div/div[3]/div[2]/main/div/form/input")
    nameBox.send_keys(name + Keys.ENTER)
    print(f"Successfully joined game {pin} as {name}!")
    ### ANSWERING ###

    # Loop for every question
    while True:
        try:
            
            # Wait for the question element to appear
            question_locator_wait = WebDriverWait(driver, 300)
        
            question_locator_wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@class="shadow-text__Text-sc-o7uc06-1 cAcSib" and contains(text(), "Question")]')))
            question_element = driver.find_element(By.XPATH, f'//div[@class="shadow-text__Text-sc-o7uc06-1 cAcSib" and contains(text(), "Question")]')

            # Extract the question number from the element text
            question_number_text = question_element.text
            question_number = int(question_number_text.replace("Question", "").strip())

            print(f"Question {question_number}: Number {question_number} also {answerTable.get(question_number)}")

            # Answer the question
            kahootClientAnswer(driver, int(answerTable.get(question_number)[7]))
            time.sleep(.5)

        except Exception as e:
            # Program waits max of 5 mins for questions to appear before terminating
            print(e)
            print("Something has gone wrong or the program has terminated")
            time.sleep(5)
            break
    
    driver.quit()

    
def kahootClientAnswer(driver, option):
    """
    Takes in driver and an option number (1-4) and clicks the corresponding answer button
    """
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
    Takes in driver and a quizID (in the url of a kahoot quiz) and returns a dictionary of questions mapped to a single correct answer (even if their are multiple correct answers for that question)
    """
    print("Building answer table... please wait")
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    # Wait for web elements to load
    driver.get("https://create.kahoot.it/details/" + quizid)
    waitForButton = WebDriverWait(driver, 10)
    waitForButton.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/main/div[2]/div[2]/div[2]/div/section[1]/div/button")))
    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/main/div[2]/div[2]/div[2]/div/section[1]/div/button").click()
    time.sleep(1)
    
    answerTable = {}
    questions = driver.find_elements(By.CLASS_NAME, "question-item__QuestionListItem-sc-1evx9zu-0")

    # Loop through each question and find the correct answer(s)
    for i, question in enumerate(questions, start=1):
        question_text = question.find_element(By.CLASS_NAME, "styles__Question-sc-19vxqaz-6").text
        answer_options = question.find_elements(By.CLASS_NAME, "styles__Choice-sc-19vxqaz-17")

        # Loop through each answer child of the question
        for option in answer_options:
            answer_text = option.find_element(By.CLASS_NAME, "styles__Answer-sc-19vxqaz-20").text
            aria_label = option.get_attribute("aria-label")

            # Check if the answer is correct
            if "incorrect" not in aria_label and "correct" in aria_label:
                # Answers stored as "Option X - Answer Text"
                answ = aria_label.split("-")
                answerTable[i] = f'{answ[0]}-{answ[1]}'
    
    print("Build success!")
    driver.quit()
    return answerTable
    



if __name__ == "__main__":

    quizID = input("Enter the quizID (should be in the url of hosts browser): ")
    quizCode = input("Enter the quiz code: ")
    nickname = input("Enter your desired nickname: ")
    
    print("Starting bot...")
    answerTable = kahootAnswersLookUp(quizID)
    automateKahootClient(quizCode, nickname, answerTable)