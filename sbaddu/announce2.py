from sopel import plugin
from sopel.formatting import CONTROL_COLOR , colors , CONTROL_BOLD , CONTROL_NORMAL

logs = "#trinacry-logs"
nono = ["#bot" , "#opscourse" , "#opers" , logs , "#minecraft"]

@plugin.commands("ann chan")
@plugin.require_admin("Sorry, admin only")
def ann(bot , trigger):
	chanlist = ""
	for channel in bot.channels:
		if channel not in nono:
			chanlist += str(channel) + " "
			bot.say(CONTROL_BOLD + CONTROL_COLOR + colors.RED + "[ANNOUNCE]:" + CONTROL_NORMAL + " %s " % trigger.group(2) , channel)
	bot.say(CONTROL_BOLD + CONTROL_COLOR + colors.RED + "[ANNOUNCE]:" + CONTROL_NORMAL +
			  " trasmesso in: " + chanlist , logs)

@plugin.commands("ann pm")
@plugin.require_admin("Sorry, admin only")
def ann_pm(bot , trigger):
	testo = trigger.group(2)
	lista = ""
	lista_nono = ["ChanServ" , "DuckieBot" , "TestUserZNC" , "MatrixBridge" , "Trinacry" , "T-Dev"]
	for user in bot.users:
		if user[0] in "-+&~@%":
			user = user[1:]
		if user not in lista.split(", ") and user not in lista_nono:
			lista += user + ", "
		bot.notice(CONTROL_BOLD + CONTROL_COLOR + colors.RED + "[ANNOUNCE]:" + CONTROL_NORMAL + " %s "
				% testo , user)
	bot.say(CONTROL_BOLD + CONTROL_COLOR + colors.RED + "[ANNOUNCE]:" + CONTROL_NORMAL +
			  " trasmesso a: " + lista.rstrip(", ") , logs)


@plugin.commands("help ann")
@plugin.require_admin("Sorry, admin only")
def ann_wrong(bot , trigger):
	bot.say("use '.ann chan' to send the announce to channels.")
	bot.say("use '.ann pm' to send the announce to pms.")
