# ./scripts/extraction.py
# ==================================================
# standard
import time, random
# requirements
from loguru import logger as watcher
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# --------------------------------------------------

def data_extraction() -> None:
    
    watcher.add(sink='./temp/file_{time}.log')
    
    with open('./temp/LINKS.txt', 'r') as f:
        txt_file = f.readlines()
        txt_file = [l.rstrip().split('-') for l in txt_file]
    
    download_path = './downloads/'
    xpath = '//*[@id="pdf"]/div/a[2]'
    preferences = {'download.default_directory': download_path, 'safebrowsing.enabled': 'false'}
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option ('prefs', preferences)
    service = Service(executable_path=ChromeDriverManager().install())
    
    driver = webdriver.Chrome(service=service, options=options)
    
    time.sleep(3)
    watcher.info('NAVEGADOR LISTO')
    
    for idl, link in txt_file[1203:]:
        watcher.info('HACIENDO: \n{}'.format(link))
        time.sleep(random.uniform(4, 6))
        
        driver.get(link)
        time.sleep(5)
        
        try:
            driver.find_element(By.XPATH, xpath).click()
        except:
            watcher.warning('NOT FOUND: {}\n'.format(idl))
            
            with open(f4 := './temp/NOTFOUND.txt', 'a') as nf:
                nf.write('{}\n'.format(idl))
            continue
        
        x = int()
        thresh = 10
        maxwait = 3
        
        while x < thresh:
            time.sleep(maxwait)
            x += 5
            watcher.info('Threshold: {}'.format(thresh-x))
    
    watcher.info('DESCARGA COMPLETADA: {}\n'.format(idl))
    driver.close()
    watcher.info('Done')
    
    print(f'Created files at: {download_path}, {f4}')
