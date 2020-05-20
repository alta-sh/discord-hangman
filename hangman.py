# A hangman bot for discord written by alta
import hangState
import discord
from discord.ext import commands

client = commands.Bot(command_prefix='hang!')
client.remove_command('help')

runningGames = []
commands = ["help", "play"]

# Checks if the user is in a game (if the author.id is in runningGames)
def isInGame(authorID):
    for game in runningGames:
        if (game["author"] == authorID):
            return True
    return False

# Deletes the authors dict in runningGames
def endGame(authorID):
    for game in runningGames:
        if (game["author"] == authorID):
            del runningGames[runningGames.index(game)]


@client.event
async def on_ready():
    print('Successfully logged in as {0.user}'.format(client))


@client.event
async def on_message(message):

    message.content = message.content.lower()

    # Check if the message sender is currently in a game:
    if (isInGame(message.author.id)):

        if (message.content != "hang!guess"):
            # check if they've sent a command
            if (message.content.startswith(client.command_prefix)):
                await message.channel.send(f"You can't use that command whilst in a game {message.author.name}...\n"+
                                            "If you would like to end the game type `end` 🤗")
                return

            # If they end the game
            if (message.content == "end"):
                await message.channel.send(f"Thanks for playing {message.author.mention}!\nGame successfully ended...")
                endGame(message.author.id)

            # If they enter a word without writing hang!guess first
            elif (len(message.content) > 1):
                await message.channel.send(f"{message.author.mention} please only enter 1 character at a time!\n"+
                                            "If you would like to guess the word use the command \n`hang!guess {your guess}`\n"+
                                            "Or if you would like to quit the game write `end`")

            else: # process the message as a character guess 
                await message.channel.send("You guessed a character...")

    await client.process_commands(message)


@client.command()
async def help(ctx):
    await ctx.send('here are the commands you can use:... ')

@client.command()
async def play(ctx):
    await ctx.send('Ok {0}, setting up the game now 👍'.format(ctx.message.author.mention))

    # Check if user isn't already in a game
    if(isInGame(ctx.message.author.id)):
        await ctx.send(f'Actually {ctx.message.author.name}, it looks like you\'re already in a game...' +
                        'type `end` to leave it.')
    else:
        # Add userID, guesses and a random word to runningGames
        randWord = ''
        runningGames.append({"author": ctx.message.author.id, "remainingGuesses": 0, "word": randWord})


# Reading the token
with open('token.txt', 'r') as file:
    client.run(file.readline())
