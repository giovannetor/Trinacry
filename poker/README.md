<img src="https://github.com/giovannetor/Trinacry/blob/main/perlogo_small.png" alt="perlogo" width="110" height="100"> <img src="https://github.com/giovannetor/Trinacry/blob/main/T_LOGO_WHITE.png" alt="TTT_logo_white" width="100" height="100">
# POKER
Sopel module for Italian (traditional) Poker on IRC! 

### [Game Rules](https://www.pagat.com/poker/variants/italian.html)

## Commands In-Game for Users
1. `.poker` : Starts a match of Poker. 
2. `.join` : Joins the match.
3. `.deal` : Deals the game. From now on, no player can join the match.
4. `.cards` : Let the user see his cards.
5. `.fiches` : Make the use see his fiches.
6. `.leave` : Leave a phase. Doesn't leave the match.
7. `.stay` : Decide not to bet / change cards.
8. `.bet` : Makes you bet fiches.
9. `.change` : Makes you change cards. All the cards must be put in the same line, separated by a space.
10. `.ontable` : Shows how many fiches are there atm on the table.
11. `.value` : Hints the value of the cards in your hand.
12. `.quit` : Allows a player to quit the current match. Must be used 2 times.
13. `.language` : Allows a user to change the game's language (*Avaible: Italian - English*). Can only be used after the start, but before the deal.
14. `.pokerhelp` : Notices the game commands and some hints.
15. `.rules` : Notices the game's rules 
16. `.poli` : Notices a quick table in game to show card's value as *Score* and *On Table*
17. `.rank` :  Makes the BOT send you your STATS  *(Score - Tot win - Tot played - Time played - Win Rate)*

## Commands in-game for Admins:
1. `.adrank` : (*PRIV MSG ONLY*) Makes the BOT send a rank of players based on a parameter *(win - tot - time - score - player (playernick))*
2. `.delplayer` : (*PRIV MSG ONLY and REQUIRES OWNER*) Delete a player from the Database.
3. `.adstop poker` : Stops an ongoing game. No one wins.
4. `.brmove` : Moves the game to another channel.
5. `.brisgames` : Shows where the BOT has ongoing games.

### Note:
- Linux recomended.
- Uses Sopel v8.0.0.dev0
- ***IMPORTANT*** : the bot sends by default some logs to a channel named *#trinacry-logs*. You can remove the log feature, or change the chan name.
- ***IMPORTANT*** : the bot only works in the chan listed in `game_chan = []` (will implement the config in the future)



