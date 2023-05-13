import discord
from discord.ext import commands


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
#Définit une fonction asynchrone appelée on_ready qui est exécutée lorsque le bot est prêt à être utilisé.
async def on_ready():
    # Récupérer le premier serveur auquel le bot a accès
    guild = bot.guilds[0]
    
    # Récupérer le premier canal texte de ce serveur
    channel = guild.text_channels[0]
    
    # Vérifier si le bot a accès à ce canal
    if not channel.permissions_for(channel.guild.me).send_messages:

        print("Je n'ai pas la permission d'envoyer des messages dans ce canal.")
        return
    
    # Envoyer le message
    await channel.send("C'est reparti comme en 46 !")

#async def ban(ctx, user : discord.User, *reason): : 
#Définit une commande ban qui 
#bannit un utilisateur spécifié avec une raison optionnelle.
@bot.command()
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

#async def unban(ctx, user, *reason): : Définit une commande 
#unban qui révoque le bannissement d'un utilisateur spécifié 
#avec une raison optionnelle.
@bot.command()
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

#async def kick(ctx, user : discord.User, *reason): : Définit 
# une commande kick qui expulse un utilisateur spécifié avec 
# une raison optionnelle.
@bot.command()
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.send(f"{user} à été kick.")

#async def delete(ctx, amount=1500): : Définit une commande delete 
# qui supprime un certain nombre de messages dans le canal actuel.

@bot.command()
async def delete(ctx, amount=1500):
    await ctx.channel.purge(limit=amount)
    print('J efface poto')
    
# @bot.command()
# async def clear(ctx, nombre : int):
# 	messages = await ctx.channel.history(limit = nombre + 200).flatten()
# 	for message in messages:
# 		await message.delete()
