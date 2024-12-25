from flask import Flask, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, asyncio
import uuid
from datetime import datetime

from config import Config
from utils.mongo_worker import twitterTrends
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_trending', methods=['GET'])
async def get_trending():
    try:
        cookies = Config.COOKIES
        strg = ""

        option = webdriver.ChromeOptions()

        # option.add_argument('--proxy-server=%s' % PROXYMESH_URL) 
        # option.add_argument("--headless")
        option.add_argument("--disable-gpu")
        option.add_argument("--no-sandbox")
        option.binary_location = '/usr/bin/brave-browser'
        driver = webdriver.Chrome(options=option)

        driver.maximize_window()
        driver.get("http://x.com")

        for cookie in cookies:
            driver.add_cookie(cookie)

        time.sleep(2)
        print("Login successful!")
        driver.refresh()
        time.sleep(5)


        trending_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Timeline: Trending now"]'))
        )

        WebDriverWait(driver, 10).until(
            lambda d: len(trending_section.find_elements(By.XPATH, './*')) > 0
        )

        children = trending_section.find_elements(By.XPATH, './*')

        
        for child in children:
            print(child.text)
            strg += child.text + "\n"

        
        skip = ['What’s happening', 'Show more']
        cleaned = [i for i in filter(lambda x: x not in skip and x != '', strg.split('\n'))]

        
        data = []

        
        def generate_unique_id():
            return str(uuid.uuid4())

        
        def get_current_datetime():
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        
        i = 0
        while i < len(cleaned):
            
            if 'posts' in cleaned[i]:
                i += 1
                continue

            trend_data = {
                'unique_id': generate_unique_id(),
                'date_time': get_current_datetime(),
            }

            trend_data[cleaned[i]] = ''
            
            if i + 1 < len(cleaned) and '#' in cleaned[i + 1]:
                trend_data[cleaned[i]] = cleaned[i + 1]
                i += 1

            data.append(trend_data)
            
            i += 1

        print(data)
        
        await asyncio.create_task(twitterTrends.insert_data({
            'data': data
        }))

        driver.quit()
        return jsonify(data)

    except Exception as e:
        print("ERROR: ", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
