# Peer Review Feedback


Jonathan Resendiz
1. Race condition in place_bet 

2.	Typo in function name
      a.	We will quickly fix the typos
3.	F-string SQL in users.py
      a.	The status filter that we currently have shouldn’t be a security issue as we have a catch all case where if the user where to input something else for the status parameter, the status filter should be an empty string.
4.	Comments table has no game_id column
      a.	tables.py will be removed as it is not being used and our new changes are reflected in our database
5.	Parent_id is not null with no default
      a.	Same thing with the issue above
6.	get_user_creds crashes on bad username
      a.	We will fix this by adding one_or_none and by handling it in the case the user is None
7.	Wrong FK constraint name
      a.	We think that this is not a significant change as the program will still run fine as the issue that it will cause is not knowing which foreign key is which
8.	bets.amount is Integer in schema but float in API
      a.	This issue is in tables.py which will get removed as bets.amount is currently a float
9.	No comment explaining leaderboard wallet filter
      a.	We think that wallet.from_bet might be understandable as it a column that tracks if the balance change was from a bet or a deposit/withdraw. We also intended for pending bets to not show up as the leaderboard and negative numbers as bets may lose later on or you happen to go on a losing streak.
10.	No validation on limit/page in get_games
       a.	We will fix this by adding checks that make sure that the limit and page parameters are not being passed bad numbers. We will also try to be consistent across files
11.	comments.py is empty
       a.	We will remove this as the comments functionality is located in games.py
12.	server.py tag descriptions
       a.	We don’t think that this issue is relevant as the tag descriptions don’t really affect the functionality of the program
13.	League enum is hard-coded to two leagues
       a.	While we would have to update the enum everytime, new leagues are rarely added and so we don’t think that this issue needs to be fixed

API Specs
1.	API spec response for POST /auth/users doesn't match what the code returns
      a.	We will update the specs to reflect the new changes that we currently have by adding name and phone to the request and by only including access token and token type in the response
2.	games table has no result column
      a.	tables.py will be removed as it is not being used since the new changes is reflected in our database
3.	Wallet and bets store money as Integer
      a.	Same situation as above
4.	No unique constraint to prevent duplicate bets
      a.	Will remove the conflict error from the API spec as we are going to allow multiple bets for the same game and team since users may want to bet more money after their initial bet.

5.	Entire notifications system is in the spec but doesn't exist in code
      a.	We decided to not go forward with this so we will remove this from the API spec
6.	GET /bets/{bet_id} is in the spec but not implemented
      a.	We will address this by implementing this functionality

7.	DELETE /auth/tokens is in the spec but not implemented
      a.	We will remove this from the API specs
8.	Spec uses string IDs like "u_4f8a2c1b", code uses plain integers
      a.	We don’t think that this is relevant as the responses in the API spec are example ids
9.	GET /games requires both league and status with no defaults
      a.	We will fix this by having those parameters have default values
10.	comments table schema doesn't match how it's actually used
       a.	This is in tables.py which will be removed
11.	Leaderboard only supports daily/weekly, spec says monthly and all too
       a.	Will remove monthly option from API spec
12.	 GET /games returns a plain list, spec shows a paginated response envelope
        a.	Will update /games endpoint to reflect API spec
