#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import lxml
import urllib.request as ur
import urllib.parse as up
from openpyxl import load_workbook
import random
import re

def GetFinDocs():

    stock_code = get_random_stock_info()[0]
    stock_name = str(get_random_stock_info()[1])

    print("stock code " + str(stock_code) + "\nstock name " + stock_name)

    edinet_query_url = "https://disclosure.edinet-fsa.go.jp/E01EW/BLMainController.jsp?uji.verb=W1E63010CXW1E6A010DSPSch&uji.bean=ee.bean.parent.EECommonSearchBean&TID=W1E63011&PID=W1E63010&SESSIONKEY=1501557262265&lgKbn=2&pkbn=0&skbn=0&dskb=&dflg=0&iflg=0&preId=1&row=100&idx=0&syoruiKanriNo=&mul={0}&fls=on&cal=1&era=H&yer=&mon=&pfs=4".format(stock_name)

    edinet_query_resp = ur.urlopen(edinet_query_url)

    edinet_query_soup = BeautifulSoup(edinet_query_resp, "html5lib")

    print(edinet_query_soup.prettify())

def main():

    random_stock_code = get_random_stock_info()[0]
    random_stock_name = get_random_stock_info()[1]
    print("stock name: {0}, stock code: {1}".format(random_stock_name, random_stock_code))

    goog_fin_url = "https://www.google.com/finance?q={0}&ei=hvteWZHBLs2K0gSrtLuADw".format(random_stock_code)
    print(goog_fin_url)

    goog_fin_resp = ur.urlopen(goog_fin_url)
    goog_fin_soup = BeautifulSoup(goog_fin_resp, "html5lib")

    try:
        hp_url = goog_fin_soup.find("a", id="fs-chome").text.replace("\n","")
    except:
        print("Didn’t find google finance link for {0}".format(random_stock_code))

    if hp_url.endswith("/"):
        hp_url = hp_url[:-1]

    print("Company homage page url: {0}".format(hp_url))

    hp_url_netloc = up.urlparse(hp_url).netloc

    hp_url_domain = re.match("(www\.)?([\u002D0-z]+)(?=\.)", hp_url_netloc).group(2)
    print("Company homepage domain: {0}".format(hp_url_domain))

    hp_url_resp = ur.urlopen(hp_url)

    hp_url_soup = BeautifulSoup(hp_url_resp, "html5lib")

    hp_url_links = [link.get('href') for link in hp_url_soup.find_all('a')]

    for link in hp_url_links:
        if link is None or link is "" or re.match("/r/n|/n", link):
            hp_url_links.remove(link)

    for link in hp_url_links:
        if link[0] == ".":
            link[0] = hp_url
        elif link[0] == "/":
            link = hp_url + link
        elif re.match("[A-z0-9]",link[0]) and link[:4] != "http":
            link = "{0}/{1}".format(hp_url, link)
        print(link)

    hp_url_domain_links = [link for links in hp_url_links if up.urlparse(link) == hp_url_netloc]

def get_random_stock_info():

    stocks_list_url = "http://www.jpx.co.jp/markets/indices/topix/tvdivq00000030ne-att/TOPIX_weight_jp.xlsx"

    resp_stocks_list_resp = ur.urlopen(stocks_list_url)

    stocks_list_wb = load_workbook(resp_stocks_list_resp)

    stocks_list_ws = stocks_list_wb.active

    stocks_list_headers = stocks_list_ws["A1:F1"][0]

    stock_codes = [code[0].value for code in stocks_list_ws["C1:C10000"] if code[0].value is not None]
    company_names = [name[0].value for name in stocks_list_ws["B1:B10000"] if name[0].value is not None]

    stock_info = dict(zip(stock_codes,company_names))

    rand_stock_code = random.choice(list(stock_info.keys()))
    rand_stock_name = stock_info.get(rand_stock_code)

    return [rand_stock_code, rand_stock_name]

if __name__=='__main__':
    main()
