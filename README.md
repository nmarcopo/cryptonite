# Cryptonite, the Crypto Currency Forecaster

[Link to GitHub repository for reference](https://github.com/nmarcopo/programmingParadigmsProject)


## Members
* Austin Sura (asura) 
* Nicholas Marcopoli (nmarcopo) 
* Sung Hyun Shin  (sshin1)
* Chan Hee Song  (csong1)

## Features
- [x] Display current hottest and coldest N currencies
- [x] Cyrpto currency investement simulator
- [x] User specific crypto currency wallet
- [ ] Crypto currency investment recommender

## For November 7: OO API Due
### How to use this API:
Our API involves two functions that call an external cryptocurrency API and several other functions that interact with a local database of users and their cryptocurrency investments. Our functions are as follows:  
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
| Resources     | GET                  | PUT                             | POST         | DELETE      |
|---------------|----------------------|---------------------------------|--------------|-------------|
| /users/       |                      | Check password                  | Make new id  | Change ID   |
| /users/:uid   | Get user wallet info | Change password                 | Add new data | Delete user |
| /crypto/      |                      | find hottest and coldest crypto |              |             |
| /crypto/:days |                      | what if investment simulator    |              |             |
| /reset/       |                      | Reset user db (test purposes)   |              |             |

