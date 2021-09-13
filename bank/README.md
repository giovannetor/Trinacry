<img src="https://github.com/giovannetor/Trinacry/blob/main/T_LOGO_BLACK.png" alt="TTT_logo_black" width="100" height="100"> <img src="https://github.com/giovannetor/Trinacry/blob/main/perlogo_small.png" alt="perlogo" width="110" height="100"> <img src="https://github.com/giovannetor/Trinacry/blob/main/T_LOGO_WHITE.png" alt="TTT_logo_white" width="100" height="100">
# BANK
Sopel module to manage an internal Money Bank on IRC! 

### Currency: TriCoins (₸)

## Commands for Users
1. (**cmd**) `.bank (<nick>)` : shows your (or another's) current amount of ₸.
1. (**cmd**) `.pay <nick> <value>` : pays a user with a certain amount of ₸. Be sure to have that amount before using it.
1. (**cmd**) `.help bank` : provides a help file on IRC.
## Commands for Admins
1. (**cmd**) `.give <nick> <value>` : gives to a user a certain amount of ₸.
1. (**cmd**) `.take <nick> <value>` : takes from a user a certain amount of ₸.
1. (**cmd**) `.transfer <nickfrom> <nickto> (<amount>)` : transfer all the ₸ from a nick to another (or just an amount. Optional.)


# SHOP
Sopel module to manage an internal Shop System on IRC!

## Commands for Users
1. (**cmd**) `.shop (<catalogue>)` : Enter the shop and see the catalogues available. (You can directly jump to the catalogue)
1. (**cmd**) `.buy <catalogue> <item_name> (<amount> default = 1)`: Buy an item from a certain catalogue.
1. (**cmd**) `.inventory` : Shows the items in your inventory.
1. (**cmd**) `.sell <item_name> (<amount> default = 1)` : Sell an item in your inventory. IMPORTANT: Items will be sold for half of their shop value.
1. (**cmd**) `.help shop` : Well...you're here, aren't you? :P

## Commands for Admins 
1. (**cmd**) `.inventory <user>` : Admins can see other people's inventories.

-ITEM COMMANDS-
1. (**cmd**) `.item info catalogue,item` _: Gives infos about a catalogue or a precise item. If you want only catalogue info, replace "item" with "/"
1. (**cmd**) `.item add catalogue,item_name,cost,quantity,(effect),(description)`: Adds an item to a catalogue. You can omit effect and description with "/"
1. (**cmd**) `.item rem catalogue,item` : Removes an item from the catalogue
1. (**cmd**) `.item usertake <user> <item_name> (<amount> def = 1)` : Take an (amount of) item from a user's inventory.
1. (**cmd**) `.item usertake <user> <catalogue>  <item_name> (<amount> def = 1)` : Give to a user an (amount of) item taken from a catalogue
1. (**cmd**) `.graphic`  : Test the logos, yuppi!

