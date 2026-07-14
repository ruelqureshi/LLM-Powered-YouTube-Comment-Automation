import time, configparser, urllib.parse, sys, openai, os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

openai.api_key = ''

def print_s(text):
    print(text)
    with open('logfile.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(text)

def unicode_escape(text):
    return text.encode('unicode_escape').decode('utf-8')

def unicode_unescape(text):
    return text.encode('utf-8').decode('unicode_escape')

options = webdriver.ChromeOptions()
#options.add_argument("-headless")
options.add_argument("-start-maximized")

chrome_driver_path = 'chromedriver.exe'

user_data_dir = 'C:/Users/GAMING/AppData/Local/Google/Chrome/User Data'
profile = 'Default'

chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_argument(f"user-data-dir={user_data_dir}")
chrome_options.add_argument(f"profile-directory={profile}")
#chrome_options.add_argument("--headless")

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.implicitly_wait(10)

wait = WebDriverWait(driver, 40)
driver.implicitly_wait(10)
counter = int(sys.argv[1])+1
comment_counter = 1

try:
    print_s('\n[+] Opening youtube studio.')
    driver.get('https://studio.youtube.com/')
    channel_icon = wait.until(EC.element_to_be_clickable(('xpath', "//button[@id='avatar-btn']")))
    driver.execute_script("arguments[0].click();", channel_icon)

    switch_account_button = wait.until(EC.element_to_be_clickable(('xpath', "/html/body/ytcp-app/ytcp-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer[1]/div[2]/ytd-compact-link-renderer[3]/a/tp-yt-paper-item")))
    switch_account_button.click()
    switch = wait.until(EC.element_to_be_clickable(('xpath', f'/html/body/ytcp-app/ytcp-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[4]/ytd-multi-page-menu-renderer/div[3]/div[1]/ytd-account-section-list-renderer[1]/div[2]/ytd-account-item-section-renderer/div[2]/ytd-account-item-renderer[{counter}]/tp-yt-paper-icon-item/tp-yt-paper-item-body')))
    switch.click()

    channel_icon = wait.until(EC.element_to_be_clickable(('xpath', "//*[@id='img']")))
    driver.execute_script("arguments[0].click();", channel_icon)

    current_channel = driver.find_element('xpath', '//*[@id="account-name"]')
    print_s(f'\n[+] Fetching comments from channel: {current_channel.text}.')

    comments_button = wait.until(EC.element_to_be_clickable(('xpath', "//*[@id='menu-paper-icon-item-3']")))
    driver.execute_script("arguments[0].click();", comments_button)
        
    while True:
        # Check if there exists a 'Read More' button, if there is it will click it
        try:
            read_more = driver.find_element('xpath', f'/html/body/ytcp-app/ytcp-entity-page/div/div/main/div/ytcp-animatable[5]/ytcp-activity-section/div[2]/ytcp-comments-section/div[2]/tp-yt-iron-list/div/div[{comment_counter}]/ytcp-comment-thread/ytcp-comment/div[1]/div/div[1]/div[2]/span/span/ytcp-button/div')
            read_more.click()
        except:
            pass

        # Append comments found to list
        try:
            time.sleep(5)
            comment = driver.find_element('xpath', f'/html/body/ytcp-app/ytcp-entity-page/div/div/main/div/ytcp-animatable[5]/ytcp-activity-section/div[2]/ytcp-comments-section/div[2]/tp-yt-iron-list/div/div[{comment_counter}]/ytcp-comment-thread/ytcp-comment/div[1]/div/div[1]/div[2]/span/span')
            comments.append(comment.text)
            comment_counter += 1
            print("Passed")
        except:
            break

    time.sleep(15)
    print_s("\n[+] Processing comments.")
    if not comments:
        print("\n[!] No comments to process.")

        with open('comments_bool.txt', 'w') as f:
            f.write('true')
        driver.quit()
        exit()

    replies = []

    print_s(f'\n[+] Generating replies.')

    replies = []
    for x in comments:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Write a reply to this comment and don't use emojis '{x}'.",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0, 
        )

        c = {
            'reply': response['choices'][0]['text'],
        }

        replies.append(c)

    print_s(f'\n[+] Replying.')

    reply_button = driver.find_elements('xpath', f'//ytcp-comment-button[@id="reply-button"]')
    for i in range(len(replies)):
        time.sleep(5)
        #reply_button = driver.find_element('xpath', f'/html/body/ytcp-app/ytcp-entity-page/div/div/main/div/ytcp-animatable[5]/ytcp-activity-section/div[2]/ytcp-comments-section/div[2]/tp-yt-iron-list/div/div[{i+1}]/ytcp-comment-thread/ytcp-comment/div[1]/div/div[1]/div[2]/div[2]/ytcp-comment-action-buttons/div/ytcp-comment-button/span/ytcp-button/ytcp-button-shape/button/div')
        #driver.execute_script("arguments[0].click();", reply_button)
        reply_button[i].click()

        time.sleep(5)
        
        reply_box = driver.find_element('xpath', '//textarea[@id="textarea"]')
        try:
            reply_text = replies[i]['reply']
            reply_box.send_keys(reply_text)
        except Exception as e:
            cancel = driver.find_element('xpath', '//button[@aria-label="Cancel"]')
            cancel.click()
            time.sleep(5)
            continue
                        
        time.sleep(5)
                
        #click_reply = driver.find_element('xpath', f'/html/body/ytcp-app/ytcp-entity-page/div/div/main/div/ytcp-animatable[5]/ytcp-activity-section/div[2]/ytcp-comments-section/div[2]/tp-yt-iron-list/div/div[{i+1}]/ytcp-comment-thread/ytcp-comment/div[2]/ytcp-commentbox/div[1]/div/div/div/ytcp-ve/ytcp-comment-button/a/tp-yt-paper-button/yt-formatted-string')
        click_reply = driver.find_element('xpath', f'//ytcp-comment-button[@id="submit-button"]/span/ytcp-button/ytcp-button-shape/button')
        #driver.execute_script("arguments[0].click();", click_reply)
        click_reply.click()

    time.sleep(10)
    driver.quit()

except Exception as e:
    print(str(e))
    print('\n[!] Skipping.')
    with open('status.txt', 'w') as f:
        f.write('done')

    with open('comments_bool.txt', 'w') as f:
        f.write('true')

    exit()

else:
    print_s('\n[+] Done.')
    with open('status.txt', 'w') as f:
        f.write('done')

    with open('comments_bool.txt', 'w') as f:
        f.write('true')

    exit()
