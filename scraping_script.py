from bs4 import BeautifulSoup #extract data from HTML
import re

def get_table_rows(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    ### find the table with history data
    history_table = soup.find("table", {"id": "history"})
    table_body = history_table.findChildren("tbody", recursive=False)
    #print(table_body)
    table_rows = table_body[0].select("tr")
    #print(table_rows)
    for row in table_rows:
        print("###################################")
        if(len(row.find_all('td')) < 3):
            #handling situation when rows are like this:
            #<tr style="display: none;"><td></td><div></div></tr>
            continue
        yield get_data_from_row(row)

def get_data_from_row(row):
    date_raw, name_raw, type_raw = row.find_all('td')
    date = date_raw.find('div').get_text()
    name = name_raw.find('a').get_text()
    type = type_raw.find('div').get_text()
    return [date, name, type]


def find_page_no(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    pozycja_napis = soup.find("div", {"class": "navigatorLabel"}).getText()

    ## Pozycje 1 do 10 z 361 --> pozycje == ['1', '10', '361']
    pozycje = re.sub('[a-zA-Z]+', " ", pozycja_napis).split()

    strona = int(pozycje[1]) // 10

    if pozycje[0] == pozycje[1] == pozycje[2]:
        #last page
        return strona + 1
    else:
        return strona
