# Average Times From Facebook Information

This code is meant to be used inside DFY Setters to calculate average reply time across multiple accounts

## Pre-Requisites

You will need the following accounts setup
1. settersandspecialists.com gmail account
2. Github account (personal)
3. GCP Account

## Installation

1. Ensure python3 and GitHub CLI are installed with

1. ```console
brew install python3
```


2. ```console
brew install gh
```

NOTE: You will need to verify your GitHub account using the onscreen prompts

2. Download your client secret json file from Google Cloud
If you do not have your OAuth already setup, please follow steps 1-6 [here](https://docs.gspread.org/en/v4.0.1/oauth2.html#for-end-users-using-oauth-client-id)

3. Rename your client secret file to exactly credentials.json
Ensure that it is in your Downloads folder

4. Setup the gspread config files and move credentials.json

```console
mkdir .config/gspread
cd .config/gspread
mv Downloads/credentials.json /Users/louisrae/.config/gspread
```

## Usage
1. Clone the code repository and install requirements

```console
gh repo clone louisrae/team_scripts
cd team_scripts
virtualenv venv
. venv/bin/activate
pip3 install -r requirements.txt
```

2. Navigate to folder and run conversation_averages.py

```console
cd team_scripts/tracking
python3 conversation_averages.py
```

3. Paste desired link from Downloaded FB Messages [here](https://drive.google.com/drive/u/0/folders/1sAMiZQtCjCh7RNMJhnMedPmuHynONfAs)
NOTE: You must be on a settersandspecialists.com email to access this

4. Press enter and wait for code to run

5. Open Average Spreadsheets to see your average times [here](https://docs.google.com/spreadsheets/d/1XxCMbAsBuR8TYDEIgclfcgmpH_v6xVmKB4JmG8yRqs0/edit#gid=323658950)

## License
[MIT](https://choosealicense.com/licenses/mit/)
