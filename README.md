# Divvy-Bikes-Scraper

![image](https://user-images.githubusercontent.com/44789534/162628460-c75272bf-42a8-4a21-9e63-edabfe0a4a3f.png)

Divvy-Bikes-Scraper is a command-line tool that allows Divvy bike members to scrape their ride data from the Divvy website and export it to a CSV file. Divvy, which is operated by Lyft, does not have a public API for accessing ride data, so this tool utilizes reverse engineering techniques to make the necessary GraphQL requests.

To use the tool, users will need to have a Divvy account and provide their login credentials. The tool will then scrape the ride data from the Divvy website and export it to a CSV file, which can be opened with a spreadsheet program like Microsoft Excel or Google Sheets. The CSV file will include information such as the start and end dates of each ride, the start and end stations, the duration of the ride, as well as ride distance.

It was built in Python and uses the Requests library for web scraping. The GraphQL requests were reverse engineered using the Network tab in Chrome Dev Tools. 

## Instructions

1. Create a virtual environment by navigating into the project directory and running the following command:
```
python3 -m venv my_env
```

2. Install the necessary Python libraries from `requirements.txt` by executing the following:

```
pip3 install -r requirements.txt
```

3. Navigate to https://account.divvybikes.com/ride-history and log into your Divvy Bikes account
4. Open up your browswer's dev tools and navigate to the Network tab

<img width="1000" alt="image" src="https://user-images.githubusercontent.com/44789534/160257650-733f8b5f-e793-4d01-8e02-2c2f290436f8.png">


5. Copy the value of the `lyftAccessToken` stored in the `Cookie` request header and save it as your `AUTHORIZATION` secret it in the project's `.env` file. 

<img width="741" alt="image" src="https://user-images.githubusercontent.com/44789534/160257698-582de274-7e5d-46cc-a45c-5065d8cf6c4b.png">

  
  **Note**: you should be able to find this `PUT` request by its domain address (account.divvybikes.com)

6. Run the script by executing the following from your terminal

  ```python3 script.py```

7. Verify that the script executed correctly by checking the print statements in your terminal. You should also have a file called `my_divvy_data.csv` in the project directory now

TODO

- [x] Create `.env` file for authoirzation bearer token
- [x] Create `requirements.txt` file
- [ ] Clean up `script.py`
- [x] Write up instructions to run with screenshots in `README.md`
