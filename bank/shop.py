import sopel.plugin as plugin
from sopel.formatting import colors, CONTROL_BOLD, CONTROL_COLOR, CONTROL_NORMAL, CONTROL_ITALIC
#from sopel.modules.bank import bank_add, bank_rem
from bank import bank_add , bank_rem , coins  # Use for Trinacry


SHOP = CONTROL_BOLD + CONTROL_COLOR + colors.RED + "," + colors.BLACK + " ₸ SHOP ₸ " + CONTROL_NORMAL + " | "
USER_SHOP = CONTROL_BOLD + CONTROL_COLOR + colors.BLACK + "," + colors.RED + " ₸ SHOP ₸ " + CONTROL_NORMAL + " | "

LOG_CHAN = "#trinacry-logs"
shop_chan = "#shop"


def format_add(item , amount):
    add = USER_SHOP + CONTROL_BOLD + "[" + CONTROL_COLOR + colors.LIGHT_GREEN + "+" + CONTROL_NORMAL + CONTROL_BOLD + "]" + CONTROL_NORMAL + " ADDED " + str(amount)+" "+ str(
        item) + " to your Inventory. Check .inventory for more infos."
    return add


def format_rem(item , amount):
    rem = USER_SHOP + CONTROL_BOLD + "[" + CONTROL_COLOR + colors.RED + "-" + CONTROL_NORMAL + CONTROL_BOLD + "]" + CONTROL_NORMAL + " REMOVED " +str(amount)+" "+ str(
        item) + " from your Inventory. Check .inventory for more infos."
    return rem


def f_catalogue(bot, catalogue: dict, colour = "cyan"):
    try: bot.say(CONTROL_BOLD + CONTROL_ITALIC + "Here's the Catalogue for " + f_item(catalogue["set_title"]["effect"] , colour))
    except: bot.say(CONTROL_BOLD + CONTROL_ITALIC + "Here's the Catalogue you're looking for." )
    for item in catalogue:
        if item.split("_")[0] != "set":
            bot.say(f_item("ITEM: ", colour) + item + f_item(" COST: ", colour) + str(catalogue[item]["cost"])  + coins() + f_item(
            " STOCK: ", colour) + str(catalogue[item]["quantity"]) + f_item(" DESCRIPTION: ", colour) + str(
            catalogue[item]["description"] + f_item(" EFFECT: ", colour) + str(catalogue[item]["effect"])))
    bot.say(
        CONTROL_BOLD + CONTROL_ITALIC + "If you want to buy something, use .buy <catalogue_name> <item_name> (<amount>, default = 1). E.g. : .buy food ice_cream 2")


def f_inventory(bot, catalogue: dict, colour = "white"):
    bot.notice(CONTROL_BOLD + CONTROL_ITALIC + "Here's your Inventory!")
    for item in catalogue:
        bot.notice(f_item("ITEM: ", colour) + item + f_item(" COST: ", colour) + coins() + str(catalogue[item]["cost"]) + f_item(
            " STOCK: ", colour) + str(catalogue[item]["quantity"]) + f_item(" DESCRIPTION: ", colour) + str(
            catalogue[item]["description"] + f_item(" EFFECT: ", colour) + str(catalogue[item]["effect"])))
    bot.notice(CONTROL_BOLD + CONTROL_ITALIC + "If you want to buy something, visit #shop ")


def f_item(name, colour = "white"):
    colori = {"red": CONTROL_COLOR + colors.RED + "%s" + CONTROL_NORMAL,
              "cyan": CONTROL_COLOR + colors.CYAN + "%s" + CONTROL_NORMAL,
              "green": CONTROL_COLOR + colors.GREEN + "%s" + CONTROL_NORMAL,
              "yellow": CONTROL_COLOR + colors.YELLOW + "%s" + CONTROL_NORMAL,
              "lime": CONTROL_COLOR + colors.LIGHT_GREEN + "%s" + CONTROL_NORMAL,
              "black": CONTROL_COLOR + colors.BLACK + "%s" + CONTROL_NORMAL,
              "blue": CONTROL_COLOR + colors.BLACK + "%s" + CONTROL_NORMAL,
              "pink": CONTROL_COLOR + colors.LIGHT_PURPLE + "%s" + CONTROL_NORMAL,
              "purple": CONTROL_COLOR + colors.PURPLE + "%s" + CONTROL_NORMAL,
              "gray": CONTROL_COLOR + colors.LIGHT_GRAY + "%s" + CONTROL_NORMAL,
              "white": CONTROL_COLOR + colors.WHITE + "%s" + CONTROL_NORMAL}
    try:
        stringa = colori[colour] % str(name)
    except:
        stringa = str(name)
    return stringa


