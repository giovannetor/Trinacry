from sopel import module 
from sopel.formatting import CONTROL_COLOR , colors , CONTROL_BOLD , CONTROL_NORMAL

@module.commands("ann")
@module.require_admin
def ann(bot , trigger):
	for channel in bot.channels:
		bot.say(CONTROL_BOLD + CONTROL_COLOR + colors.RED + "[ANNOUNCE]:" + CONTROL_NORMAL + " %s " % trigger.group(2) , channel)
	bot.reply("FATTO :)")
