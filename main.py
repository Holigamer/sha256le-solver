import random
import string

from selenium import webdriver
from selenium.webdriver.common.by import By

firefox = webdriver.Firefox()
firefox.get("https://keftcha.github.io/sha256le/")


# bruteforcing the solution
# max of 16 tries
def bruteforceSHA256le():
    correct_symbols = [0] * 64
    for i in range(0, 16):
        firefox.find_element(By.ID, "input").clear()
        current_solution = ""
        for symbol in range(0, 64):
            # go through all 64 chars
            if correct_symbols[symbol]:
                # there is already a symbol at this place
                current_solution += correct_symbols[symbol]
            else:
                # convert integer to hex
                current_solution += str(i) if i < 10 else "abcdef"[i - 10]

        print("Trying: '" + current_solution + "'")
        firefox.find_element(By.ID, "input").send_keys(current_solution)

        # validate solution
        firefox.find_element(By.ID, "checkButton").click()

        # interpret correct symbols and save in cache
        tries = firefox.find_element(By.ID, "triesNode").find_elements(By.XPATH, "//div")
        last_try_symbol_spans = tries[-1].find_elements(By.TAG_NAME, "span")

        pos = 0  # where are we?
        for symbol in last_try_symbol_spans:
            # find symbols that are green.
            if "green" in symbol.get_attribute("style"):
                correct_symbols[pos] = symbol.text
            pos += 1


# random char algorithm with past memory.
def randomGuessSHA256le():
    solutions_past = []
    correct_symbols = "".join("n" for _ in range(64))  # Fill invalid sports with n, because n is cool

    while "n" in correct_symbols:
        # there is still a wrong symbol

        # generate a new seed
        sol = ""
        for i in range(64):
            if correct_symbols[i] != "n":
                sol += correct_symbols[i]
            else:
                sol += str(random.choice(string.digits + 'abcdef')).lower()
        solutions_past.append(sol)

        # validate solution
        firefox.find_element(By.ID, "input").clear()
        print("Trying: '" + solutions_past[-1] + "'")
        firefox.find_element(By.ID, "input").send_keys(solutions_past[-1])
        firefox.find_element(By.ID, "checkButton").click()

        # extract correct symbols from tries
        tries = firefox.find_element(By.ID, "triesNode").find_elements(By.XPATH, "//div")
        last_try_symbol_spans = tries[-1].find_elements(By.TAG_NAME, "span")

        pos = 0
        for symbol in last_try_symbol_spans:
            # find green symbols in latest try
            if "green" in symbol.get_attribute("style"):
                temp = list(correct_symbols)
                temp[pos] = symbol.text
                correct_symbols = "".join(temp)
            pos += 1


# random char algorithm with past memory and only unique new random generation.
# max of 16 tries, because of unique new random chars
def randomGuessSHA256leSmart():
    solutions_past = []
    correct_symbols = "".join("n" for _ in range(64))  # Fill invalid sports with n, because n is cool

    while "n" in correct_symbols:
        # there is still a wrong symbol

        # generate the random sha key
        sol = ""
        for i in range(64):
            if correct_symbols[i] != "n":
                sol += correct_symbols[i]
            else:
                # create a char that was not there before
                while True:
                    r = str(random.choice(string.digits + 'abcdef')).lower()
                    past_characters = "".join(solutionPast[i] for solutionPast in solutions_past)

                    if not r in past_characters:
                        sol += r
                        break

        solutions_past.append(sol)

        # validate solution
        firefox.find_element(By.ID, "input").clear()
        print("Trying: '" + solutions_past[-1] + "'")
        firefox.find_element(By.ID, "input").send_keys(solutions_past[-1])
        firefox.find_element(By.ID, "checkButton").click()

        # extract correct symbols from tries
        tries = firefox.find_element(By.ID, "triesNode").find_elements(By.XPATH, "//div")
        last_try_symbol_spans = tries[-1].find_elements(By.TAG_NAME, "span")

        pos = 0
        for symbol in last_try_symbol_spans:
            # find green symbols in latest try
            if "green" in symbol.get_attribute("style"):
                temp = list(correct_symbols)
                temp[pos] = symbol.text
                correct_symbols = "".join(temp)
            pos += 1


# bruteforceSHA256le()
randomGuessSHA256le()
# randomGuessSHA256leSmart()