def add_item(bot,
             cat_sec: str,
             item_name: str,
             cost: int,
             quantity: int,
             effect: str,
             description: str):
    catalogue = bot.db.get_plugin_value("shop", cat_sec, default = {})
    if catalogue == {}:
        bot.say(SHOP + "Catalogue " + f_item(cat_sec, "white") + " has been created.")
    if effect == "/":
        effect = None
    if description == "/":
        description = "No description provided."

    if item_name not in catalogue:
        catalogue[item_name] = {"cost": cost, "quantity": quantity, "effect": effect, "description": description}
        bot.db.set_plugin_value("shop", cat_sec, catalogue)
        bot.say(SHOP + "Item " + f_item(item_name, catalogue["set_col"]["effect"]) + " successfully " + f_item("ADDED",
                                                                                       "lime") + " the catalogue " + f_item(
            cat_sec, catalogue["set_col"]["effect"]) + " with the following data: " + CONTROL_ITALIC + str(catalogue[item_name]))
    else:
        bot.say(SHOP + "Item " + f_item(item_name, catalogue["set_col"]["effect"]) + " is already in the catalogue " + f_item(cat_sec,
                                                                                                      catalogue["set_col"]["effect"]) + " with the following data: " + CONTROL_ITALIC + str(
            catalogue[item_name]))


def info_item(bot, cat_sec: str, item_name: str):
    catalogue = bot.db.get_plugin_value("shop", cat_sec)

    if not catalogue:
        bot.say(SHOP + "Catalogue " + f_item(cat_sec, "white") + " doesn't exist.")
        return
    if item_name == "/":
        bot.say(SHOP + "Catalogue " + f_item(cat_sec, catalogue["set_col"]["effect"]) + " Info: " + str(catalogue.keys()))
        return
    if item_name not in catalogue:
        bot.say(SHOP + "The item " + f_item(item_name, "white") + " IS NOT in the catalogue " + f_item(cat_sec,
                                                                                                      catalogue["set_col"]["effect"]) + ".")
        return

    bot.say(SHOP + "Item INFO: " + f_item(item_name, catalogue["set_col"]["effect"]) + " in catalogue " + f_item(cat_sec,
                                     catalogue["set_col"]["effect"]) + CONTROL_ITALIC + ":   " + str(catalogue[item_name]))


def del_item(bot, cat_sec: str, item_name: str):
    catalogue = bot.db.get_plugin_value("shop", cat_sec)
    if not catalogue:
        bot.say(SHOP + "Catalogue " + f_item(cat_sec, "white") + " doesn't exist.")
        return
    elif item_name not in catalogue:
        bot.say(SHOP + "The item " + f_item(item_name, "white") + " IS NOT in the catalogue " + f_item(cat_sec,
                                                                                                      catalogue["set_col"]["effect"]) + ".")
        return
    catalogue.pop(item_name)
    bot.db.set_plugin_value("shop", cat_sec, catalogue)
    bot.say(SHOP + "Item " + f_item(item_name, catalogue["set_col"]["effect"]) + " successfully " + f_item("DELETED",
                                                                                   "red") + " from the catalogue " + f_item(
        cat_sec, catalogue["set_col"]["effect"]) + ".")
    if len(catalogue) == 0:
        bot.say(SHOP + "Catalogue " + f_item(cat_sec, catalogue["set_col"]["effect"]) + " is empty, so has been deleted.")


@plugin.commands("graphic")
@plugin.require_admin("Only admin can test.")
def testshop(bot, trigger):
    bot.say("Here's the shop admin graphic: " + SHOP)
    bot.say("Here's the shop user graphic: " + USER_SHOP)


@plugin.commands("item info")
@plugin.require_admin("Only admins can use this command.")
def item_info(bot, trigger):
    #if trigger.sender != LOG_CHAN:
    #    bot.say("Please use this command in the admin channel.")
    #    return
    if not trigger.group(2):
        bot.notice("Syntax: .item info <catalogue>,(<item_name>).   E.g.: .item del food,pizza", LOG_CHAN)
        bot.notice("IMPORTANT: by omitting the item_name with '/', you'll receive infos on the Catalogue.", LOG_CHAN)
        return

    string = trigger.group(3)
    try:
        catalogue_section, item_name = string.split(",")
    except:
        bot.say("Missing one or more required fields.")
        return
    info_item(bot, catalogue_section, item_name)


