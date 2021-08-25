from sopel.plugin import  commands,  example , require_admin
from sopel.formatting import CONTROL_COLOR , colors , CONTROL_BOLD , CONTROL_NORMAL, CONTROL_ITALIC

log = "#trinacry-logs"

BANK =  CONTROL_COLOR + colors.ORANGE + "," + colors.BLACK + " ₸ BANK ₸ " + CONTROL_NORMAL + " | "

def money_getter(bot , nick):
    money = bot.db.get_nick_value(nick , "coins")
    if not money:
        bot.db.set_nick_value(nick , "coins" , 0)
        return 0
    else:
        return money

def bank_add(bot , nick : str,  value_to_add : int ,reason :str = "No reason given."):
    money = money_getter(bot , nick)
    money += value_to_add
    bot.db.set_nick_value(nick , "coins" , money)
    bot.say(format_add(value_to_add , reason) , nick)
    bot.say(BANK + nick + " obtained " + str(value_to_add) + coins() + ". Reason: " + reason , log)

def bank_rem(bot , nick :str,  value_to_rem : int ,reason : str = "No reason given."):
    money = money_getter(bot , nick)
    money -= value_to_rem
    bot.db.set_nick_value(nick , "coins" , money)
    bot.say(format_rem(value_to_rem , reason) , nick)
    bot.say(BANK + nick + " lost " + str(value_to_rem) + coins() + ". Reason: " + reason , log)

def coins():
    coins_format = CONTROL_BOLD + CONTROL_COLOR +colors.ORANGE + " TriCoins (₸) " + CONTROL_NORMAL
    return coins_format

def format_add(money , reason):
    add = BANK + CONTROL_BOLD + "[" + CONTROL_COLOR + colors.LIGHT_GREEN + "+" + CONTROL_NORMAL + CONTROL_BOLD + "]" + CONTROL_NORMAL + \
           " ADDED " + str(money) + coins() + " to your Bank Account. Reason: " + CONTROL_ITALIC + reason
    return add

def format_rem(money , reason):
    rem = BANK + CONTROL_BOLD + "[" + CONTROL_COLOR + colors.LIGHT_RED + "-" + CONTROL_NORMAL + CONTROL_BOLD + "]" + CONTROL_NORMAL + \
           " REMOVED " + str(money) + coins() + " from your Bank Account. Reason: " + CONTROL_ITALIC + reason
    return rem

@commands("bank" , "ba")
def bank(bot , trigger):
    if not trigger.group(3):
        money = money_getter(bot , trigger.nick)
        bot.say(BANK + trigger.nick + " you have " + str(money) + coins() + " in your Bank Account.")
    else:
        if trigger.group(3) != "*":
            if trigger.group(3) == "Trinacry" or trigger.group(3) == "trinacry":
                bot.reply("Darling, I'm the Bank. I own all of your" + coins() + "MUAHAHA!!")
                return

            gender = bot.db.get_nick_value(trigger.group(3) , "pronouns")

            if not gender:
                gender_def = "their"
            else:
                gender_def = gender.split("/")[2]

            money = money_getter(bot , trigger.group(3))
            bot.say(BANK + trigger.group(3) + " has " + str(money) + coins() + "in " + gender_def + " Bank Account.")



@commands("pay")
@example(".pay gio 50")
def pay(bot , trigger):
    if not trigger.group(3) or not trigger.group(4):
        bot.reply(BANK + CONTROL_BOLD + CONTROL_COLOR + colors.RED + "FORMAT:" + CONTROL_NORMAL + " .pay <nick> < ₸ >")
        return

    money_1 = money_getter(bot , trigger.nick)
    money_2 = money_getter(bot , trigger.group(3))
    try:
        to_give = int(trigger.group(4))
    except:
        bot.reply(BANK + CONTROL_BOLD + CONTROL_COLOR + colors.RED + "FORMAT:" + CONTROL_NORMAL + " .pay <nick> < ₸ >")
        return

    if to_give > money_1:
        bot.say(BANK + trigger.nick + " you don't have enough" + coins() + "to pay.")
        return

    money_1 -= to_give
    money_2 += to_give

    bot.db.set_nick_value(trigger.nick , "coins" , money_1)
    bot.db.set_nick_value(trigger.group(3) , "coins" , money_2)
    bot.say(BANK + "Succesfully paid " + str(money_2) + coins() + "to " + trigger.group(3))

    bot.say(format_rem(to_give , "Payment to " + trigger.group(3)) , trigger.nick)
    bot.say(format_add(to_give , "Payment from " + trigger.nick) , trigger.group(3))

