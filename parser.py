import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re
import csv



def parse_ad(driver):
    time.sleep(1.5)
    flat = {}
    html = str(driver.page_source)
    url = str(driver.current_url)
    exception = False
    print(url)
    try:
        id = re.findall('\/([\d]*)\/', url)
        flat['id'] = id[-1]
    except Exception as e:
        print('refreshed')
        driver.refresh()
        try:
            id = re.findall('\/([\d]*)\/', url)
            flat['id'] = id[-1]
        except Exception as e:
            exception = True
            flat['id'] = '-'

    try:
        address = re.findall('class="a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr">([\s\S]*?)</a>', html)
        flat['address'] = ','.join(address)
    except Exception as e:
        print(e)
        flat['address'] = '-'

    try:
        price = re.findall('<span itemprop="price"[\s\S]*?>([\d]+)[\s\S]*?([\d]+)[\s\S]*?([\d]+)[\s\S]*?</span>', html)
        # returns array with spaces, so we need to concat elem
        price = ''.join(price[0])
        flat['price'] = price
    except Exception as e:
        print(e)
        flat['price'] = '-'

    try:
        title = re.findall('class="a10a3f92e9--title--2Widg">([\s\S]*?)</h1>', html)
        flat['title'] = title[0]
    except Exception as e:
        print(e)
        flat['title'] = '-'

    try:
        underground = re.findall('<a class="a10a3f92e9--underground_link--AzxRC"[\s\S]*?>([\s\S]*?)</a>', html)
        flat['underground'] = ','.join(underground)
    except Exception as e:
        print(e)
        flat['underground'] = '-'

    try:
        highways = re.findall('class="a10a3f92e9--link--1t8n1 a10a3f92e9--highway_link--1jVab">([\s\S]*?)</a>', html)
        flat['highways'] = ','.join(highways)
    except Exception as e:
        print(e)
        flat['highways'] = '-'

    try:
        info = re.findall('<div class="a10a3f92e9--info-text--2uhvD">(.*?)</div>', html)
        flat['small_info'] = ','.join(info)
    except Exception as e:
        print(e)
        flat['small_info'] = '-'

    try:
        description = re.findall('class="a10a3f92e9--description-text--1_Lup">([\s\S]*?)</p>', html)
        description = re.sub('<br>', '', description[0])
        flat['description'] = description
    except Exception as e:
        print(e)
        flat['description'] = '-'

    try:
        info = re.findall('class="a10a3f92e9--value--3Ftu5">([\s\S]*?)</span>', html)
        info_names = re.findall('class="a10a3f92e9--name--3bt8k">([\s\S]*?)</span>', html)
        for i, name in enumerate(info_names):
            if 'Площадь комнат' in name:
                info_names[i] = 'Площадь комнат'
        for i, name in enumerate(info_names):
            flat[name] = info[i]
    except Exception as e:
        print(e)

    try:
        info = re.findall('class="a10a3f92e9--value--22FM0"">([\s\S]*?)</div>', html)
        if info:
            info_names = re.findall('class="a10a3f92e9--name--22FM0">([\s\S]*?)</div>', html)
            for i, name in enumerate(info_names):
                flat[name] = info_names[i]
    except Exception as e:
        print(e)

    try:
        photo_num = re.findall('class="a10a3f92e9--title--1e5zS">([\s\S]*?)</div>', html)
        flat['photo num'] = photo_num[-1]
    except Exception as e:
        print(e)
        flat['photo num'] = '-'
    if exception == True:
        with open('data/errfile.txt', 'a') as out:
            out.write(url + '\n')
    print(flat)
    return flat





def init_driver():
    driver = webdriver.Firefox()
    driver.implicitly_wait(10)
    return driver