@plugin.commands("item add")
@plugin.require_admin("Only admins can add items to the Catalogue. Please, contact one if you need one.")
def item_add(bot, trigger):
    #if trigger.sender != LOG_CHAN:
    #    bot.say("Please use this command in the admin channel.")
    #    return
    if not trigger.group(2):
        bot.notice("Syntax: .item add CATALOGUE_SECTION,ITEM_NAME,COST,QUANTITY,(EFFECT),'(DESCRIPTION)'", LOG_CHAN)
        bot.notice(
            "You can omit EFFECT and DESCRIPTION by writing '/' instead. E.g.: .item add food,pizza,5,10,/,typical_italian_food",
            LOG_CHAN)
        bot.notice("IMPORTANT: spaces must be '_' or only the 1st word will be taken.", LOG_CHAN)
        return

    string = trigger.group(3)

    try:
        catalogue_section, item_name, cost, quantity, effect, description = string.split(",")
        des = ""
        for i in description.split("_"):
            des += i + " "
    except:
        bot.say("Missing one or more required fields.")
        return

    add_item(bot, catalogue_section, item_name, int(cost), int(quantity), effect, des)

@plugin.commands("item usergive")
@plugin.require_admin("Only admins can put items in Inventories.")
def item_usergive(bot, trigger):
    #if trigger.sender != LOG_CHAN:
    #    bot.say("Please use this command in the admin channel.")
    #    return
    if not trigger.group(2):
        bot.notice("Syntax: .item usergive USER CATALOGUE ITEM_NAME AMOUNT(def = 1)", LOG_CHAN)
        return
    try:
        item_name = trigger.group(5)
        cat_name = trigger.group(4)
        user_name = trigger.group(3)
        user_inventory = bot.db.get_nick_value(user_name, "inventory", default = {})
        catalogue = bot.db.get_plugin_value("shop" ,cat_name , default = {})
        if inventory == {}:
            bot.say(SHOP + user_name + "'s Inventory is Empty.")
            return
        if catalogue == {}:
            bot.say(SHOP + "Catalogue " + cat_name + " doesn't exist.")
            return
        if item_name.lower() not in catalogue:
            bot.say(SHOP + item_name + " not in " + trigger.group(3) + "'s Inventory.")
            return

    except:
        bot.say(SHOP + "You're missing one or more parameters.")
        return

    try: amount = int(trigger.group(6))
    except: amount = 1
    if amount < 0:
        bot.say(SHOP + "You can't add negative amounts. Use .item usertake to remove items from a user inventory.")
        return

    if item_name not in user_inventory:
        user_inventory[item_name] = {"cost": catalogue[item_name]["cost"], "quantity": amount,
                                     "effect": catalogue[item_name]["effect"],
                                     "description": catalogue[item_name]["description"]}
    else:
        user_inventory[item_name]["quantity"] += amount

    bot.say(SHOP + f_item("ADDED ", "green") + str(amount) + " " + f_item(item_name,
                "white") + " to the Inventory of " + f_item(trigger.group(3), "cyan") + ".")

    bot.say(format_add(item_name , amount), trigger.nick)
    bot.db.set_nick_value(trigger.nick, "inventory", user_inventory)



@plugin.commands("item usertake")
@plugin.require_admin("Only admins can remove items from Inventories.")
def item_usertake(bot, trigger):
    #if trigger.sender != LOG_CHAN:
    #    bot.say("Please use this command in the admin channel.")
    #    return
    if not trigger.group(2):
        bot.notice("Syntax: .item usertake USER ITEM_NAME AMOUNT(def = 1)", LOG_CHAN)
        return
    inventory = bot.db.get_nick_value(trigger.group(3), "inventory", default = {})
    if inventory == {}:
        bot.say(SHOP + trigger.group(3) + "'s Inventory is Empty.")
        return
    item_name = trigger.group(4)
    if trigger.group(4).lower() not in inventory:
        bot.say(SHOP + item_name + " not in " + trigger.group(3) + "'s Inventory.")
        return

    try: amount = int(trigger.group(5))
    except: amount = 1
    if amount < 0:
        bot.say(SHOP + "You can't remove negative amounts. Use .item usergive to put items in a user inventory.")
        return

    if amount == "*":
        inventory.pop(item_name)
        bot.say(SHOP + "Item " + f_item(item_name, "white") + " successfully " + f_item("DELETED",
                                                                                       "red") + " from the Inventory .")
    else:
        inventory[item_name]["quantity"] -= int(amount)
        bot.say(SHOP + f_item("REMOVED ", "red") + str(amount) + " " + f_item(item_name,
                                                                              "white") + " from the Inventory of " + f_item(
            trigger.group(3), "cyan") + ".")
        if inventory[item_name]["quantity"] <= 0:
            inventory.pop(item_name)

    bot.db.set_nick_value(trigger.nick, "inventory", inventory)
    bot.say(format_add(item_name , amount), trigger.nick)
    if len(inventory) == 0:
        bot.say(SHOP + "Inventory is empty, so has been deleted.")


