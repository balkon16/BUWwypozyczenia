from bs4 import BeautifulSoup #extract data from HTML
import re

def get_table_rows(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    ### find the table with history data
    history_table = soup.find("table", {"id": "history"})
    table_body = history_table.findChildren("tbody", recursive=False)
    print(table_body)
    table_rows = table_body[0].select("tr")
    for row in table_rows:
        print(row)
        print("###################################")

def find_page_no(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    ## Pozycje 1 do 10 z 361
    pozycja_napis = soup.find("div", {"class": "navigatorLabel"}).getText()

    pozycje = re.sub('[a-zA-Z]+', " ", pozycja_napis).split()

    strona = int(pozycje[1]) // 10

    if pozycje[0] == pozycje[1] == pozycje[2]:
        return strona + 1
    else:
        return strona
