try:
    import pandas as pd 
    import time
    import re
    import requests
    #from urllib.request import urlopen
    from bs4 import BeautifulSoup
    import unicodedata
    import selenium
except Exception as err:
    str_lib = str(err).replace("No module named ", "").replace("'", "")
    print(" ATTENTION,  Missing library: '{0}' \n * Please Open Anaconda prompt and type: 'pip install {0}'".format(str_lib))


##https://www.youtube.com/watch?v=ndwuUzgAiPY
#url = 'http://www.moneycontrol.com/mutual-funds/performance-tracker/returns/large-cap-fund.html'
#ttt = pd.io.html.read_html(url)
#print(ttt)
#https://www.youtube.com/watch?v=MX33Yoa-EvE
#https://www.whoishostingthis.com/tools/user-agent/
#str_url = 'http://www.espn.com/nba/statistics/player/_/stat/assists/sort/avgAssists/year/2019/seasontype/2'


def Act_WaitTranslation(int_sec = 5):
    print('  * Wait for Translation {} secondes ...'.format(str(int_sec)))
    time.sleep(int_sec)

def fBl_ChineseInString(str_stringToTest):
    l_result = re.findall(r'[\u4e00-\u9fff]+', str_stringToTest)
    if l_result:    return True
    return False


def fBL_checkConnexion(o_page):
    try: 
        if o_page.status_code == 200: 
            return True
        else: 
            print(' Connexion close for the status code of the page is not 200 ' )
            print(' - Status code of the page is: ' + o_page.status_code)
    except: 
        print('  ERROR in fBL_checkConnexion: Connexion fails because the input is not a page')
    return False
    

def fDf_htmlGetArray_json(str_url, str_jsonCriteria = ""):
    try:
        o_page = requests.get(str_url)
    except:
        print(' ERROR in fDf_htmlGetArray_json: requests.get(str_url)')
        print(' - ', str_url)
        raise
    if not fBL_checkConnexion(o_page): 
        print(' ERROR in fDf_htmlGetArray_json: fBL_checkConnexion')
        print('  - URL in fDf_htmlGetArray_json is: ', str_url)
        return False
    #print(o_page.content)
    try:
        if str_jsonCriteria != '':  df = pd.DataFrame(o_page.json()[str_jsonCriteria])
        else:                       df = pd.DataFrame(o_page.json())
    except:
        print(' ERROR in fDf_htmlGetArray_json: pd.DataFrame(o_page.json()[str_jsonCriteria])')
        print(' - ', str_url)
        print(' - ', str_jsonCriteria)
        raise
    return df


#ipath= "ajgvdf	"
#print(fBl_ChineseInString(ipath))


def fDf_htmlGetArray_Soup(str_url, bl_th = False, bl_waitForTranslation = False, int_waitTime = 1, bl_cleanXA0 = True):  
    arr_result = []
    try:
        d_headers = {'User-Agent': 'Chrome/71.0.3578.98'}     #Chrome/71.0.3578.98      #Mozilla/5.0
        o_page = requests.get(str_url, headers = d_headers)
        if bl_waitForTranslation:       Act_WaitTranslation(int_waitTime)
    except:
        print(' ERROR in fDf_htmlGetArray_Soup: requests.get(str_url)')
        print(' -  ', str_url)
        raise
    if not fBL_checkConnexion(o_page): 
        print(' ERROR in fDf_htmlGetArray_Soup: fBL_checkConnexion(o_page): ')
        print(' -  ', str_url)
        return False    
    try:
        bs_soup = BeautifulSoup(o_page.content, "html.parser")      # lxml   # html5lib
        #bs_soup = bs_soup.replace(u'\xa0', ' ')
        #bs_soup.prettify(formatter = lambda x: x.replace(u'\xa0', ' '))
        #bs_soup.prettify(formatter = lambda x: x.replace(r'&nbsp;', ' '))
    except:
        print(' ERROR in fDf_htmlGetArray_Soup: BeautifulSoup(o_page.content, "html.parser")')
        print(' -  ', str_url)
        raise
    try:
        for o_table in bs_soup.find_all('table'):
            for o_row in o_table.find_all('tr'):
                # Balise Th = Text / Titre
                o_th = [o_cell.text.strip() for o_cell in o_row.find_all('th')]                
                if bl_th and o_th:      o_cells = o_th
                else:                   o_cells = []
                # Balise TD = Chiffre
                o_td = [o_cell.text.strip() for o_cell in o_row.find_all('td')]
                if o_td:                o_cells = o_cells + o_td
                elif o_th:              o_cells = o_th
                else:                   o_cells = []    
                # Clean Cells
                if bl_cleanXA0:
                    o_cells = [unicodedata.normalize("NFKD",cel_Text) for cel_Text in o_cells]
                    o_cells = [cel_Text.replace('\n', '  ').replace('\r', '') for cel_Text in o_cells]
                # add the row to result
                if o_cells:   arr_result.append(o_cells)
                # Chinese Translation - Recursive                
                if bl_waitForTranslation:
                    for cell in o_cells:
                        if fBl_ChineseInString(cell):
                            if int_waitTime > 60:
                                print('   *_* ERROR : still Chinese within Result: ', cell)
                                print('   *_!!!_* Cannot wait anymore, Do it manually: ')
                                print('   *_URL_* ', str_url)
                                break
                            elif int_waitTime > 20:     int_waitTime = int_waitTime + 20
                            elif int_waitTime > 10:     int_waitTime = int_waitTime + 10
                            else:                       int_waitTime = int_waitTime + 5
                            print('   *_* ERROR : still Chinese in Result: ', cell)
                            df_return = fDf_htmlGetArray_Soup(str_url, bl_th, True, int_waitTime)
                            return df_return
        df = pd.DataFrame(arr_result)
    except:
        print(' ERROR in fDf_htmlGetArray_Soup: LOOP on tables / rows / cells')
        print(' -  ', str_url)
        raise
    return df


