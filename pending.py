import os, shutil
import json
import requests

from oauth2client import file, client, tools
from apiclient import discovery
from httplib2 import Http

#Google Scopes
SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()

if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v2', http=creds.authorize(Http()))

directory = "add your directory path here"
os.chdir(directory)
files = sorted(os.listdir(directory), key = os.path.getctime)

itemcount = len([name for name in os.listdir('.') if os.path.isfile(name)])

i = 0
for file in os.listdir(directory):
    i += 1 
    filename = os.fsdecode(file)
    filepath = directory + filename #completes our filepath

    #upload to google drive
    FilesDrive = ((FileName, False),)
    for FileName, convert in FilesDrive:
        metadata = {'title': FileName}
        res = DRIVE.files().insert(convert=convert, body=metadata,
        media_body=FileName, fields='mimeType, exportLinks,alternateLink').execute()
        if res:
            print('Uploaded "%s" (%s)' % (FileName, res['mimeType']))

    #Delete File in local folder
    for the_file in os.listdir(directory):
        file_path = os.path.join(directory, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        
        except Exception as e:
            print(e)
