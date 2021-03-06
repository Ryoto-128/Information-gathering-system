import time
import multiprocessing
from multiprocessing import Pool

from modules.fileIO import Csv
from modules.webdriver import Chrome


def get_list_url(target_url, corp_name, corp_location):
    ch = Chrome()
    with ch.driver as driver:
        driver.get(target_url)
        time.sleep(2)
        driver.find_element_by_id('keyword-suggest').find_element_by_class_name('a-text-input').send_keys(corp_name)
        driver.find_element_by_id('area-suggest').find_element_by_class_name('a-text-input').send_keys()
        driver.find_element_by_class_name('m-keyword-form__button').click()
        time.sleep(2)
        current_url = driver.current_url
        return current_url

def passContent(content):
    print('start thread')
    corp_name = content[0]
    green_url = content[1]
    corp_location = content[2]
    list_url = get_list_url(target_url, corp_name, corp_location)
    content = [corp_name, corp_location, green_url,list_url]
    fileIO.addCsv(output_path, content)



if __name__ == "__main__":
    target_url = 'https://itp.ne.jp/'
    input_path = './input.csv'
    output_path = './output.csv'
    target_row = [0,1,2]
    process_num = multiprocessing.cpu_count()
    # process_num = 2

    fileIO = Csv()
    csv_contents = fileIO.readCsv(input_path, target_row)
    process = Pool(process_num)
    process.map(passContent, csv_contents)