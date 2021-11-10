# Average Times From Facebook Information

This code is meant to be used inside DFY Setters to calculate average reply time across multiple accounts

## Pre-Requisites

You will need the following accounts setup
1. settersandspecialists.com gmail account
2. [Github account (personal)](https://github.com)
3. [Google Cloud Account](https://cloud.google.com)

## Installation

### 1. Ensure python3, GitHub CLI and virtualenv are installed with

1. ```brew install python3 ```

2. ```brew install gh ```

3. ```brew install virtualenv ```

If you have not authenticated GitHub, follow the below steps

1. ```gh auth login ```

2. Select Github.com

3. Select HTTPS for Preferred Protocol

4. Type Y to authenticate GIT

5. Select login with a web browser

6. Follow the on-screen prompts

### 2. Download your client secret json file from Google Cloud
If you do not have your OAuth already setup

Follow these steps

1. Head to Google Developers Console and create a new project (or select the one you already have) This is in the top left next to the title. It may be labelled 'Select A Project'.

2. In the search boxat the top, search for “Google Drive API” and enable it.

3. In the search box at the top, search for “Google Sheets API” and enable it.

Once this is done, please follow steps 3-6 [here](https://docs.gspread.org/en/v4.0.1/oauth2.html#for-end-users-using-oauth-client-id)

### 3. Rename your client secret file to exactly credentials.json
Ensure that it is in your Downloads folder and names credentials.json

### 4. Setup the gspread config files and move credentials.json

1. ```mkdir .config/gspread```
2. ```cd .config/gspread```
3. ```cd ```
4. ```mv Downloads/credentials.json /Users/$USER/.config/gspread```


## Usage
### 1. Clone the code repository and install requirements

1. ```gh repo clone louisrae/team_scripts```
2. ```cd team_scripts/tracking```
3. ```virtualenv venv```
4. ```. venv/bin/activate```
5. ```pip3 install -r requirements.txt```


### 2. Navigate to folder and run conversation_averages.py

1. ```cd team_scripts/tracking```
2. ```python3 conversation_averages.py```


### 3. Paste desired link from Downloaded FB Messages [here](https://drive.google.com/drive/u/0/folders/1sAMiZQtCjCh7RNMJhnMedPmuHynONfAs)
NOTE: You must be on a settersandspecialists.com email to access this

### 4. Press enter and wait for code to run

### 5. Open Average Spreadsheets to see your average times [here](https://docs.google.com/spreadsheets/d/1XxCMbAsBuR8TYDEIgclfcgmpH_v6xVmKB4JmG8yRqs0/edit#gid=323658950)

## License
[MIT](https://choosealicense.com/licenses/mit/)