#str_url = r'http://www.yuantaetfs.com/en/#/Orders/1066'
#d_headers = {'User-Agent': 'Chrome/71.0.3578.98'} 
#o_page = requests.get(str_url, headers = d_headers)
#bs_soup = BeautifulSoup(o_page.content, "html.parser")
#print(bs_soup)
#for o_ng in bs_soup.find_all('ng'):
#    for o_table in o_ng.find_all('table'):
#        print(o_table)




#df = fDf_htmlGetArray_Soup(str_url)
#str_path = r'C:\Users\laurent.tupin\IHS Markit\HK PCF Services Team - General\Auto_py\Fubon\Fubon20200124\test'
#df.to_csv(str_path + '.csv', header = False, index = False)
#df.to_excel(str_path + '.xlsx', sheet_name = 'Sheet1', header = False, index = False)



class c_Selenium_InteractInternet():
    # ----------------------------------------------------
    # To use Chrome Driver
    #  Go to chromedriver.chromium.org
    #  download and UnZip the folder
    #  Move it to Users/local/bin or C:\ProgramData\Anaconda3\Library\bin (Windows)
    # ----------------------------------------------------
    def __init__(self, str_url):
        self.driver = selenium.webdriver.Chrome()
        self.driver.get(str_url)
        
    def clic(self, str_buttonName, str_buttonxPath, l_buttonIfFailed):
        # ----------------------------------------------------
        # Right click on the button and chose Inspect
        # Spot the button Type
        # Right Click and Copy XPath, You get the XPATH
        # ----------------------------------------------------
        time.sleep(5)
        btn_click = self.driver.find_element_by_xpath(str_buttonxPath)
        if not str_buttonName.lower() in btn_click.text.lower():
            print('Link found was not {} but: {}'.format(str_buttonName, btn_click.text))
            for xPath in l_buttonIfFailed:
                time.sleep(5)
                btn_click = self.driver.find_element_by_xpath(xPath)
                print('Link is: {}'.format(btn_click.text))
                btn_click.click()
        else:   btn_click.click()
    
    def fillUp(self, str_buttonxPath, str_textToFill):
        time.sleep(2)
        fld_toFill = self.driver.find_element_by_xpath(str_buttonxPath)
        fld_toFill.send_keys(str_textToFill)
    
    def changeWindow(self, int_nbWindow):
        self.baseWindow = self.driver.window_handles[0]
        int_nbWindow = int_nbWindow % len(self.driver.window_handles)
        self.newWindow = self.driver.window_handles[int_nbWindow]
        self.driver.switch_to.window(self.newWindow)
        
    def changeWindowBack(self):
        try:        self.driver.switch_to.window(self.baseWindow)
        except:
            print('Could not go back to Base Window... Wron use of changeWindowBack... Make sure u used changeWindow before')
            self.driver.switch_to.window(self.driver.window_handles[0])







# ******************* Brouillon *******************
    
def fDf_htmlGetArray_Soup_brouillon(str_url):  
    #str_url = "https://www.cmegroup.com/trading/energy/crude-oil/light-sweet-crude_quotes_settlements_futures.html"
    #str_url = "http://www.data.jma.go.jp/obd/stats/etrn/view/monthly_s3_en.php?block_no=47401&view=1"
    
    d_headers = {'User-Agent': 'Mozilla/5.0'}     #Chrome/71.0.3578.98
    o_page = requests.get(str_url, headers = d_headers)
#    o_page = urlopen(str_url).read()
#    print(o_page.content)
    
    if not fBL_checkConnexion(o_page): 
        print(' - URL in fDf_htmlGetArray_Soup_brouillon is: ', str_url)
        return False
    bs_soup = BeautifulSoup(o_page.content, "html.parser")      # lxml   # html5lib
    #print(bs_soup)
    
    ## Create a txt file to save the array
    #with open('html.txt', 'w') as txt:
        
    # 'settlementsFuturesProductTable'
    # 'cmeTable cmeSettlementsFutures cmeFloatingHead'
    # 'cmeTable cmeSettlementsFutures'
    for o_table in bs_soup.find_all('table'):
    #for o_table in bs_soup.find_all('table', class_ = 'cmeTable cmeSettlementsFutures'):
        print('-----table------')
        time.sleep(0.5)
        for o_row in o_table.find_all('tr'):
            print('-----row------')
            print(o_row)
            o_ths = [o_th.text.strip() for o_th in o_row.find_all('th')]
            if not o_ths == []:
                print('-----th------')
                print(o_ths)            
            o_cells = [o_cell.text.strip() for o_cell in o_row.find_all('td')]
            if not o_cells == []:
                print('-----cell------')
                print(o_cells)  # txt.write(o_cell.text + ',')
            #txt.write('\n')




#str_url = 'http://www.yuantaetfs.com/WebAccess/Orders/Index?fundid=1066&date=20190927'            
#df_data = fDf_htmlGetArray_Soup(str_url)
#str_Pcf = '\\\\uk-pdeqtfs01\\E\\Data\\Lucerne\\Data\\SOLA PCF\\Auto_Py\\Yuanta\\Yuanta 20191001\\abc.csv'
#df_data.to_csv(str_Pcf, index = False, header = False, sep = ',')
  
            