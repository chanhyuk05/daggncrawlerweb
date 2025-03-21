import time
from email.mime import image

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_items(location_id: str, amount: int, search_keyword: str, output: str):
    url = f"https://www.daangn.com/kr/buy-sell/?in={location_id}&search={search_keyword}"

    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    SCROLL_PAUSE_TIME = 1.5
    last_count = 0
    
    print('amount:', amount)

    while True:
        articles = driver.find_elements(By.CSS_SELECTOR, '[data-gtm="search_article"]')
        if len(articles) >= amount:
            break

        driver.execute_script("""
            const main = document.querySelector('main#main-content');
            const divs = main.querySelectorAll('div');
            if (divs.length >= 2) {
                const targetBottom = divs[1].offsetTop + divs[1].offsetHeight;
                main.scrollTo({ top: targetBottom, behavior: 'smooth' });
            }
        """)
        time.sleep(SCROLL_PAUSE_TIME)

        new_count = len(articles)
        if new_count == last_count:
            try:
                show_more_button = driver.find_element(By.CSS_SELECTOR, '[data-gtm="search_show_more_articles"] button')
                show_more_button.click()
                time.sleep(SCROLL_PAUSE_TIME)
                continue
            except:
                break
        last_count = new_count

    final_articles = driver.find_elements(By.CSS_SELECTOR, '[data-gtm="search_article"]')
    results = []

    for idx, article in enumerate(final_articles[:amount], start=1):
        try:
            title = article.find_element(By.CSS_SELECTOR, 'div > div > h2').text
            price = article.find_element(By.CSS_SELECTOR, 'div > div > div').text
            
            try:
              price = int(price[:-1].replace(",", ""))
            except ValueError:
              price = price[:-1]
            
            link = article.get_attribute("href")
            image = article.find_element(By.CSS_SELECTOR, 'article > div:first-of-type > div > span > img').get_attribute("src")
            
            if not link:
                continue
            
            try:
                status = article.find_element(By.CSS_SELECTOR, 'article > div:first-of-type > span')
                
                if status:
                  results.append({
                    "title": title,
                    "price": price,
                    "status": status.text,
                    "link": link,
                    "image": image
                  })
                else:
                  results.append({
                    "title": title,
                    "price": price,
                    "status": None,
                    "link": link,
                    "image": image
                  })
            except:
                results.append({
                    "title": title,
                    "price": price,
                    "status": None,
                    "link": link,
                    "image": image
                })
        except Exception as e:
            print(f"{idx}. Error extracting article details: {e}")

    driver.quit()
    return results