@plugin.commands("item del", "item rem")
@plugin.require_admin("Only admins can remove items from the Catalogue.")
def item_del(bot, trigger):
    ##if trigger.sender != LOG_CHAN:
    #    bot.say("Please use this command in the admin channel.")
    #    return
    if not trigger.group(2):
        bot.notice("Syntax: .item del <catalogue>,<item_name>", LOG_CHAN)
        bot.notice("E.g.: .item del food,pizza", LOG_CHAN)
        return

    string = trigger.group(3)

    try:
        catalogue_section, item_name = string.split(",")
    except:
        bot.say("Missing one or more required fields.")
        return

    del_item(bot, catalogue_section, item_name)


@plugin.commands("item")
@plugin.require_admin("Only admins can use Item commands.")
def item_helper(bot, trigger):
    if not trigger.group(2):
        bot.say("Available commands: info | del | add | usertake | usergive ")


# def catalogue_getter(bot , catalogue_name):
#    catalogue = bot.db.get_plugin_value("shop", cat_sec)
#    if not catalogue:
#        return False
#    return  catalogue

@plugin.commands("shop")
@plugin.require_chanmsg("Please, use this command in #shop .")
def shop(bot, trigger):
    if trigger.sender != shop_chan:
        bot.say("Please, use this command in #shop .")
        return
    if not trigger.group(3):
        bot.say(
            USER_SHOP + "Welcome to TriShop! We have the following Catalogues available to visit: " + f_item("FOOD ", "red") + f_item("MIX " , "green") + f_item("BONUS " , "purple"))
        bot.say(USER_SHOP + "To visit a Catalogue, use .shop <catalogue name>")
    else:
        name = trigger.group(3)
        catalogue = bot.db.get_plugin_value("shop", name.lower(), default = {})
        if catalogue == {}:
            bot.say(USER_SHOP + "Catalogue " + f_item(name.lower(), "white") + " is empty.")
            return

        try: colour = catalogue["set_col"]["effect"]
        except:  colour = "white"
        f_catalogue(bot, catalogue , colour)


@plugin.commands("inventory", "inv")
def inventory(bot, trigger):
    if trigger.group(3) and trigger.admin:
        inventory = bot.db.get_nick_value(trigger.group(3), "inventory", default = {})
    elif trigger.group(3) and not trigger.admin:
        bot.say(USER_SHOP + "Only admins can see other's Inventories.")
        return
    else:
        inventory = bot.db.get_nick_value(trigger.nick, "inventory", default = {})
    if inventory == {}:
        bot.notice(USER_SHOP + "Your inventory is empty. Might want to buy something?")
        return
    f_inventory(bot, inventory, "white")

