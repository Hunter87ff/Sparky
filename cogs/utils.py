import discord
from discord.ext import commands
cmd = commands

class Utility(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.counter = 0


	@cmd.command()
	async def ava(ctx, user:discord.Member = None):
		if user == None:
			user = ctx.author
			return await ctx.send(user.avatar_url)

		else:
			return await ctx.send("Something went wrong")




	

















def setup(bot):
	bot.add_cog(Utility(bot))