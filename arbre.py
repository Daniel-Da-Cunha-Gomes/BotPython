import asyncio
import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
#class Question: : Définit une classe Question pour 
#représenter une question dans l'arbre de questions et réponses.
class Question:
    def __init__(self, text, yes=None, no=None):
        self.text = text
        self.yes = yes
        self.no = no

#async def ask(self, ctx, user_id): : Définit 
# une méthode asynchrone ask pour poser une question 
# à un utilisateur via Discord.
    async def ask(self, ctx, user_id):
        #reactions = ['👍', '👎'] : Définit les réactions possibles 
        # pour la question (pouce levé et pouce baissé).
        message = await ctx.send(self.text)
        reactions = ['👍', '👎']
        #for reaction in reactions: : Ajoute les réactions à un 
        # message pour permettre à l'utilisateur de répondre à la question.
        for reaction in reactions:
            await message.add_reaction(reaction)
        #def check(reaction, user): : Définit une fonction de vérification 
        # pour wait_for afin de s'assurer que la réaction provient de l'utilisateur correct.
        def check(reaction, user):
            return user.id == user_id and reaction.message == message and str(reaction.emoji) in reactions
        #reaction, user = await bot.wait_for('reaction_add', timeout=60.0, 
        # check=check) : Attend que l'utilisateur réagisse au message pendant 
        # 60 secondes et récupère la réaction et l'utilisateur.
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Désolé, la réponse a expiré.")
            return None
        #if str(reaction.emoji) == reactions[0]: : 
        # Vérifie si l'utilisateur a réagi avec le pouce levé.
        if str(reaction.emoji) == reactions[0]:
            if self.yes is not None:
                return await self.yes.ask(ctx, user_id)
            else:
                return self.text + " - Réponse positive"
        else:
            if self.no is not None:
                return await self.no.ask(ctx, user_id)
            else:
                return self.text + " - Réponse négative"

# L'arbre de questions, avec une question racine et des sous-questions
root_question = Question("Bonjour ! Avez-vous besoin d'aide en Frontend?",
                         yes=Question("Tu as besoins de cour en HTML CSS?",
                                      yes=Question("cour HTML = :thumbsup: cour CSS = :thumbsdown: ",
                                                    yes=Question("https://www.youtube.com/watch?v=qsbkZ7gIKnc"),
                                                   no=Question("https://www.youtube.com/watch?v=iSWjmVcfQGg")),
                                      no=Question("Tu veux pousser tes compétance en frontend?",
                                                  yes=Question("TKT c est pas long https://www.youtube.com/watch?v=oCINeytlyRA"),
                                                  no=Question("bah bouge de la poto"))),
                         no="Très bien, n'hésitez pas à revenir si vous avez besoin d'aide en frontend !")


conversation_history = {}
#async def test(ctx): : Définit une commande test qui 
# commence la conversation avec l'utilisateur en posant 
# la question racine.
@bot.command()
async def test(ctx):
    user_id = ctx.author.id
    if user_id not in conversation_history:
        conversation_history[user_id] = []
    await root_question.ask(ctx, user_id)
    conversation_history[user_id].append(root_question)
#async def reset(ctx): : Définit une commande 
# reset pour réinitialiser l'historique de conversation 
# de l'utilisateur
@bot.command()
async def reset(ctx):
    user_id = ctx.author.id
    if user_id in conversation_history:
        del conversation_history[user_id]
    await ctx.send("Discution réinitialisée.")

# Définit une commande speak qui vérifie si le sujet est traité dans l'arbre de questions.
@bot.command()
async def speak(ctx, subject):
    # Vérifier si le sujet est traité dans l'arbre de questions
    def is_subject_in_question(question):
        if subject.lower() in question.text.lower():
            return True
        if question.yes is not None and is_subject_in_question(question.yes):
            return True
        if question.no is not None and is_subject_in_question(question.no):
            return True
        return False
    
    if is_subject_in_question(root_question):
        await ctx.send("Oui, je parle de {}".format(subject))
    else:
        await ctx.send("Non, je ne parle pas de {}".format(subject))



