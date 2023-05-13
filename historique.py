import discord
from discord.ext import commands

# Définir une liste chaînée pour stocker l'historique des commandes
class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None
        
class History:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        
    def add_command(self, command):
        new_node = Node(command)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
            self.current = new_node
    
    def get_last_command(self):
        if not self.current:
            return None
        return self.current.value
    
    def get_user_commands(self, user_id):
        user_commands = []
        current_node = self.head
        while current_node:
            if current_node.value.author.id == user_id:
                user_commands.append(current_node.value)
            current_node = current_node.next
        return user_commands
    
    def move_forward(self):
        if self.current and self.current.next:
            self.current = self.current.next
    
    def move_back(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
    
    def clear_history(self):
        self.head = None
        self.tail = None
        self.current = None

# Créer un bot Discord
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Créer une instance de l'historique
history = History()

# Commande pour ajouter une commande à l'historique
@bot.command()
async def add(ctx):
    history.add_command(ctx)

# Commande pour afficher la dernière commande rentrée
@bot.command(name="der")
async def last(ctx):
    last_command = history.get_last_command()
    if last_command:
        await ctx.send(f"La dernière commande rentrée est: {last_command.content}")
    else:
        await ctx.send("L'historique est vide.")

# Commande pour afficher toutes les commandes d'un utilisateur
@bot.command(name='history')
async def user_history(ctx):
    """Affiche l'historique des commandes de l'utilisateur"""
    user_id = str(ctx.author.id)
    user_history = history.get_user_commands(user_id)
    if user_history:
        user_history_string = "Historique des commandes de l'utilisateur :\n"
        user_history_string += "\n".join([cmd.content for cmd in user_history])
        await ctx.send(user_history_string)
    else:
        await ctx.send("Vous n'avez pas encore utilisé de commande.")

# Commande pour se déplacer dans l'historique en avant
@bot.command(name="devant")
async def forward(ctx):
    history.move_forward()

# Commande pour se déplacer dans l'historique en arrière
@bot.command(name="back")
async def back(ctx):
    history.move_back()

# Commande pour vider l'historique
@bot.command(name="efface")
async def clear(ctx):
    history.clear_history()
    await ctx.send("L'historique a été vidé.")

