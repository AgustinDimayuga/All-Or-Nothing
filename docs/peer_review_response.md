# Peer Review Feedback


## Jonathan Resendiz

### Code Review
1. Race condition in place_bet 

We added concurrency added in bets by checking their balance as we are updating it 
and if they don't have enough, then we don't let them place the bet.

2.	Typo in function name

We will quickly fix the typos

3.	F-string SQL in users.py

The status filter that we currently have shouldn’t be a security issue as we have a catch all case where if the user where to input something else for the status parameter, the status filter should be an empty string.

4.	Comments table has no game_id column

tables.py will be removed as it is not being used and our new changes are reflected in our database
5.	Parent_id is not null with no default

Same thing with the issue above
6.	get_user_creds crashes on bad username

We will fix this by adding one_or_none and by handling it in the case the user is None
7.	Wrong FK constraint name

We think that this is not a significant change as the program will still run fine as the issue that it will cause is not knowing which foreign key is which
8.	bets.amount is Integer in schema but float in API

This issue is in tables.py which will get removed as bets.amount is currently a float
9.	No comment explaining leaderboard wallet filter

We think that wallet.from_bet might be understandable as it a column that tracks if the balance change was from a bet or a deposit/withdraw. We also intended for pending bets to not show up as the leaderboard and negative numbers as bets may lose later on or you happen to go on a losing streak.
10.	No validation on limit/page in get_games

We will fix this by adding checks that make sure that the limit and page parameters are not being passed bad numbers. We will also try to be consistent across files
11.	comments.py is empty

We will remove this as the comments functionality is located in games.py
12.	server.py tag descriptions

We don’t think that this issue is relevant as the tag descriptions don’t really affect the functionality of the program
13.	League enum is hard-coded to two leagues

While we would have to update the enum everytime, new leagues are rarely added so we don’t think that this issue needs to be fixed


### API Specs
1.	API spec response for POST /auth/users doesn't match what the code returns

We will update the specs to reflect the new changes that we currently have by adding name and phone to the request and by only including access token and token type in the response
2.	games table has no result column

tables.py will be removed as it is not being used since the new changes is reflected in our database
3.	Wallet and bets store money as Integer

Same situation as above
4.	No unique constraint to prevent duplicate bets

Will remove the conflict error from the API spec as we are going to allow multiple bets for the same game and team since users may want to bet more money after their initial bet.

5.	Entire notifications system is in the spec but doesn't exist in code

We decided to not go forward with this so we will remove this from the API spec
6.	GET /bets/{bet_id} is in the spec but not implemented

We will address this by implementing this functionality

7.	DELETE /auth/tokens is in the spec but not implemented

We will remove this from the API specs as it is not being used
8.	Spec uses string IDs like "u_4f8a2c1b", code uses plain integers

We don’t think that this is relevant as the responses in the API spec are example ids
9.	GET /games requires both league and status with no defaults

We will fix this by having those parameters have default values
10.	comments table schema doesn't match how it's actually used

This is in tables.py which will be removed
11.	Leaderboard only supports daily/weekly, spec says monthly and all too

Will remove monthly option from API spec
12.	 GET /games returns a plain list, spec shows a paginated response envelope

Will update /games endpoint to reflect API spec

## Davis Responses:

1. I would use a decimal instead of a float for your money (amount, new_balance, etc) in your functions in bets.py because Decimal is best for money.

      a.  Definitely something worth catching, after changing our database structure we made sure the balance was in numeric data type to reflect the right decimal places.
2. I would also fix the place_bet function in bets.py because if a user wanted to place down many bets, then the check could happen after the update which allows to user to bet more money than they have.

      a. Now with the concurrency update, this problem was fixed (By Implementing Try and Catch block)

3. For place_bet function in bets.py, I would add a maximum and minimum bet limit.

      a. Although this would be a change to the our code I don't think this Idea would agree to our projects mission (Incentivise users to bet as much as possible). Although having a minimum would make sense and we did implement that.
4. For the error in place_bet function, I would add more to "Not enough money" by showing how much more money they need or how much they currently have.

      a. Code is now changed to display the error message and how much they have

5. You could also add another error for teams that don't exist in bets.py.

      a. This Error is already being displayed
6. I would also add a check for the odds/payout in place_bet to make sure its not a abnormal payout multiplier.

      a. Although  the odds are from a range of numbers, we insure the users are gaining profit so I don't think it's something worth looking at.

7. In place_bets for live games, I would change the odds to the new odds because someone could place a bet using old odds instead of new one. Otherwise, someone can place a bet that is very close to hitting with "before game odds". One option is to store the odds when bets are placed.

      a. During time of creation games are assigned odds for both hom and away teams so odds would not be changing based on who bets


