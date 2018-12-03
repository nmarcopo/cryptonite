# Cryptonite, the Crypto Currency Forecaster

[Link to GitHub repository for reference](https://github.com/nmarcopo/programmingParadigmsProject)


## Members
* Austin Sura (asura) 
* Nicholas Marcopoli (nmarcopo) 
* Sung Hyun Shin  (sshin1)
* Chan Hee Song  (csong1)

## Features
- [x] Display current hottest and coldest N currencies
- [x] Crypto currency investement simulator
- [x] User specific crypto currency wallet
- [ ] Crypto currency investment recommender

## For November 7: OO API Due
### How to use this API:
Our API involves two functions that call an [external cryptocurrency API](https://min-api.cryptocompare.com) and several other functions that interact with a local database of users and their cryptocurrency investments. Our functions are as follows:  
#### \_crypto\_api
- find\_hottest\_coldest(days, topN, mode): Given an amount of days, this function will find the "hottest" or "coldest" topN cryptocurrencies, depending on the user's input. The "hottest" cryptocurrencies are those that have seen the greatest growth over a period of user specified days (from user specified previous days to the current day), and the "coldest" cryptocurrencies are those which have seen the greatest loss over that period. This information could be important to determining which cryptocurrency to buy.
- what\_if\_investment(days, cryptosAndAmount): Given an amount of days and a dictionary of cryptocurrencies and amounts of cryptocurrencies, this function will detect how much money in US Dollars a user would have made (or lost) if they invested in those currencies at that date.

#### \_user\_database
- set\_user(user, pwd): Create an entry in the database for a new user and set its password to a hashed password of what they selected as their password.
- check\_pwd(user, pwd): Checks when logging in to ensure that the entered password matches the user's password.
- change\_pwd(user, curr\_pwd, new\_pwd): Change a user's password, provided that they know their old one.
- change\_id(user, newID, pwd): Change the user's id, provided that they know the password.
- delete\_user(user, pwd): Remove a user from the database, as long as you know their username and password.
- add\_sub\_asset(user, asset\_dict): Change the amount of cryptocurrency a user has in their portfolio, given a dict of crypto and the amount they'd like to add or subtract.
- reset\_data(): Clear all users and their investments from the database.

### FOR THE GRADER: How to run the tests.
To run the tests, simply run the following command:  
`python3 test_api.py`  
The output will tell you if the API passed the tests.

## For November 28: Web Server Due
### RESTful JSON Specification
| Resources          | GET                           | PUT                          | POST                            | DELETE |
|--------------------|-------------------------------|------------------------------|---------------------------------|--------|
| /users/            |                               | Check password               | Make new id                     |        |
| /users/:uid        | Get user wallet info          | Change password              | Add new data                    |        |
| /users/change/     |                               | Change ID                    |                                 |        |
| /users/change/:uid |                               | Delete user                  | Delete coin from user wallet    |        |
| /crypto/           |                               | Get current crypto price     | find hottest and coldest crypto |        |
| /crypto/whatif/    |                               | what if investment simulator |                                 |        |
| /crypto/:temp      | Get top 5 hottest / coldest   |                              |                                 |        |
| /reset/            | Reset user db (test purposes) |                              |                                 |        |

- PUT to /users/
Returns success if id exists and pwd is correct, else error
- POST to /users/
Returns success if id and pwd is right, else error
- GET to /user/:uid
If user has wallet, return success with json array of cryptos and amount. Else returns error
- PUT to /users/:uid
Returns success if id and pwd is right, else error
- POST to /users/:uid
Returns success if id and pwd is correct, else error
- PUT to /users/change/
Returns success if id exists, old_id and pwd is correct, else error
- PUT to users/change/:uid
Returns success if id exists and pwd matches, else error
- POST to users/change/:uid
Returns success if id's wallet exists and coin exists in wallet, else error
- PUT to /crypto/
Returns success and top crypto data if fetching crypto api works, else returns error
- POST to /crypto/
Returns success and crypto price if fetching data works, else returns error
- PUT to /crypto/:days
Returns success and investment simulation data if fetching crypto api works, else returns error

### How to run/test this server:
Our Webservice is run from the webserver.py program. It is a cherrypy server that you run with the command `python3.6 webserver.py`, **WHILE** in the backend folder. We are using the port 52019  of student04.cse.nd.edu to host our server. Our webserver currently has functions to call all of the commands of our APIs. The webserver can register a user and password, and then have a wallet that corresponds to that user. We are currently working a webclient using bootstrap that supports the login process, but we are still working to integrate some of the main API functions. We created a test function that shows the correct implementation of the post/put/get commands. This test script can be run by starting the server and then running the command `python3.6 test_ws.py` also **WHILE** in the backend folder.
Explicit steps:  
1. Be on student04.cse.nd.edu
2. Be in the "backend" directory of our submission  
3. run the command `python3.6 webserver.py`     
4. To test: Run the command `python3.6 test_ws.py`  

## For December 3rd: Web Client/Watch Client
### How to run the Server
Our Webservice is run from the webserver.py program. It is a cherrypy server that you run with the command `python3.6 webserver.py`, **WHILE** in the backend folder. We are using the port 52019  of student04.cse.nd.edu to host our server. Our webserver currently has functions to call all of the commands of our APIs. The webserver can register a user and password, and then have a wallet that corres
ponds to that user. We are currently working a webclient using bootstrap that supports the login process, but we are still working to integrate some of the main API functions. We created a test function that shows the correct implementation of the post/put/get commands. This test script can be run by starting the server and then running the command `python3.6 test_ws.py` also **WHILE** in the backend folder.
Explicit steps:
1. Be on student04.cse.nd.edu
2. Be in the "backend" directory of our submission
3. run the command `python3.6 webserver.py`
4. To test: Run the command `python3.6 test_ws.py`
### How to view the Web Client
    1. Make sure the server is running properly following steps above.
    2. Go to student04.cse.nd.edu/nmarcopo/programmingParadigmsProject/frontend/web_client in a web browser
### How to run the Watch Client
    1. Download the entire CryptoWatch directory.
    2. Open the Project in Android Studio.
    3. Download the Project onto a smartWatch device.
    4. Make sure the server is running properly.
    5. Start and run application as you would with a normal application.
