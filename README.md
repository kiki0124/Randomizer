## Setup
1) Install all requirements: Run `pip install -r requirements.txt`
2) Go to [config.json](/config.json) and edit edit the following values:
    - `Token`- your app's token. Can be found in [Discord developer portal](https://discord.com/developers/applications) > your app's name > Bot (in the side bar) > Token. Make sure all Privileged Gateway Intents are enabled (scroll down a bit from where you copied the token)
    - `Items`- a list of items from which WinterBot will choose a random one with the selected interval. Example:
    ```json
    ["Item 1", "Item 2", "Item 3"]
    ```
    - `Prefixes`- a list of prefixes that can be used for message based commands. Example:
    ```json
    ["wb!", "~", ";"]
    ```
    - `Hours`- The of hours between each Guess message being sent.
    - `Minutes`- The delay of minutes between each Guess message being sent.
    - `Seconds`- The delay of seconds between each Guess message being sent.
    - `Channel_ID`- The ID of the channel where the Guess message should be sent. If you do not know how to get a channel's ID please take a look at [this tutorial](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID) 
3) Run [functions.py](/functions.py)- `python3 functions.py`
4) Start the app by running [main.py](/main.py)- `python3 main.py` A line saying that the app is online along with its name should be displayed in the console.
