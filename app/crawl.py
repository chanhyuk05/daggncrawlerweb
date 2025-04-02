import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_items(location_id: str | list[str], amount: int, search_keyword: str, start_price: int, end_price: int):
    print('크롤링 중...')
      
    # print(url)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.set_capability('browserless:token', 'S3Pc72Rgvfkbfl21c8e135b203b982cbcbb5b5efb8')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")

    driver = webdriver.Remote(
    command_executor='https://chrome.browserless.io/webdriver',
    options=chrome_options
    )

    results = []
    
    if isinstance(location_id, list):
      base_amount = amount // len(location_id)
      remainder = amount % len(location_id)
      amounts = [base_amount + (1 if i < remainder else 0) for i in range(len(location_id))]
      

      for i, (loc_id, loc_amount) in enumerate(zip(location_id, amounts)):
        bar = "=" * (loc_amount)
        result = crawl_items(driver, loc_id, start_price, end_price, search_keyword, loc_amount)
        print(f"[{i + 1}/{len(location_id)}] {loc_id.split('-')[0]}: {bar} ({len(result)})")
        results.extend(result)
    else:
        result = crawl_items(driver, location_id, start_price, end_price, search_keyword, amount)
        results = result


    driver.quit()
    print('크롤링 완료')
    return results
  
def crawl_items(driver, location_id: str, start_price: int, end_price: int, search_keyword: str, amount: int):
  url = f"https://www.daangn.com/kr/buy-sell/?in={location_id}&only_on_sale=true&search={search_keyword}"
    
  if start_price and end_price:
      url += f'&price={start_price}__{end_price}'
  
  driver.get(url)

  SCROLL_PAUSE_TIME = 1.5
  last_count = 0

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
      
      if not link:
        continue
        
      results.append({
        "title": title,
        "price": price,
        "link": link,
      })
    except Exception as e:
        print(f"{idx}. Error extracting article details: {e}")
          
  for result in results:
    driver.get(result['link'])
    
    time_text = driver.find_element(By.CSS_SELECTOR, 'time').text
    description = driver.find_element(By.CSS_SELECTOR, 'article > div:nth-child(1) > div:nth-child(2) > section:nth-child(2) > p').text
    
    user = driver.find_element(By.CSS_SELECTOR, 'article > div:nth-child(1) > div:nth-child(2) > section:nth-child(1) > div:nth-child(2) > div > div > div:nth-child(1) > div > a:nth-child(1)')
    username = user.find_element(By.CSS_SELECTOR, 'span').text
    userlink = user.get_attribute('href')
    

    
    metadata = driver.find_element(By.CSS_SELECTOR, 'article > div:nth-child(1) > div:nth-child(2) > section:nth-child(2) > div:nth-of-type(2)')
    
    chatting = metadata.find_element(By.CSS_SELECTOR, 'span:nth-child(1)').text
    watching = metadata.find_element(By.CSS_SELECTOR, 'span:nth-child(3)').text
    
    result['time'] = time_text
    result['description'] = description
    result['chatting'] = int(chatting.split(' ')[1])
    result['watching'] = int(watching.split(' ')[1])
    result['username'] = username
    result['userlink'] = userlink
    result['location'] = location_id.split('-')[0]
    
  return results