import discord

from Main.markov import Markov

client = discord.Client()

markov = Markov(10)


def generate_cmd(argv: [str]) -> str:
    if 2000 < int(argv[0]):
        return "Error: Can't generate Discord messages longer than 2000 characters"
    rtn: str = markov.generate(int(argv[0]))
    return rtn


functions = {
    "generate": generate_cmd
}


def msg_parser(msg: [str]) -> str:
    cmd: [str] = msg.split()
    if 1 < len(cmd):
        return functions.get(cmd[1])(cmd[2:])
    else:
        return "Invalid Syntax (@testbot command [arg1 arg2 ...])"


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if client.user != message.author:
        if client.user in message.mentions:
            await message.channel.send(msg_parser(message.content))
        else:
            msgs: [str] = message.content.split("\n")
            for m in msgs:
                markov.parse(m)


if __name__ == "__main__":
    try:
        f = open("token.txt", "r")
        client.run(f.read())
    except:
        print("Invalid Token")
        exit(1)
