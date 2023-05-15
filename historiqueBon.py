from datetime import datetime
import discord
from discord.ext import commands

class Command:
    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.timestamp = datetime.now()
        self.previous = None
        self.next = None
# Cette classe Command est utilisée pour stocker des informations sur chaque commande que 
# notre bot reçoit. Elle contient un nom, l'ID de l'utilisateur qui a envoyé la commande, 
# la date et l'heure à laquelle la commande a été reçue, ainsi que des références aux 
# commandes précédentes et suivantes dans l'historique.
class CommandHistory:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self.locked = False
        self.locked_by = None
    #La classe CommandHistory représente l'historique des commandes reçues par notre bot. 
    #Elle maintient une liste chaînée de Command, ainsi que des informations sur l'état 
    #de l'historique, telles que la commande actuelle et si l'historique est verrouillé.

    def lock_history(self, user_id):
        if not self.locked:
            self.locked = True
            self.locked_by = user_id
            return True
        elif self.locked_by == user_id:
            return True
        else:
            return False
    #Cette méthode permet de verrouiller l'historique des commandes, ce qui empêche toute 
    # modification ultérieure de l'historique. Elle retourne True si l'historique est 
    # maintenant verrouillé, ou si l'utilisateur qui essaie de verrouiller l'historique 
    # est déjà celui qui l'a verrouillé.
    def unlock_history(self, user_id):
        if self.locked and self.locked_by == user_id:
            self.locked = False
            self.locked_by = None
            return True
        else:
            return False
    #Cette méthode permet de déverrouiller l'historique des commandes. Elle retourne 
    # True si l'historique a été déverrouillé avec succès, ou si l'utilisateur qui 
    # essaie de déverrouiller l'historique est celui qui l'a verrouillé.
    def add_command(self, name, user_id):
        if not self.locked:
            command = Command(name, user_id)
            if not self.head:
                self.head = command
                self.tail = command
                self.current = command
            else:
                command.previous = self.tail
                self.tail.next = command
                self.tail = command
    #Cette méthode ajoute une nouvelle commande à l'historique. Si l'historique est 
    # verrouillé, la commande n'est pas ajoutée. Sinon, elle crée une nouvelle instance 
    # de la classe Command avec le nom de la commande et l'ID de l'utilisateur, et 
    # l'ajoute à la fin de la liste chaînée.

    def get_last_command(self):
        if self.tail:
            return self.tail.name
        else:
            return None

    def get_user_commands(self, user_id):
        commands = []
        command = self.head
        while command:
            if command.user_id == user_id:
                commands.append(command.name)
            command = command.next
        return commands
    #La méthode get_user_commands prend en paramètre l'ID d'un utilisateur et renvoie 
    # une liste de toutes les commandes exécutées par cet utilisateur. Elle parcourt 
    # la liste chaînée en partant de la tête et en passant par chaque nœud jusqu'à la 
    # fin. Si l'ID de l'utilisateur correspond à celui de la commande en cours de 
    # traitement, elle ajoute le nom de cette commande à la liste.


    def move_forward(self):
        if self.current and self.current.next:
            self.current = self.current.next

    def move_back(self):
        if self.current and self.current.previous:
            self.current = self.current.previous

    def clear_history(self):
        self.head = None
        self.tail = None
        self.current = None


intents = discord.Intents.all()

client = commands.Bot(command_prefix="!", intents=intents)
history = CommandHistory()

@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user}")
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!"):
        # Ajouter la commande à l'historique
        history.add_command(message.content, message.author.id)
        
        if message.content == "!der":
            # Afficher la dernière commande
            last_command = history.get_last_command()
            await message.channel.send(f"Dernière commande : ```{last_command}```")
        elif message.content == "!mescommandes":
            # Afficher toutes les commandes de l'utilisateur
            user_commands = history.get_user_commands(message.author.id)
            await message.channel.send(f"Vos commandes : ```{user_commands}```")
        elif message.content == "!arriere":
            # Se déplacer en arrière dans l'historique
            history.move_back()
            current_command = history.current.name
            await message.channel.send(f"Commande actuelle : ```{current_command}```")
        elif message.content == "!avant":
            # Se déplacer en avant dans l'historique
            history.move_forward()
            current_command = history.current.name
            await message.channel.send(f"Commande actuelle : ```{current_command}```")
        elif message.content == "!effacer":
            # Effacer l'historique des commandes
            history.clear_history()
            await message.channel.send("Historique des commandes effacé.")
        else:
            await client.process_commands(message)