@plugin.commands("sell")
@plugin.require_chanmsg("Please, use this command in #shop .")
def sell(bot , trigger):
    if trigger.sender != shop_chan:
        bot.say("Please, use this command in #shop .")
        return
    if not trigger.group(3):
        bot.reply(f_item("ERROR: ", "red") + "Please, write an item to Sell. Remember that Items are sold for half their value.")
        return

    if not trigger.group(4):
        amount = 1
    else:
        amount = int(trigger.group(4))

    item_name = trigger.group(3)
    user_inventory = bot.db.get_nick_value(trigger.nick, "inventory", default = {})
    user_money = bot.db.get_nick_value(trigger.nick, "coins")

    if item_name not in user_inventory:
        bot.say(USER_SHOP + "The item " + f_item(item_name , "cyan") + " isn't in your Inventory.")
        return
    if amount > user_inventory[item_name]["quantity"]:
        bot.say(USER_SHOP + "You asked to sell " + f_item(str(amount) , "pink") + " items but you only have "
                + f_item(str(user_inventory[item_name]["quantity"]) , "pink") + " in your Inventory.")
        return
    to_earn = amount * int(user_inventory[item_name]["cost"] // 2)
    user_inventory[item_name]["quantity"] -= amount
    if user_inventory[item_name]["quantity"] == 0:
        user_inventory.pop(item_name)


    user_money += to_earn
    bank_add(bot, trigger.nick, to_earn, "Selling: " + item_name + ". Amount: " + str(amount))
    bot.say(format_rem(item_name , amount), trigger.nick)
    bot.db.set_nick_value(trigger.nick, "inventory", user_inventory)
    bot.say(USER_SHOP + "Successfully sold the item for " + str(to_earn) + coins())


@plugin.commands("buy")
@plugin.require_chanmsg("Please, use this command in #shop .")
def buy(bot, trigger):
    if trigger.sender != shop_chan:
        bot.say("Please, use this command in #shop .")
        return
    if not trigger.group(3):
        bot.reply(f_item("ERROR: ", "red") + "Please, write a Catalogue.")
        return
    if not trigger.group(4):
        bot.reply(f_item("ERROR: ", "red") + "Please, write an Item to buy.")
        return
    if not trigger.group(5):
        amount = 1
    else:
        amount = int(trigger.group(5))
    cat_name, item_name = trigger.group(3).lower(), trigger.group(4).lower()
    catalogue = bot.db.get_plugin_value("shop", cat_name.lower(), default = {})
    if catalogue == {}:
        bot.say(f_item("ERROR: ", "red") + "Catalogue " + f_item(
            cat_name) + " doesn't exist. Wrong format? Remember to replace spaces with '_'")
        return
    if item_name.lower() not in catalogue:
        bot.say(f_item("ERROR: ", "red") + "Item " + f_item(item_name) + " isn't in " + f_item(
            cat_name , catalogue["set_col"]["effect"]) + ". Wrong format? Remember to replace spaces with '_'")
        return
    bot.say(USER_SHOP + "Your order is being processed. Might require a bit.")

    user_inventory = bot.db.get_nick_value(trigger.nick, "inventory", default = {})
    user_money = bot.db.get_nick_value(trigger.nick, "coins")

    cost = amount * catalogue[item_name]["cost"]
    if catalogue[item_name]["quantity"] == 0:
        bot.say(
            USER_SHOP + "The item " + item_name + " is temporarily over. Contact an admin if you'd like more added!")
        return
    if user_money < cost:
        bot.say(USER_SHOP + "I'm really sorry, but you don't have enough money.")
        return
    if amount > catalogue[item_name]["quantity"]:
        bot.say(USER_SHOP + "I'm really sorry, but the shop only has " + f_item(str(catalogue[item_name]["quantity"]),
                                                                                "pink") + " while you requested " + f_item(
            str(amount), "pink") + ".")
        return

    if item_name not in user_inventory:
        user_inventory[item_name] = {"cost": catalogue[item_name]["cost"], "quantity": amount,
                                     "effect": catalogue[item_name]["effect"],
                                     "description": catalogue[item_name]["description"]}
    else:
        user_inventory[item_name]["quantity"] += amount

    catalogue[item_name]["quantity"] -= amount
    if catalogue[item_name]["quantity"] == 0:
        bot.say(
            USER_SHOP + "The item " + f_item(item_name , catalogue["set_col"]["effect"]) + " is temporarily over. Contact an admin if you'd like more added!")

    bot.db.set_nick_value(trigger.nick, "inventory", user_inventory)
    bot.db.set_plugin_value("shop", cat_name.lower(), catalogue)
    user_money -= cost
    bank_rem(bot, trigger.nick, cost, "Shopping: " + item_name + ". Amount: " + str(amount))
    bot.say(format_add(item_name , amount), trigger.nick)

@plugin.commands("help shop")
def help_shop(bot , trigger):
    if not trigger.admin:
        bot.notice(USER_SHOP + "Help: https://webchat.duckie.chat/uploads/f6dc42892177bfa9/paste.txt   ")
    else:
        bot.notice(SHOP + "Admin Help: https://webchat.duckie.chat/uploads/ea39a05373c30f58/paste.txt   ")
