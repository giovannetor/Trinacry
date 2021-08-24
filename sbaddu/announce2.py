from sopel import plugin
from sopel.formatting import CONTROL_COLOR , colors , CONTROL_BOLD , CONTROL_NORMAL

logs = "#trinacry-logs"
nono = ["#bot" , "#opscourse" , "#opers" , logs , "#minecraft"]
@plugin.commands("ann")
@plugin.require_admin
def ann(bot , trigger):
	chanlist = ""
	for channel in bot.channels:
		if channel not in nono:
			chanlist += str(channel) + " "
			bot.say(CONTROL_BOLD + CONTROL_COLOR + colors.RED + "[ANNOUNCE]:" + CONTROL_NORMAL + " %s " % trigger.group(2) , channel)
	bot.say(CONTROL_BOLD + CONTROL_COLOR + colors.RED + "[ANNOUNCE]:" + CONTROL_NORMAL +
			  " trasmesso in: " + chanlist , logs)
