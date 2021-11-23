<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About The Project

Our team is not competitive enough. We need to focus more on tracking our core metrics and comparing them with other team members. I created this script to pull the 7d totals for the main metric for each position. It then pushes the leaderboard to CSV which I can then post on Slack. This is important ...

Here's why:
* If you give people a stopwatch, they will naturally track themselves
* People want to know where they stand
* Management can easily see who is performing and who is not

No leaderboard is perfect, and this is a work in progress. We have not got our metrics perfectly dialled in and there is still manual tracking done. However this is the start of a project that should allow us to infer data from the Level 10 Dashboard and therefore make better decisions


### Built With

* [gspread](https://docs.gspread.org/en/v4.0.1/)
* [pandas](https://pandas.pydata.org)


<!-- GETTING STARTED -->
## Getting Started

We need to make sure we have python and virtualenv installed so that we can download the packages. Follow the below packages then move to installation

1. ```brew install python3 ```

2. ```brew install virtualenv ```

### Prerequisites

You will need the following accounts setup
1. settersandspecialists.com gmail account
2. python, pandas, gspread (Follow the Getting Started Steps)

### Installation

See below for the steps to follow to set the code up on your computer

1. ```gh repo clone louisrae/team_scripts```
2. ```cd team_scripts/leaderboard```
3. ```virtualenv venv```
4. ```. venv/bin/activate```
5. ```pip3 install -r requirements.txt```
6. ```cd team_scripts/leaderboard```
7. ```python3 leaderboard.py```


<!-- USAGE EXAMPLES -->
## Usage

This is a very simple script to use. Once you have run it, you will recieve a csv in the same directory where this script is located

You can use that CSV to paste the results to Slack


<!-- ROADMAP -->
## Roadmap

- [] Format output ready for Slack
- [] Push to Slack daily
- [] Create leaderboards from other data in the Dashboard


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.


<!-- CONTACT -->
## Contact

Your Name - [Louis-Rae](louisrae@settersandspecialists.com)


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Will do this more in future