8. Your comments.py is empty. If it's suppose to be empty, I would delete it to avoid confusion and to make your project cleaner.

      a. The file has now been deleted

9. In post_comment function for games.py, I would add a limit on how many comments a user can add or give them a time out if they post too many comments in a short amount of time to avoid spam comments.

      a. This is a reasonable constraint to add, and it had been implemented

10. In post_comment function for games.py, I would also block comments that use any explicit language or add a profanity count that when they get up to a certain number, they are banned.

      a. Definitely something to add. Profanity checking has been added

11. For get_leaderboard in leaderboard.py, I would have a case where it deals with ties.

      a. Great catch, This fix has been updated

12. For get_token_data in user_helper.py, I notice that you have print statements. If those are use for debugging, I would delete them to make your logs look cleaner.

      a. Print statements have now been deleted

13. For class League in games.py, MLB is spelled wrong (written as NLB)

      a. Changes have been made to Database
## Davis API Design Comments
1. The workflow examples have NBA but the actual available games don't match during testing

      a. Shortly after we Inserted more games which changed some things

2. Some workflows were missing required bearing token in request examples that caused authentication errors during testing

      a. The workflow was created before fully implementing the most updated version and there for the errors

3. In your APISpec.md, your POST auth/users has a 201 Response but testing returned 200

      a. Function has be changed to reflect  flow
4. For your error responses in APISpec, you have much more detail error responses than the ones in testing. I would use the original error messages.

      a. For user simplicity we decided to keep the messages simpler, although we are realizing that some of the responses are too simple

5. POST/bets/resolve in mentioned in APISpec but not in testing

      a. We decided to let a cronjob do that and therefore that spec because irrelevant

6. Money values should use Decimal instead of float to avoid rounding problems

      a. Already Addressed Above
7. The comments table in the APISpec should include the game_id also.

      a. database has been changed to reflect this concern
8. The notification endpoints were listed in APISpec but not in testing

      a. At first we intended to do notifications but for the sake of simplicity we decided to scratch that idea and let the user check based on when the game had ended
9. "409 Conflict — duplicate bet submission detected" is never explained in the APISpec what they do to prevent this

      a. While creating the project we realized that users should be able to bet on a team as much times as they want

      (sort of like when you can place the same parlay if that is a users intention)
10. The APISpec and Example Workflows use game_id as "g_1a2b3c4d" but in testing, it can only take integers

      a. the game_id was a place_holder value as an example for people who actually want to bet then it would be the game id of whatever game they would like to bet on
11. APISpec says leaderboard can have a monthly and all period but testing only shows daily/weekly

      a. we just thought a monthly leader board would not be as satisfactory for a user a weekly leaderboard so we just did not include it
12. Validation rules for usernames, passwords, emails, and phone numbers could be better explained in APISpec

      a. The API spec held some factors that had been changed since the commit, but we should have updated it


## Ethan Yang

### Code Review

1. In auth.py, many imports are duplicated 
(APIRouter, Depends, status, BaseModel). Cleaning duplicate imports would improve readability and maintainability.

We will quickly clean up our imports

2.  The password helper function is misspelled as verify_passwword, which can be easily renamed to the correct spelling.

This was fixed earlier from a earlier issue

3. get_user_creds() uses .one() instead of .one_or_none(). If a username does not exist, this may raise a database exception instead of returning an authentication failure.

We also fixed this issue earlier by adding .one_or_none()

4. JWT payloads are printed directly with print(payload) inside authentication logic. Sensitive token data generally should not be logged in production environments

We will remove those print statements to improve security

5. Exception handling also uses print(e) instead of structured logging. Using Python’s logging module would improve debugging and production monitoring

This was fixed by the issue above

6. In games.py, SQL queries use f-string interpolation for status_filter. Parameterized queries would be safer and more consistent.

As mentioned before, we only put in pre made strings into the query and any
user input goes through bind parameters so that we can avoid any security issues

7. place_bet() in bets.py contains validation, balance logic, odds logic, inserts, and response construction all in one function. Separating logic into service/helper layers would improve maintainability.

We think that this issue is not relevant as we are not using that many
inserts/updates

8. Wallet balances are recalculated repeatedly using SUM(change) queries. This works, but could become inefficient at larger scale with many transactions

We will fix this by adding a seperate table that keeps track of balances
that is not ledger based. We will update the user balances by using update queries.

9. users.py also contains repeated imports, suggesting linting/cleanup tools like Ruff are not fully enforced despite being included in dependencies.

