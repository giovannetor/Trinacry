from sopel.formatting import colors, CONTROL_BOLD, CONTROL_COLOR, CONTROL_NORMAL
from sopel.plugin import commands, require_admin

CHAN_MAN = CONTROL_BOLD + CONTROL_COLOR + colors.WHITE + "," + colors.LIGHT_PURPLE + " CHAN MANAGEMENT " + CONTROL_NORMAL + " | "


def setup(bot):
    global log_channel
    log_channel = bot.db.get_plugin_value("chan_management", "log_chan", default="#trinacry-logs")


@commands("gamechan add")
@require_admin("Admin Only.")
def chan_add(bot, trigger):
    chan_db = bot.db.get_plugin_value("chan_management", "game_chans", default={})
    chanlist = []
    try:
        for chan in trigger.group(4).split(","):
            chanlist.append(chan)
    except:
        bot.reply("Syntax: .gamechan add <plugin> <#chan1,#chan2...>")
        return
    try:
        chan_db[trigger.group(3)].extend(chanlist)
    except:
        chan_db[trigger.group(3)] = chanlist
    bot.db.set_plugin_value("chan_management", "game_chans", chan_db)
    bot.say(f"{CHAN_MAN}Chans {chanlist} correctly added as Game Chans for {trigger.group(3)} by "
            f"{trigger.nick}.", log_channel
            )

@commands("gamechan del" , "gamechan rem")
@require_admin("Admin Only.")
def chan_del(bot, trigger):
    chan_db = bot.db.get_plugin_value("chan_management", "game_chans", default={})
    chanlist = []
    try:
        for chan in trigger.group(4).split(","):
            chanlist.append(chan)
    except:
        bot.reply("Syntax: .gamechan rem <plugin> <#chan1,#chan2...>")
        return
    try:
        chan_db[trigger.group(3)].remove(chanlist)
    except:
        bot.reply(f"{CHAN_MAN} Error while removing the chans {chanlist}")
        return
    bot.db.set_plugin_value("chan_management", "game_chans", chan_db)
    bot.say(f"{CHAN_MAN}Chans {chanlist} correctly removed as Game Chans for {trigger.group(3)} by "
            f"{trigger.nick}.", log_channel
            )

@commands("logchan set")
@require_admin("Admin Only.")
def chan_add(bot, trigger):
    try:
        log_chan = trigger.group(3)
    except:
        bot.reply("Syntax: .logchan set <#chan>")
        return
    if "#" not in log_chan:
        bot.reply("Syntax: .logchan set <#chan>")
        return
    bot.db.set_plugin_value("chan_management", "log_chan", log_chan)
    bot.say(f"{CHAN_MAN}Chan {log_chan} correctly set as Log Chan by {trigger.nick}.", log_channel)

@commands("logchan")
@require_admin("Admin Only.")
def show_log_chan(bot , trigger):
    bot.say(f"{CHAN_MAN}The Log Chan is {log_channel}")

@commands("gamechans")
@require_admin("Admin Only.")
def show_game_chan(bot , trigger):
    game_chans = bot.db.get_plugin_value("chan_management", "game_chans", default={"None" : "None"})
    ret = ""
    for plugin , value in game_chans:
        ret += str(plugin) + ": " + str(value) + " || "
    bot.say(f"{CHAN_MAN}The Game Chans are {ret}")

@commands("logtest")
def logtest(bot , trigger):
    bot.say(f"{CHAN_MAN} LOG TEST" , log_channel)