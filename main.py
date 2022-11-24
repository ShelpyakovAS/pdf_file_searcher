from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import requests
import io
from lxml import etree
import threading
import sys
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--threads_count', default='1')
    parser.add_argument('--browser', default='chrome')
    parser.add_argument('--headless', default='true')
    parser.add_argument('--method', default='selenium')
    return parser


def get_threads_list(count, method):
    threads_list = []
    for i in range(count):
        try:
            if method == 'selenium':
                threads_list.append(threading.Thread(target=searchers[i].search_pdf_by_selenium, args=(list_url.pop(),)))
            elif method == 'requests':
                threads_list.append(threading.Thread(target=searchers[i].search_pdf_by_requests, args=(list_url.pop(),)))
            else:
                raise f'Method {method} not found!'
        except IndexError:
            'pop from empty list'
    return threads_list


class Searcher:

    browsers_dict = {
        'chrome': {
            'options': ChromeOptions,
            'browser': webdriver.Chrome
        },
        'firefox': {
            'options': FirefoxOptions,
            'browser': webdriver.Firefox
        }
    }

    def __init__(self, browser_name, headless_mode):
        self.options = self.browsers_dict[browser_name]['options']()
        if headless_mode == 'true':
            self.options.headless = True
        self.browser = self.browsers_dict[browser_name]['browser'](options=self.options)

    def search_url(self):
        self.browser.get('https://www.cbr.ru/')
        time.sleep(2)
        url_links = ['https://www.cbr.ru/', ]
        button = self.browser.find_element(By.XPATH, '/html/body/header/div[5]/div/div/div[1]/div/div[1]/div/div')
        button.click()
        time.sleep(2)
        for locator in ["//*[contains(@class,'inner_links')]//a",
                        "//*[contains(@id,'menu_content_Activity')]//a",
                        "//*[contains(@id,'menu_content_FinancialMarkets')]//a",
                        "//*[contains(@id,'menu_content_Documents')]//a",
                        "//*[contains(@id,'menu_content_AboutBank')]//a",
                        "//*[contains(@id,'menu_content_Services')]//a"]:
            for link in self.browser.find_elements(By.XPATH, locator):
                url_links.append(link.get_attribute('href'))
        self.browser.quit()
        return url_links

    def search_pdf_by_selenium(self, link):
        self.browser.get(link)
        print(f'{link}')
        links_have_href = self.browser.find_elements(By.XPATH, '//a[@href]')
        for link in links_have_href:
            href = link.get_attribute("href")
            if '.pdf' in href:
                with open('selen_result.txt', 'a') as f:
                    f.write(href+'\n')
                f.close()

    def search_pdf_by_requests(self, link):
        data = requests.get(link).text
        print(f'{link}')
        parser = etree.HTMLParser()
        tree = etree.parse(io.StringIO(data), parser)
        for im in tree.xpath('//a'):
            if im.get('href'):
                if '.pdf' in im.get('href'):
                    with open('re_result.txt', 'a') as f:
                        if 'http' not in im.get('href'):
                            f.write('https://www.cbr.ru' + im.get('href') + '\n')
                        else:
                            f.write(im.get('href') + '\n')
                    f.close()

    '''def __del__(self):
        self.browser.quit()'''


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    searcher = Searcher(namespace.browser, namespace.headless)
    list_url = searcher.search_url()

    threads_count = int(namespace.threads_count)
    searchers = [Searcher(namespace.browser, namespace.headless) for i in range(threads_count)]

    while len(list_url) != 0:
        threads_list = get_threads_list(threads_count, namespace.method)
        for thread in threads_list:
            thread.start()
        for thread in threads_list:
            thread.join()





