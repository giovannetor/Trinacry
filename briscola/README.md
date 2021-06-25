# BrisBot2
Sopel bot created to host a match of BRISCOLA (typical Italian card game) on IRC

### [Game Rules](https://en.wikipedia.org/wiki/Briscola)

## Commands in-game for Users:
1. `.briscola` : Starts a match of Briscola. 
2. `.join` : Joins the match. (*IMPORTANT*: the game can be played with 4 OR 2 players.)
3. `.deal` : Deals the game. From now on, no player can join the match, and leaving will cause the other team to win.
4. `.ca` : Let the user see his cards.
5. `.teams` : Make the bot summerise the scores of each team.
6. `.quit` : Allows a player to quit the current match. If the match has been dealt, the other team will win.
7. `.lan` : Allows a user to change the game's language (*Avaible: Italian - English*). Can only be used after the start, but before the deal.
8. `.brhelp` : Notices the game commands and some hints.
9. `.rules` : Notices the game's rules 
10. `.poli` : Notices a quick table in game to show card's value as *Score* and *On Table*
11. `.rank` :  Makes the BOT send you your STATS  *(Score - Tot win - Tot played - Time played - Win Rate) *

## Commands in-game for Admins:
1. `.adrank` : (*PRIV MSG ONLY*) Makes the BOT send a rank of players based on a parameter *(win - tot - time - score - player (playernick))*
2. `.delplayer` : (*PRIV MSG ONLY and REQUIRES OWNER*) Delete a player from the Database.
3. `.adminstop` : Stops an ongoing game. No one wins.
4. `.brmove` : Moves the game to another channel.
5. `.brisgames` : Shows where the BOT has ongoing games.
### Note:
- The Module already has a DB inside. The files manager.py and models.py are no more required, since they have been included in the main code.
- Linux recomended.
- Uses SQlite 1.3.32 and Sopel 7.0.7 (check requirements.txt and INSTALL.md)
- ***IMPORTANT*** : the bot sends by default some logs to a channel named *#trinacry-logs*. You can remove the log feature, or change the chan name.
## TO IMPLEMENT:
- [X] Create a DB that keeps track of user's score. Probably using SQlite.
- [ ] The DB uses user's nicknames instead of usernames. Want to use usernames.
- [X] Add the Idle time. After some amount of time, an idle player gets kicked and the other team wins.
- [X] Add more and more detailed logs to report.
- [X] Fix 4 players matches (suspect there are a few bugs unresolved, lack of test dummy...)

![alt text](https://github.com/giovannetor/Trinacry/blob/main/perlogo_new.png)

