
# coding: utf-8

# In[1]:

import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import re
import datetime

#for gspread
import json
import gspread
from oauth2client.client import SignedJwtAssertionCredentials


# In[2]:

#constants to change
BASE_URL = 'http://stackoverflow.com/users/'
GMAIL_CREDENTIALS_JSON = '/Users/sarah/Downloads/API Project-8cfd2a9ceee5.json'
GSHEET_WORKBOOK_NAME = 'Growth Rate'
GSHEET_WORKBOOK_TAB_INDEX = 3 
GSHEET_STARTING_ROW_NUM = 2



# In[3]:

def googlesheet(gsheet_workbook_name, gsheet_workbook_tab_index):
    json_key = json.load(open(GMAIL_CREDENTIALS_JSON))
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), scope)
    gc = gspread.authorize(credentials)

    wks = gc.open(gsheet_workbook_name).get_worksheet(gsheet_workbook_tab_index)
    return wks


# In[4]:

def soup_response(base_url, user_num):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 ;Windows NT 6.1; WOW64; AppleWebKit/537.36 ;KHTML, like Gecko; Chrome/39.0.2171.95 Safari/537.36')]
    response = opener.open(base_url + str(user_num))
    soup = BeautifulSoup(response)
    return soup


# In[5]:

def month_num(month_string):
    return str(MONTHS_ARRAY.index(month_string) + 1)


# In[6]:

def find_month(text):
    return re.findall('-(\d{2})-', text)[0]


# In[7]:

def find_year(text):
    return re.findall('\d{4}', text)[0]


# In[8]:

def create_month_year(text):
    return find_month(text) + '/1/' + find_year(text)


# In[22]:




# In[11]:

wks = googlesheet(GSHEET_WORKBOOK_NAME, GSHEET_WORKBOOK_TAB_INDEX)
CURRENT_DATE = datetime.date(2000,1,1)
ROW_NUM = GSHEET_STARTING_ROW_NUM
ERROR_COUNT = 0
DONEZO = 0
MONTHS_ARRAY = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

while (DONEZO == 0):
    for user_num in range(9000000, 10000000, 10000):
        try:
            soup = soup_response(BASE_URL, user_num)
        except:
            print 'error', user_num, ERROR_COUNT, DONEZO
            ERROR_COUNT += 1

            if (ERROR_COUNT > 20):
                DONEZO = 1
                break
            continue

        ERROR_COUNT = 0
        
        pretext = soup.findAll('span', text = re.compile('Member for'))[0] #change based on website
        text = soup.find(text = re.compile('Member for')).findNextSibling('span')['title'] #change based on website
        
        date_string = create_month_year(text)
        date = datetime.date(int(find_year(text)), int(find_month(text)) , 1)

        if (date > CURRENT_DATE):
            CURRENT_DATE = date

            if user_num > 1:
                print date_string, user_num, DONZO
                wks.update_acell('A' + str(ROW_NUM), date_string)
                wks.update_acell('B' + str(ROW_NUM), user_num)
                ROW_NUM += 1


# In[ ]:



