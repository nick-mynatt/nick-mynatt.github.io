import discord
import os
import re
from random import randint
from keep_alive import keep_alive

client = discord.Client()

cypherMode = True


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Command: .roll
    # Find any message in format '.roll d??..?' where ? are numbers
    if message.content.startswith('.roll') or message.content.startswith('.r'):
        dice_pattern = '[d][0-9]+'
        match = re.search(dice_pattern, message.content)
        if match:
            dice = match.group(0)
            roll = diceRoll(dice)
            await message.channel.send(roll)

    # Command: .cypherMode
    # Toggles Cypher Mode. Changes other functions.
    if message.content.startswith('.cypher'):
        toggleCypher()
        await message.channel.send('Cypher mode: {}'.format(cypherMode))


# Takes a format d??..? (where ? are numbers) and converts to a random int in range 1..?
def diceRoll(dice):
    msg = "Error"
    if dice.startswith('d') or dice.startswith('D'):
        num = int(dice[1:])  # casting str to int
        if num > 0:
            roll = randint(1, num)
            msg = roll

            # Special Cypher text
            if cypherMode:
                if roll == 17:
                    msg = '17 - +1 dmg'
                elif roll == 18:
                    msg = '18 - +2 dmg'
                elif roll == 19:
                    msg = '19 - +3 dmg or minor effect'
                elif roll == 20:
                    msg = '20 - +4 dmg or MAJOR effect'

            # Special d20 text
            elif num == 20:
                if roll == 1:
                    msg = '1 - **FAIL**'
                elif roll == 20:
                    msg = '20 - **CRIT**'

    return msg


def toggleCypher():
    global cypherMode
    cypherMode = not cypherMode


keep_alive()
client.run(os.getenv('TOKEN'))
