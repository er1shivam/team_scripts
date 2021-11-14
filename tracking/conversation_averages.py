#Import Necessary Packages
import gspread
import pandas as pd
from datetime import datetime, timedelta
import os


def dictionary_of_reply_timestamps(df): #Creates dictionary of the conversation name as the key, and a list of the reply times as the value

	grouped_df = df.groupby(['Conversation','Date'])['Date'].unique()  #FIrst groups the conversation by uniques

	names_with_timestamps = { name : [] for name in sorted(list(set([name for name in df['Conversation']]))) if name} #Creates the dictionary based off the names of each conversation in the file
	
	for name in names_with_timestamps: 
		names_with_timestamps[name] = grouped_df[name].astype(str).to_list() #Shifts the lists of datetimes of replies from the dataframe to the dictionary

		formatted_strings = []

		for index,value in enumerate(names_with_timestamps[name]):
			formatted_strings.append(value[2:-2]) #Changes the string to account for intial weird formatting

			formatted_strings[index] = datetime.strptime(formatted_strings[index], '%Y-%m-%d %H:%M:%S') #Shifts the format from string to datetime
			names_with_timestamps[name] = formatted_strings #Changes the value of the key to the list of their reply times

	return names_with_timestamps

def get_conversation_average(names_with_timestamps): #Gets the time between each message in the list of reply times and returns a dictionary with the key being the conversation, and the value being a single number showing the average reply time

	conversation_average = { name : '' for name in names_with_timestamps if ''} #Creates the initial dictionary based on the keys in the dictionary created above

	for name in names_with_timestamps:
		for index,time in enumerate(names_with_timestamps[name]):
			if index+1 == len(names_with_timestamps[name]): #Ensures that it does not check the last element in the list, which would cause an error
				pass
			else:
				list_of_reply_times = []
				reply_time = names_with_timestamps[name][index+1] - names_with_timestamps[name][index] #Gets the reply time between the current message and the next message in the iteration
				list_of_reply_times.append(abs(reply_time)) #Appends the reply time to a list in order to find the average

				avg_time = sum(list_of_reply_times, timedelta()) / len(list_of_reply_times) #Gets the average reply time in that list of timestamps for the conversation

				conversation_average[name] = avg_time #Replaces the value of the Conversation key to a string representation of the average time

	return conversation_average


def get_full_average(df,conversation_average):

	times = []

	for name,time in conversation_average.items(): #Converts time into timestamp. Get error if the time is over 1 day. Not sure how to fix this so just used try, except
		try:
			obj = datetime.strptime(str(time), '%H:%M:%S').timestamp()
		except ValueError:
			pass
		else:
			times.append(obj)

	try: #takes the average time from the timestamps and returns it in datetime form.
		full_average = datetime.fromtimestamp(sum(times) / len(times)).strftime('%H:%M:%S')
	except ZeroDivisionError: #If there are no conversations, there will be no average and therefore this avoids error
			full_average = 'Not enough data'
	else:
		full_average = datetime.fromtimestamp(sum(times) / len(times)).strftime('%H:%M:%S')

	return full_average

def setup(worksheet): #Sets up everything we need from functions above
	df = pd.DataFrame(worksheet.get_all_records())
	names_with_timestamps = dictionary_of_reply_timestamps(df)
	conversation_average = get_conversation_average(names_with_timestamps)
	full_average = get_full_average(df,conversation_average)

	return full_average
	
def sheets_setup(): #Gets gspread going
	gc = gspread.oauth() 
	url = input('Which Google Sheet do you want data on? ') #Allows us to use any google sheet in the folder without changing code

	sh = gc.open_by_url(url)
	average_sheet = gc.open('Average Spreadsheet').worksheet('Account Averages') #Set variable so can in future push results
	daily_sheet = gc.open('Average Spreadsheet').worksheet('Daily Averages') #Same as above

	return sh, average_sheet, daily_sheet

def get_averages(): #Runs everything, but very monolithic and will be refactored

	sh, average_sheet, daily_sheet = sheets_setup()
	worksheet_list = sh.worksheets()
	metadata = []
	list_of_averages = []
	md_dict = {'Date': '','Account': '','Average Reply Time': ''} #Creates the dictionary to append to the metadata list
	
	for sheet in worksheet_list: #Runs on every sheet in the workbook
		
		worksheet = sh.worksheet(sheet.title)
		full_average = setup(worksheet)
		list_of_averages.append(full_average)

		md_dict['Account'] = sheet.title[9:]
		md_dict['Average Reply Time'] = full_average
		md_dict['Date'] = sheet.title[:8]
		metadata.append(md_dict.copy())
		print(f'{sheet.title[9:]} is done')

	df1 = pd.DataFrame(metadata)
	df1.to_csv('your_array.csv', header=False, index=False)
	df1 = pd.read_csv('your_array.csv', skiprows=[0]) #Removes headers to allow it to be added to google sheet. Output is google sheet with the dictionary for each sheet in the workbook

	average_sheet.append_rows([df1.columns.values.tolist()] + df1.values.tolist()) 

	times = []
	for time in list_of_averages:
		try:
			obj = datetime.strptime(time, '%H:%M:%S')
			obj = obj.timestamp()
		except TypeError:
			print('TypeError')
		else:
			times.append(obj)

	all_average = datetime.fromtimestamp(sum(times) / len(times)).strftime('%H:%M:%S') #Gets averages across accounts 
	daily_sheet.append_row([sheet.title[:8],all_average])
	os.remove('your_array.csv')


if __name__ == "__main__":
    get_averages()