@commands("give")
@require_admin("I'm sorry, but only admins can give TriCoins.")
@example(".give gio 50")
def give(bot , trigger):

    money = money_getter(bot , trigger.group(3))
    money += int(trigger.group(4))

    bot.db.set_nick_value(trigger.group(3) , "coins" , money)

    bot.notice(BANK + trigger.nick + ": correctly added " + str(trigger.group(4)) + coins() + "to "  +
              trigger.group(3) + "'s Bank Account." , trigger.nick)
    bot.say(BANK + trigger.nick + " gave " + str(trigger.group(4)) + coins() + "to " + trigger.group(3) + " succesfully." , log)
    bot.say(format_add(trigger.group(4) , "TriCoins given by an Admin.") ,trigger.group(3))

@commands("take")
@require_admin("I'm sorry, but only admins can take TriCoins.")
@example(".take gio 50")
def take(bot , trigger):

    money = money_getter(bot , trigger.group(3))
    if trigger.group(4) == "*":
        money = 0
    else:
        money -= int(trigger.group(4))
    if money < 0:
        money = 0

    bot.db.set_nick_value(trigger.group(3) , "coins" , money)

    bot.notice(BANK + trigger.nick + ": correctly removed " + str(trigger.group(4)) + coins() +
              "from "  + trigger.group(3) + "'s Bank Account." , trigger.nick)
    bot.say(BANK + trigger.nick + " took " + str(trigger.group(4)) + coins() + "from " + trigger.group(3) + " succesfully." , log)
    bot.say(format_rem(trigger.group(4) , "TriCoins taken by an Admin.") ,trigger.group(3))

@commands("transfer")
@example(".transfer gio giovannetor" , ".transfer gio(3) gio2(4) 50(5)")
@require_admin("Only admins can transfer TriCoins.")
def transfer(bot , trigger):

    money_available = money_getter(bot , trigger.group(3))
    money_to = money_getter(bot , trigger.group(4))

    if not trigger.group(5) or trigger.group(5) == "*":
        money_from = money_available
        money_tot = money_from + money_to

        bot.db.set_nick_value(trigger.group(3) , "coins" , None)
        bot.db.set_nick_value(trigger.group(4) , "coins" , money_tot)

        bot.say(format_rem(money_from , "Transfer to " + trigger.group(4)) ,trigger.group(3))
        bot.say(format_add(money_from , "Transfer from " + trigger.group(3)) ,trigger.group(4))
        bot.say(BANK + trigger.nick + " transferred " + str(money_from) + coins() + "from " + trigger.group(3) + " to "
                + trigger.group(4) + " succesfully." , log)

    else:
        money_from = int(trigger.group(5))
        if money_from > money_available:
            bot.reply("you don't have this many TriCoins.")
            return
        money_left = money_available - money_from
        money_tot = money_from + money_to

        bot.db.set_nick_value(trigger.group(3) , "coins" , money_left)
        bot.db.set_nick_value(trigger.group(4) , "coins" , money_tot)

        bot.say(format_rem(money_from , "Transfer to " + trigger.group(4)) ,trigger.group(3))
        bot.say(format_add(money_from , "Transfer from " + trigger.group(3)) ,trigger.group(4))
        bot.say(BANK + trigger.nick + " transferred " + str(money_from) + coins() + "from " + trigger.group(3) + " to "
                + trigger.group(4) + " succesfully." , log)

@commands("help bank")
def help_bank(bot , trigger):
    bot.notice(BANK + "HELP: https://webchat.duckie.chat/uploads/119b6835c6ded361/paste.txt "  , trigger.nick)