We will remove these imports along with any other unused imports that appear in other files

10.  README.md contains minor spelling/grammar mistakes such as “docker contianer,” which can easily be fixed

We don't think that this is a relevant issue as these are only minor spelling mistakes that don't 
affect the functionality of the program

11. package.json still contains the default "Error: no test specified" script even though pytest is included elsewhere. This suggests testing setup/documentation could be improved

We don't think that this is a relevant issue as we are not running any tests through pytest

12. server.py defines OpenAPI metadata only for the bets tag even though multiple route groups exist (auth, games, users, leaderboard). Additional tag descriptions would improve Swagger documentation quality.

We will add short descriptions for the other routes

13. The comments schema forces parent_id to be non-nullable, which may prevent creation of true top-level comments.

This issue was addressed earlier as it was an issue with tables.py which was removed

14. Monetary values are stored as Integer in SQL while API models expose float values. Using a consistent numeric representation would reduce possible rounding/conversion issues

This issue appeared in tables.py which was removed. The database was updated to support float values instead of integers.

15. Authentication endpoints do not appear to implement rate limiting or brute-force protection

We think that this issue is out of scope for our project as we want to keep our project simple 
and implementing this is out of scope for this course.



### Design Review

1. Separating credentials into a user_cred table is a good normalization choice, but storing usernames separately in users makes authentication queries slightly more complex because extra joins are required.

While it does require an extra join, it helps with adding extra security so that 
a username doesn't get associated with a password if an attacker got data from the user_creds table

2. The wallet table works as a transaction ledger, but recalculating balances through aggregation queries could become expensive as transaction history grows. A cached balance field may help scalability.

We addressed this issue earlier by adding a new table that keeps track of balances and is not ledger based

3. The comments.parent_id column is non-nullable even though the schema appears to support nested comments. Allowing NULL parent IDs would make top-level comments easier to represent.

This issue is coming from tables.py which was removed. Our new changes are reflected in our database.

4. The API currently lacks explicit versioning such as /api/v1/, which could make future updates harder to manage without breaking clients.

We think that this issue is out of scope for our project as we are trying to keep our project simple
and is not a topic that was covered.

5. The route /games/game_details?id= works, but a route like /games/{id} would be cleaner and more RESTful.

We will rename this route to /games/{game_id} to better represent that the route
is going to a specific game

6. Error responses are inconsistent across endpoints. Some routes return plain strings while others return structured objects with error codes/messages. Standardizing the format would improve frontend integration.

We will address by configuring our endpoints to return HTTPExceptions for any errors that we encounter

7. The League enum currently only supports two hardcoded values (NLB and WORLD_CUP). Moving leagues into database-driven values would make the API more scalable.

We made an enum for leagues so that the user can pick between leagues that are currently available.
Also, leagues are rarely added and there are a very small amount of leagues compared to games.

8. JWT tokens currently only include user_id and name. Including roles or permission scopes would make future admin/moderation features easier to implement.

While it would make those features to easier to implement, they are 
out of scope for our project

9. Endpoint naming conventions are somewhat inconsistent (/leaderboard, /games, /auth/users). Standardizing naming patterns would make the API feel more polished.

Our current names for these endpoints best describe
what they are supposed to do so we think that this issue is not significant enough to change.

10. Monetary values are handled inconsistently because SQL stores them as integers while the API models expose floats. Using a single numeric representation would reduce possible rounding issues.

We configured our database to handle money as floats instead of integers so this shouldn't be an issue.

11. Pagination exists on several endpoints, but the API does not currently return pagination metadata such as total pages or next-page links. Adding metadata would improve frontend usability.

We addressed this issue earlier by adding that metadata into the result which was specified in the API spec.

12. The comments system supports nested comments through parent_id, but there does not appear to be a depth limit or recursion handling strategy, which could lead to extremely deep comment chains.

We don't think that this is an important issue as many comment threads can be really long.

13. The API documentation does not appear to document rate limits, authentication expiration behavior, or token refresh strategy, which could make integration harder for frontend developers.

While these are valid issues, they are out of scope for our project so we are not able to implement these features.

14. The leaderboard query recalculates earnings dynamically using joins and aggregation. Precomputing leaderboard statistics periodically could improve performance at larger scale.

We intended to dynamically query the leaderboard as many users could win their bets in a short time span so we want
those users to be able to see where they are on the leaderboard at any time

15. The API currently exposes only weekly and daily leaderboard periods. Making leaderboard intervals configurable would make the feature more flexible.

We don't believe that this issue is relevant as it is easier for users
to look up stats based on daily or weekly intervals as they are common intervals.

