import json
import pandas as pd
import os

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
            print('There are no messages for ' + message['sender_name'])
        else:
            pass
        dlist.append(newdict.copy())

    return dlist

def get_filepaths():
    filelist = []
    dir = input('What is the name of the folder where the messages are located? Put the exact name: ')
    main_path = "/Users/"+os.environ['USER']+"/Downloads/"+dir+"/inbox/"
    for folder in os.listdir(main_path):
        for filename in os.listdir(main_path+folder):
                filelist.append(main_path+folder+'/'+filename)
    
    return filelist, dir

def create_dataframe(todf):
    df = pd.DataFrame()
    for infile in todf:
        data = pd.DataFrame(infile)
        df = df.append(data,ignore_index=True)
    
    return df

def main():
    filelist, dir = get_filepaths()

    todf = []
    for path in filelist:
        with open(path) as f:
            data = json.load(f)
            todf.append(create_dict(data))

    df = create_dataframe(todf)
    df.to_csv(f"/Users/{os.environ['USER']}/Downloads/{dir}.csv")
    

if __name__ == "__main__":
   main()