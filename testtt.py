import requests
from bs4 import BeautifulSoup
import selenium
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time

chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
chrome_options.add_argument("--no-sandbox")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


while True:
    print("Izvēlies valodu!")
    print("Raksti 1, ja vēlies angļu Vikipēdijas interneta pārlūka lapu.")
    print("Raksti 2, ja vēlies latviski tulkoju Vikipēdijas interneta pārlūka lapu.")
    valoda = input()

    if valoda not in ["1", "2"]:
        print("Nav ievadīta pareiza opcija (1 vai 2), lūdzu, mēģiniet vēlreiz.")
        continue

    url = "https://www.wikipedia.org/"
    driver.get(url)

    time.sleep(1)
    	
    if valoda == "1":
        english_link = driver.find_element(By.ID, "js-link-box-en")
        english_link.click()

        time.sleep(2)

        menu_button = driver.find_element(By.ID, "vector-main-menu-dropdown-checkbox")
        menu_button.click()

        time.sleep(2)

        random_article_link = driver.find_element(By.CSS_SELECTOR, 'a[title="Visit a randomly selected article [alt-shift-x]"]')
        random_article_link.click()
        time.sleep(3)

        Lapas_url=driver.current_url
        
        headers = driver.find_elements(By.TAG_NAME, 'h2')
        paragraphs = driver.find_elements(By.TAG_NAME, 'p')
        
        # Extract the text from each element
        header_text = [header.text for header in headers]
        paragraph_text = [paragraph.text for paragraph in paragraphs]
        
        # Combine the text in one string
        all_text = ' '.join(header_text + paragraph_text)
        # Remove text in brackets
        pattern = r'\[[^][]*?\]'
        all_text = re.sub(pattern, '', all_text)
        
        driver.get("https://www.semrush.com/goodcontent/summary-generator/")
        time.sleep(1)
        allow_all_cookies_button = driver.find_element(By.CSS_SELECTOR, 'button.ch2-btn.ch2-allow-all-btn.ch2-btn-primary')
        allow_all_cookies_button.click()
        time.sleep(1)
        input_box = driver.find_element(By.CSS_SELECTOR, 'textarea#input[placeholder="Begin typing or paste text here..."]')
        input_box.send_keys(all_text)
        time.sleep(3)

        summarize_button = driver.find_element(By.XPATH, '//button[contains(@class, "___SButton_1ab13_gg_") and .//span[text()="Summarize"]]')
        summarize_button.click()
        word_counter_element = driver.find_element(By.CSS_SELECTOR, 'span[role="status"].gch-cs1kee')
        word_counter_text = word_counter_element.text
        word_count = int(re.search(r'\d+', word_counter_text).group())  # Extract the number
        
        if word_count < 50:
            summary_text = all_text
        elif 50 < word_count < 300:
            time.sleep(5)
            output_summary_content = driver.find_element(By.CSS_SELECTOR, 'div.gch-10i85t4[data-ui-name="Box"][role="textbox"][aria-label="Summary"]')
            summary_text = output_summary_content.text
        elif 300 <= word_count < 600:
            time.sleep(8)
            output_summary_content = driver.find_element(By.CSS_SELECTOR, 'div.gch-10i85t4[data-ui-name="Box"][role="textbox"][aria-label="Summary"]')
            summary_text = output_summary_content.text
        elif word_count >= 600:
            time.sleep(12)
            output_summary_content = driver.find_element(By.CSS_SELECTOR, 'div.gch-10i85t4[data-ui-name="Box"][role="textbox"][aria-label="Summary"]')
            summary_text = output_summary_content.text
        #time.sleep (10)

        time.sleep(1)

        driver.get("https://translate.google.com/")
        time.sleep(1)
        # Press button
        cookie_button = driver.find_element(By.CSS_SELECTOR, 'button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.XWZjwc[jscontroller="soHxf"][jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;"][data-idom-class="nCP5yc AjY5Oe DuMIQc LQeN7 XWZjwc"][jsname="b3VHJd"]')
        cookie_button.click()
        time.sleep(1)


        input_text_area = driver.find_element(By.CSS_SELECTOR, 'textarea[aria-label="Avotteksts"]')
        input_text_area.send_keys(summary_text)
        time.sleep(5)

        # Scrape translated text
        translated_text_span = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div/div[6]/div/div[1]')
        summary_text = translated_text_span.text
        time.sleep(2)
        
        driver.get(Lapas_url)
        time.sleep(2)
        

        
        page_tools_dropdown = driver.find_element(By.ID, "vector-page-tools-dropdown-checkbox")
        page_tools_dropdown.click()
        time.sleep(1)

        page_info_button = driver.find_element(By.XPATH, '//html/body/div[2]/div/div[3]/main/div[1]/div/div[2]/nav[2]/div/div/div/div/div[3]/div[2]/ul/li[6]')
        page_info_button.click()
        time.sleep(2)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        page_views_link = soup.find(attrs={"rel": "nofollow", "class": "external text"})
        page_views_text = page_views_link.get_text()

    elif valoda == "2":
        latvian_link = driver.find_element(By.ID, "js-link-box-lv")
        latvian_link.click()
        time.sleep(2)

        menu_button = driver.find_element(By.ID, "vector-main-menu-dropdown-checkbox")
        menu_button.click()
        time.sleep(1)

        random_article_link = driver.find_element(By.CSS_SELECTOR, 'a[title="Iet uz nejauši izvēlētu lapu [alt-shift-x]"]')
        random_article_link.click()
        
        time.sleep(3)

        Lapas_url=driver.current_url
        # Find all headers (<h2>) and paragraphs (<p>)
        headers = driver.find_elements(By.TAG_NAME, 'h2')
        paragraphs = driver.find_elements(By.TAG_NAME, 'p')
        
        # Extract the text from each element
        header_text = [header.text for header in headers]
        paragraph_text = [paragraph.text for paragraph in paragraphs]

            # Combine the text in one string
        all_text = ' '.join(header_text + paragraph_text)
        # Remove text in brackets
        pattern = r'\[[^][]*?\]'
        all_text = re.sub(pattern, '', all_text)

        driver.get("https://translate.google.com/?sl=auto&tl=en&op=translate")
        time.sleep(1)
        # Press button
        cookie_button = driver.find_element(By.CSS_SELECTOR, 'button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.XWZjwc[jscontroller="soHxf"][jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;"][data-idom-class="nCP5yc AjY5Oe DuMIQc LQeN7 XWZjwc"][jsname="b3VHJd"]')
        cookie_button.click()
        time.sleep(1)


        input_text_area = driver.find_element(By.CSS_SELECTOR, 'textarea[aria-label="Avotteksts"]')
        input_text_area.send_keys(all_text)
        time.sleep(5)

        # Scrape translated text
        translated_text_span = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div/div[6]/div/div[1]')
        all_text = translated_text_span.text
        time.sleep(2)
        
        
        driver.get("https://www.semrush.com/goodcontent/summary-generator/")
        time.sleep(1)
        allow_all_cookies_button = driver.find_element(By.CSS_SELECTOR, 'button.ch2-btn.ch2-allow-all-btn.ch2-btn-primary')
        allow_all_cookies_button.click()
        time.sleep(1)
        input_box = driver.find_element(By.CSS_SELECTOR, 'textarea#input[placeholder="Begin typing or paste text here..."]')
        input_box.send_keys(all_text)
        time.sleep(3)

        summarize_button = driver.find_element(By.XPATH, '//button[contains(@class, "___SButton_1ab13_gg_") and .//span[text()="Summarize"]]')
        summarize_button.click()
        word_counter_element = driver.find_element(By.CSS_SELECTOR, 'span[role="status"].gch-cs1kee')
        word_counter_text = word_counter_element.text
        word_count = int(re.search(r'\d+', word_counter_text).group())  # Extract the number
        
        if word_count < 50:
            summary_text = all_text
        elif 50 < word_count < 300:
            time.sleep(5)
            output_summary_content = driver.find_element(By.CSS_SELECTOR, 'div.gch-10i85t4[data-ui-name="Box"][role="textbox"][aria-label="Summary"]')
            summary_text = output_summary_content.text
        elif 300 <= word_count < 600:
            time.sleep(8)
            output_summary_content = driver.find_element(By.CSS_SELECTOR, 'div.gch-10i85t4[data-ui-name="Box"][role="textbox"][aria-label="Summary"]')
            summary_text = output_summary_content.text
        elif word_count >= 600:
            time.sleep(12)
            output_summary_content = driver.find_element(By.CSS_SELECTOR, 'div.gch-10i85t4[data-ui-name="Box"][role="textbox"][aria-label="Summary"]')
            summary_text = output_summary_content.text
       

        time.sleep(1)
        
        driver.get("https://translate.google.com/")
        time.sleep(1)
        # Press button
        #cookie_button = driver.find_element(By.CSS_SELECTOR, 'button.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.XWZjwc[jscontroller="soHxf"][jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;mlnRJb:fLiPzd;"][data-idom-class="nCP5yc AjY5Oe DuMIQc LQeN7 XWZjwc"][jsname="b3VHJd"]')
        #cookie_button.click()
        time.sleep(1)


        input_text_area = driver.find_element(By.CSS_SELECTOR, 'textarea[aria-label="Avotteksts"]')
        input_text_area.send_keys(summary_text)
        time.sleep(5)

        # Scrape translated text
        translated_text_span = driver.find_element(By.XPATH, '/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[2]/c-wiz[2]/div/div[6]/div/div[1]')
        summary_text = translated_text_span.text
        time.sleep(2)
        

        driver.get(Lapas_url)
        time.sleep(2)

        # Print the AI's summary to the user

        page_tools_dropdown = driver.find_element(By.ID, "vector-page-tools-dropdown-checkbox")
        page_tools_dropdown.click()
        time.sleep(1)
        
        page_info_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/main/div[1]/div/div[2]/nav[2]/div/div/div/div/div[3]/div[2]/ul/li[5]/a/span')
        page_info_button.click()
        time.sleep(2)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        page_views_link = soup.find('div', class_='mw-pvi-month')
        page_views_text = page_views_link.get_text()

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    header = soup.find("h1", id="firstHeading").get_text()
    time.sleep(1)
    print(" ")
    print(" ")
    print(f"Virsraksts: {header}")
    print(" ")
    print(f"URL: {Lapas_url}")
    print(" ")
    print("Lapas skatījumi pēdējo 30 dienu laikā: " + page_views_text)
    print(" ")
    print ("Vikipedijas texta kopsavilkums:    " + summary_text)
    print(" ")
    print(" ")
    break



