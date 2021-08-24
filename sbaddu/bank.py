from sopel.plugin import  commands,  example , require_admin
from sopel.formatting import CONTROL_COLOR , colors , CONTROL_BOLD , CONTROL_NORMAL, CONTROL_ITALIC


def money_getter(bot , nick):
    money = bot.db.get_nick_value(nick , "denari")
    if not money:
        bot.db.set_nick_value(nick , "denari" , 0)
        return 0
    else:
        return money

def denari():
    denari_format = CONTROL_BOLD + CONTROL_COLOR +colors.ORANGE + " Denari (₪) " + CONTROL_NORMAL
    return denari_format

def format_add(money):
    add = CONTROL_BOLD + "[" + CONTROL_COLOR + colors.LIGHT_GREEN + "+" + CONTROL_NORMAL + CONTROL_BOLD + "]" + CONTROL_NORMAL + \
           " ADDED " + str(money) + denari() + " to your Bank."
    return add

def format_rem(money):
    rem = CONTROL_BOLD + "[" + CONTROL_COLOR + colors.LIGHT_RED + "-" + CONTROL_NORMAL + CONTROL_BOLD + "]" + CONTROL_NORMAL + \
           " REMOVED " + str(money) + denari() + " from your Bank."
    return rem

@commands("bank" , "ba")
@example(".bank" , ".bank gio")
def bank(bot , trigger):
    if not trigger.group(3):
        money = money_getter(bot , trigger.nick)
        bot.reply(" you have " + str(money) + denari() + " in your Bank.")
    else:
        if trigger.group(3) == "Trinacry" or trigger.group(3) == "trinacry":
            bot.reply("Darling, I'm the Bank. I own all of your" + denari() + "MUAHAHA!!")
            return

        gender = bot.db.get_nick_value(trigger.group(3) , "pronouns")

        if not gender:
            gender_def = "their"
        else:
            gender_def = gender.split("/")[2]

        money = money_getter(bot , trigger.group(3))
        bot.reply(" "+ trigger.group(3) + " has " + str(money) + denari() + "in " + gender_def + " Bank.")

@commands("pay")
@example(".pay gio 50")
def pay(bot , trigger):
    if not trigger.group(3) or not trigger.group(4):
        bot.reply(CONTROL_BOLD + CONTROL_COLOR + colors.RED + "FORMAT:" + CONTROL_NORMAL + " .pay <nick> <denari>")
        return

    money_1 = money_getter(bot , trigger.nick)
    money_2 = money_getter(bot , trigger.group(3))
    try:
        to_give = int(trigger.group(4))
    except:
        bot.reply(CONTROL_BOLD + CONTROL_COLOR + colors.RED + "FORMAT:" + CONTROL_NORMAL + " .pay <nick> <denari>")
        return

    if to_give > money_1:
        bot.reply(" you don't have enough" + denari() + "to pay.")
        return

    money_1 -= to_give
    money_2 += to_give

    bot.db.set_nick_value(trigger.nick , "denari" , money_1)
    bot.db.set_nick_value(trigger.group(3) , "denari" , money_2)
    bot.say("Succesfully paid " + str(money_2) + denari() + "to " + trigger.group(3))

    bot.say(format_rem(to_give) , trigger.nick)
    bot.say(format_add(to_give) , trigger.group(3))

@commands("give")
@require_admin("I'm sorry, but only admins can give money.")
@example(".give gio 50")
def give(bot , trigger):

    money = money_getter(bot , trigger.group(3))
    money += int(trigger.group(4))

    bot.db.set_nick_value(trigger.group(3) , "denari" , money)

    bot.reply(" correctly added " + str(trigger.group(4)) + denari() + "to "  + trigger.group(3) + "'s Bank.")

    bot.say(format_add(trigger.group(4)) ,trigger.group(3))

@commands("take")
@require_admin("I'm sorry, but only admins can take money.")
@example(".take gio 50")
def take(bot , trigger):

    money = money_getter(bot , trigger.group(3))
    money -= int(trigger.group(4))
    if money < 0:
        money = 0

    bot.db.set_nick_value(trigger.group(3) , "denari" , money)

    bot.reply(" correctly removed " + str(trigger.group(4)) + denari() + "from "  + trigger.group(3) + "'s Bank.")

    bot.say(format_rem(trigger.group(4)) ,trigger.group(3))
