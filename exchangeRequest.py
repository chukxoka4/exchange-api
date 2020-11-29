# 
# This script would enable you write the exchange rates against the EURO base from the date 2010-01-15
# The rates would be written to a HTML file in the same folder and also written to a Google Spreadsheet on your Google Drive 
#
from __future__ import print_function
import urllib.request # instead of urllib2 like in Python 2.7
import json
import pickle
import os.path
import webbrowser
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def postToGoogle(data):
    theJSON = json.loads(data)
    ratesList = theJSON["rates"]["2010-01-15"]


    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    credsy = 'credentials.json'
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credsy, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)
    values =[]
    for key, value in ratesList.items():
        values += [
        [
            key,value
        ]
        ]
    body = {
    'values': values
    }
    result = service.spreadsheets().values().update(
    spreadsheetId="Insert Sheet  Id", 
    range="Insert Sheet Range",
    valueInputOption='RAW', body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))

def printResults(data):
    # Use the json module to load the string data into a dictionary
    theJSON = json.loads(data)
    
    # create file

    html = """
<!DOCTYPE html>
<html>
<head>
  <meta content="text/html; charset=ISO-8859-1"
 http-equiv="content-type">
  <title>{title}</title>
</head>
<body>
<table border=1 style="width:50%; border-collapse: collapse; text-align: left; border: 1px solid #dddddd;">
     <tr>
       <th style="background-color: #dddddd;">Currency</th>
       <th style="background-color: #dddddd;">Exchange rate (base EUR)</th>
     </tr>
     <indent>
       {table}
     </indent>
</table></body></html>"""
    


    # now we can access the contents of the JSON like any other Python object
    if "EUR" in theJSON["base"]:
        title = ("Exchange rate" + " (base) " + theJSON["base"])
    # create a variable with the rates
    ratesList = theJSON["rates"]["2010-01-15"]
    table = ""
    for key, value in ratesList.items():
        setted = """<tr>
         <td>%s</td>
         <td>%s</td>
       </tr>"""
        table += setted % (key, value)
    content = html.format(**locals())
    f = open("exchangerates.html", "w+")
    f.write(content)
    # close file
    f.close()
    filename = 'file:///'+ os.getcwd()+'/' + 'exchangerates.html'
    print("File opening...")
    webbrowser.open_new_tab(filename)
    


def main():
  # open a connection to a URL using urllib2
  webUrl = urllib.request.urlopen("https://api.exchangeratesapi.io/history?start_at=2010-01-15&end_at=2010-01-15")
  
  # get the result code and print it
  print ("result code: " + str(webUrl.getcode()))
  if (webUrl.getcode() == 200):
        data = webUrl.read().decode("utf-8")
        # print out our customized results
        printResults(data)
        print("Check Containing folder for HTML file")
        postToGoogle(data)
  else:
        print("Received an error from server, cannot retrieve results " +
              str(webUrl.getcode()))

if __name__ == "__main__":
  main()