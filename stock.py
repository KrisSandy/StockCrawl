import bs4 as bs
from selenium import webdriver
import constants

def getStockBasicInfo(info):

    print("Getting badic info")

    basicInfo = {}

    for item in info:
        if (':' in item):
            key, value = item.split(':')
            basicInfo[key.strip()] = value.strip()

    return basicInfo

def getStockFinancialLinkInfo(endPoint, history):

    print('Scraping ' + constants.baseUrl + endPoint + ' history = ' + str(history))

    driver = webdriver.Chrome(executable_path=constants.chromeDriverPath)

    driver.get(constants.baseUrl + endPoint)

    if (history == 0):
        try:
            if(driver.find_element_by_link_text('Previous Years »')):
                historyExist = 1
        except:
            historyExist = 0
    elif (history == 1):
        driver.find_element_by_link_text('Previous Years »').click()
        try:
            if (driver.find_element_by_link_text('Previous Years »')):
                historyExist = 1
        except:
            historyExist = 0
    elif (history == 2):
        driver.find_element_by_link_text('Previous Years »').click()
        driver.find_element_by_link_text('Previous Years »').click()

    html = driver.page_source

    driver.close()

    soup = bs.BeautifulSoup(html, 'lxml')

    infolinks = soup.find('div', class_='boxBg1').findAll('table')[2]

    infoData = {}
    years = []

    for td in infolinks.find('tr').findAll('td'):
        if (td.text != ''):
            years.append(td.text)

    entries = len(years)

    for tr in infolinks.findAll('tr', height='22px')[2:]:
        # infoRow = {}
        # empty = 1
        label = tr.find('td')
        heading = label.text
        headColspan = label['colspan']
        if (heading != '' and headColspan == '1'):
            for i in range(0,entries):
            #     infoRow[years[i]] = tr.findAll('td')[i+1].text
            #     if (infoRow[years[i]] != ''):
            #         empty = 0
            # if (empty == 0):
            #     infoData[heading] = infoRow
                infoData[heading + '_' + years[i]] = tr.findAll('td')[i+1].text

    return  historyExist, infoData

def getStockFinancials(links):

    print('Processing financial links')

    financialInfo = {}
    for link in links:
        if(link.text == 'Balance Sheet'):
            newLink = link.find('a').get('href').replace('balance-sheetVI', 'consolidated-balance-sheet')
            newLink = newLink[:newLink.find('#')]
            # stock['Balance Sheet'] = financials.getInfolinks(newLink)
            for i in range(0, constants.historyCount+1):
                historyExists, stockNumbers = getStockFinancialLinkInfo(newLink, i)
                for key, value in stockNumbers.items():
                    financialInfo['BS_' + key] = value
                if (historyExists != 1):
                    break

        elif(link.text == 'Profit & Loss'):
            newLink = link.find('a').get('href').replace('profit-lossVI', 'consolidated-profit-loss')
            newLink = newLink[:newLink.find('#')]
            # stock['Profile & Loss'] = financials.getInfolinks(newLink)
            for i in range(0, constants.historyCount+1):
                historyExists, stockNumbers = getStockFinancialLinkInfo(newLink, i)
                for key, value in stockNumbers.items():
                    financialInfo['PL_' + key] = value
                if (historyExists != 1):
                    break

    return financialInfo

def getStockInfo(url):

    print('Scraping ' + url)

    driver = webdriver.Chrome(executable_path=constants.chromeDriverPath)
    driver.get(url)
    html = driver.page_source
    driver.close()

    soup = bs.BeautifulSoup(html, 'lxml')

    stockInfo = {}

    stockInfo['name'] = soup.find('h1').text

    info = soup.find('div', id='nChrtPrc').find('div', class_='PB10').find('div', class_='FL gry10').text.split('|')
    stockInfo.update(getStockBasicInfo(info))

    links = soup.find('dl', id='slider').find_all('li')
    stockInfo.update(getStockFinancials(links))


    return stockInfo
