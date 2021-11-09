# JSON To CSV For Facebook Messages

This code is used to change the JSON files that are downloaded from Facebook, to CSV files that are easier to read. It also allows us to use pandas for data-analysis. The output is a CSV file based on the name of the folder that was put in

## Pre-Requisites

You will need a Facebook account to download messages from

## Installation
### 1. Ensure python3 is installed

1. ```brew install python3 ```

### 2. Download your message information from Facebook

[Click here for the explainer on how to get your information](https://www.facebook.com/help/212802592074644)

## Usage
### 1. Clone the code repository and install requirements

1. ```gh repo clone louisrae/team_scripts```
2. ```cd team_scripts/messages_to_csv```
3. ```virtualenv venv```
4. ```. venv/bin/activate```
5. ```pip3 install -r requirements.txt```

### 2. Unzip the downloaded information in your Downloads folder

### 3. (Optional) Rename the 'messages' directory to the name of the Facebook account you downloaded

### 4. Run python3 json_to_csv.py

### 5. Enter the name of the folder that you downloaded (ensure it is the top level directory e.g messages)