if __name__ == "__main__":
    try:
        city_to_search = 'Москва'
        driver = init_driver()
        action = ActionChains(driver)
        wait = WebDriverWait(driver, 15)
        driver.get('https://www.cian.ru')
        #time.sleep(2)
        choose_city = driver.find_elements_by_class_name('button_component-button-1unijOciOw6')
        #time.sleep(2)
        action.move_to_element(choose_city[1]).click().perform()
        #elem[1].click()
        #time.sleep(2)
        moscow = driver.find_element_by_class_name('city-tab--1280ae92de03d5e48a56dd4d6a7d3b87')
        moscow.click()
        choose_but = driver.find_element_by_class_name('button_component-button-1unijOciOw6')
        choose_but.click()
        room_but = driver.find_elements_by_class_name('_025a50318d--c-filters-field-room--3bqTr')
        room_but[0].click()
        #time.sleep(2)
        checkboxes = driver.find_elements_by_class_name('components-value-checkbox-yWeqqKCV')
        print('Elem: checkboxes of ', len(checkboxes))
        for i in range(len(checkboxes)):
            if i == 1 or i == 2:
                continue
            checkboxes[i].click()
        elem = driver.find_element_by_class_name('_025a50318d--c-filters-field-button--1EBB-')
        elem.click()
        while True:
            time.sleep(3)
            xpath_district = '//div[@class="_93444fe79c--container--8GQMJ _93444fe79c--filters-item--2yZB0"]/button'
            elem = driver.find_elements_by_xpath(xpath_district)
            print(len(elem))
            elem[-1].click()
            time.sleep(3)
            regions_list_class = '_93444fe79c--column-item--2EH_6'
            regions_list = driver.find_elements_by_class_name(regions_list_class)
            if len(regions_list) != 0:
                break
        cur_reg = 142
        #here we need to scroll somewhow, But it could be hard
        regions_list[cur_reg-4].location_once_scrolled_into_view
        #action.move_to_element(regions_list[cur_reg]).click().perform()
        regions_list[cur_reg].click()
        elem = driver.find_elements_by_class_name('_2_I0uxAX1QTt_l4n')
        elem[-1].click()
        #action.move_to_element(elem[-1]).click().perform()
        time.sleep(1)
        #Была возможность просмотривать объявления таблицей, но они ее убрали
        #table_buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, '_93444fe79c--icon--TTSKE')))
        # table_button = driver.find_elements_by_class_name("_93444fe79c--icon--TTSKE")
        #print(len(table_buttons))
        #ActionChains(driver).move_to_element(table_buttons[-1]).click().perform()
        while True:
            time.sleep(1)
            advs = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_93444fe79c--card--_yguQ")))
            #advs = driver.find_elements_by_class_name("objects_item_info_col_card_link")
            print(len(advs))
            if len(advs) == 0:
                raise Exception
            for counter, ad in enumerate(advs):
                print(counter)
                window_advs = driver.current_window_handle
                #print('old window: ', window_advs)
                ad.click()
                #print(driver.window_handles)
                new_window = driver.window_handles[1]
                #print('new: ', new_window)
                driver.switch_to.window(new_window)
                #print("cur: ", driver.current_window_handle)
                #print('url', driver.current_url)
                dic = parse_ad(driver)
                driver.close()
                driver.switch_to.window(window_advs)
                with open('data/data' + str(cur_reg) + '.csv', 'a', encoding='utf-8') as f:
                    writer = csv.writer(f, delimiter=';')
                    writer.writerow(dic.values())
            driver.refresh()
            time.sleep(2)
            next_page = driver.find_elements_by_xpath('//li[@class="_93444fe79c--list-item--2KxXr _93444fe79c--list-item--active--3dOSi"]/following-sibling::li')
            print(len(next_page))
            if next_page:
                next_page[0].location_once_scrolled_into_view
                ActionChains(driver).move_to_element(next_page[0]).click().perform()
                #next_page[0].click()
                time.sleep(3)
            else:
                break
        driver.quit()
    finally:
        time.sleep(5)


