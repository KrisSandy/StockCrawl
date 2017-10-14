import bs4 as bs
import urllib.request
import constants
import stock
import fileIO

def getStocks(maxStocks):

    html = urllib.request.urlopen(constants.baseUrl + constants.allStocksEndPoint)
    soup = bs.BeautifulSoup(html, 'lxml')

    stockTable = soup.find('table', class_='pcq_tbl MT10')

    count = 0

    for td in stockTable.findAll('td'):
        stockdata = stock.getStockInfo(td.find('a').get('href'))
        print(stockdata)
        fileIO.dict2csv(stockdata)
        count += 1
        if maxStocks != '*' and count == maxStocks:
            break

if __name__ == '__main__':
    getStocks(3)