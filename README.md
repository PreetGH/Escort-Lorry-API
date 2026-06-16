# Escort-Lorry-API
An API to get information about the current weather and next weather with mutations in the Roblox Game Escort Lorry

Official API of the Roblox game Escort Lorry to get information about the current weathers.

You can access the api at https://escort-lorry-api.onrender.com/weather and https://escort-lorry-api.onrender.com/status

# Documentation and How the API and the Discord bot works

In order to understand how this API works we need to understand how an stock bot like Kiro works.

### How an simple Roblox stock bot works:
A stock bot uses diffrent methods but the one that this bot also uses is **using an API**.
Basically the Roblox game owner will modify their stock scipts so when something like stock changes
it uses "HTTPService" to request/post info onto a API which stores the info there, Then the discord bot
can just request the API to get the information that the game owner posted and display it in Discord.

However this does limit games it uses as not all game owners have implemented an API system in their games.
Our game uses this method as well.

### How our API and Bot works:
We also use HTTPService to post our weather information on the API.
This is an example of what our payload looks like:

Input
```lua
     local body = HttpService:JSONEncode({
			serverId = SERVER_JOB_ID,
			playerCount = #Players:GetPlayers(),
			createdAt = serverCreationTime,
			weatherId = weatherId,
			name = weatherData.Name,
			emoji = weatherData.MutationEmoji,
			mutation = weatherData.Mutation,
			multiplier = weatherData.Multiplier,
			duration = weatherData.Time,
			timestamp = os.time(),
		})

		HttpService:RequestAsync({
			Url = API_URL,
			Method = "POST",
			Headers = {
				["Content-Type"] = "application/json",
				["x-api-key"] = API_KEY
			},
			Body = body
		})

```
Information stored in the API:
```json
  {
  "active_servers": 1,
  "data": {
    "7a8f0914-5012-4b40-86db-7bb3513c8551": {
      "createdAt": 1781537843,
      "duration": 120,
      "emoji": "⚪",
      "multiplier": 2,
      "mutation": "Common",
      "name": "Clear",
      "playerCount": 1,
      "serverId": "7a8f0914-5012-4b40-86db-7bb3513c8551",
      "timestamp": 1781545598,
      "weatherId": "Clear"
    }
  },
  "status": "ok"
}
```
On our backend which is run on Render, we have 2 endpoints "POST" and "GET". We use "POST" to post information onto the API like you see in this example, 
for security reasons you will need an API key in order to use "POST" so not anyone can flood our API with useless information. However "GET" does not require an API key and
can be used by anyone to get the information in the API.

On our discord python bot, we can use the module requests to "GET" the info on the API like this

First you will need to install the module in Command Prompt or a terminal using:
```bash
pip install requests
```

```python
import requests

url = "https://escort-lorry-api.onrender.com/weather"
data = requests.get(url).json()

print(data)
```
Then you can send it to your Discord webhook like this:
Also make sure to replace PASTE_YOUR_WEBHOOK_URL_HERE with your actual webhook url that you are
going to be sending to.
```python
WEBHOOK_URL = "PASTE_YOUR_WEBHOOK_URL_HERE"

messageData = {
# This is your message information
  "content" = data
}
requests.post(WEBHOOK_URL, json=messageData)
```
Furthermore to get specific information in the API, you can navigate it as you would for a table:
```python
data[(serverid)][name]
```
Because all "GET" really returns is a table, you can perform functions, comparasions etc like you would on a table.
Also an easy way to get info about a specific server is to "GET" from https://escort-lorry-api.onrender.com/weather/server-id (This is not tested)

### /status
Furthermore to the main API route https://escort-lorry-api.onrender.com/weather there is also https://escort-lorry-api.onrender.com/status

This route is to check weather the status of the API system by checking if there are any active Roblox servers online.
This is what the API information looks like:

No Roblox Servers Online:
```json
{"message":"No Roblox servers are reporting data","status":"critical","warning":true}
```
Roblox Servers Reporting back live:
```json
{"servers":1,"status":"healthy"}
```

Similar to the main route you can also treat the info from this route as an table but be reminded that the values change depending on the state of Roblox Servers
so for example data[message] wont work when there are servers reporting back live.
