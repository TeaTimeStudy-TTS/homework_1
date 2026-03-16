from selenium import webdriver as wd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import pandas as pd
import time

def get_elements(elements_type, target:str, sleep_time:int, timeout:int) -> list:
    count = 0
    while True :
        count += 1 * sleep_time
        time.sleep(sleep_time)
        elements =  driver.find_elements(elements_type, target)
        if timeout <= count:
            raise TimeoutError(f'TIMEOUT_SETTING : {TimeoutError}초 초과로 데이터 수집 불가')
        if len(elements) == 0:
            print(f'데이터 로딩 대기 중, {count} 초 경과')
            continue
        else :
            return elements
        
def get_element(element_type ,target:str, sleep_time:int, timeout:int):
    time.sleep(sleep_time)
    return driver.find_element(element_type, target)

def get_date_str():
    # 현재 시간 가져오기 / 문자열로 변환 (초 포함)
    return datetime.now().strftime("%Y%m%d_%H%M%S")

    
TIMEOUT_SETTING = 300
STANDARD_SLEEP_TIME = 1

# 자동 제어 브라우저 가동
try :
    driver = wd.Chrome()
    driver.get('https://www.starbucks.co.kr/store/store_map.do')

    # 요소의 동작이 끝날 때 까지 대기(최대 TIMEOUT_SETTING 초)
    WebDriverWait(driver, TIMEOUT_SETTING).until(EC.invisibility_of_element_located((By.CLASS_NAME, "loading_dimm")))
    get_element(By.CLASS_NAME, 'loca_search', STANDARD_SLEEP_TIME, TIMEOUT_SETTING).click()
    btns = get_elements(By.CSS_SELECTOR, '.set_sido_cd_btn', STANDARD_SLEEP_TIME, TIMEOUT_SETTING)
    for btn in btns[:1]:
        time.sleep(STANDARD_SLEEP_TIME)
        btn.click()
        print('here 1')
        guguns = get_elements(By.CSS_SELECTOR, '.gugun_arae_box > li > .set_gugun_cd_btn', STANDARD_SLEEP_TIME, TIMEOUT_SETTING)
        print(f'guguns : {len(guguns)}' )
        guguns[0].click()
        print('here 2')
        # 이런 처리 시, 메모리 위험성 있지만, 작은 데이터라 귀찮아서 그냥 전체로 처리함...
        time.sleep(STANDARD_SLEEP_TIME)
        tuplist = [('매장명', '주소', '매장타입')]+[(
            # find_element.text로는 나오지 않아서, find_element.get_attribute('textContent')로 진행함.
            result.find_element(By.CSS_SELECTOR, 'strong').get_attribute('textContent'),
            result.find_element(By.CSS_SELECTOR, '.result_details').get_attribute('textContent').replace("1522-3232", "").strip(),
            result.find_element(By.CSS_SELECTOR, 'i').get_attribute('class').replace('pin_', '')
        ) 
         for result in get_elements
         (By.CSS_SELECTOR, '.quickSearchResultBoxSidoGugun > .quickResultLstCon'
          , STANDARD_SLEEP_TIME, TIMEOUT_SETTING)]
        print(f'tuplist : {len(tuplist)}')
        df = pd.DataFrame(tuplist)
        # df.to_csv('./' + get_date_str() + '.csv')
        df.to_csv('./신상용.csv')
        time.sleep(STANDARD_SLEEP_TIME)
        driver.find_element(By.CLASS_NAME, 'loca_search').click()
except Exception as e:
    print(e)
finally :
    print('finally 진입')
    driver.quit()


# driver.quit()
# sidos = driver.find_elements(By.CSS_SELECTOR, '#SIDO_NM0 > option')
# sidos_value = [sido.get_attribute('value').strip() for sido in sidos[1:]]
