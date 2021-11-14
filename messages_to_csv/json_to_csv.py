import json
import pandas as pd
import os
import gspread
from datetime import date

def sheets_setup(dir):
    today = date.today()
    gc = gspread.oauth() 
    sh = gc.create(f"{dir}'s messages ({today})")
    worksheet = sh.sheet1
    
    return worksheet


def create_dict(data):

    messages = data['messages']
    dlist = []
    newdict = {'Conversation': '','Sender': '','Message':'','Timestamp':''}
    for message in messages:
        newdict['Conversation'] = data['title']
        newdict['Sender'] = message['sender_name']
        newdict['Timestamp'] = message['timestamp_ms']
        try:
            newdict['Message'] = message['content']
        except KeyError:
            print('There was a KeyError, nothing to worry about')
        else:
            pass
        dlist.append(newdict.copy())

    return dlist

def get_filepaths():
    filelist = []
    dir = input('What is the name of the folder where the messages are located? Put the exact name: ')
    main_path = "/Users/"+os.environ['USER']+"/Downloads/"+dir+"/inbox/"
    for folder in os.listdir(main_path):
        if folder.endswith('.DS_Store'):
            pass
        else:
            for filename in os.listdir(main_path+folder):
                if filename.endswith('.json'):
                    filelist.append(main_path+folder+'/'+filename)
    
    return filelist, dir

def create_dataframe(todf):
    df = pd.DataFrame()
    for infile in todf:
        df = df.append(pd.DataFrame(infile),ignore_index=True)
    
    return df

def convert_json():
    filelist, dir = get_filepaths()

    todf = []
    for path in filelist:
        with open(path) as f:
            data = json.load(f)
            todf.append(create_dict(data))

    df = create_dataframe(todf)
    worksheet = sheets_setup(dir)
    worksheet.append_rows([df.columns.values.tolist()] + df.values.tolist()) 
    

if __name__ == "__main__":
   convert_json()