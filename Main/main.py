import pickle
import discord

from Main.markov import Markov

client = discord.Client()
markov = None


def is_model(argv):
    return markov is not None


def new_markov(argv):
    global markov
    if len(argv) != 3:
        return "Error: Invalid number of arguments"
    try:
        if markov is None:
            markov = Markov(argv[0], argv[1], int(argv[2]))
            return "Success: Model created"
    except:
        pass
    return "Error: Can't make model"


def open_markov(argv):
    global markov
    if len(argv) != 1:
        return "Error: Invalid number of arguments"
    try:
        if markov is None:
            markov = pickle.load(open(argv[0], "rb"))
            return "Success: Model opened"
    except:
        return "Error: Can't open model"


def close_markov(argv):
    global markov
    if 0 != len(argv):
        return "Error: Invalid number of arguments"
    elif markov is None:
        return "Error: No model is open"
    markov = None
    return "Success: Model was closed"


def generate_cmd(argv):
    if len(argv) != 1:
        return "Error: Invalid number of arguments"
    if markov is None:
        return "Error: No model is open"
    if markov.t == "letters":
        return ("".join(markov.generate(int(argv[0]))))[:2000]
    elif markov.t == "words":
        return (" ".join(markov.generate(int(argv[0]))))[:2000]
    else:
        return "Error: Can't display output sequence (can't display this kind with text)"


def save_cmd(argv):
    if len(argv) != 0:
        return "Error: Invalid number of arguments"
    try:
        markov.save()
        return "Success: Model saved"
    except:
        return "Error: Can't save model "

def file_cmd(argv):
    if len(argv) == 1:
        try:
            markov.parse_file(argv[0])
            return "Success: Parsed file"
        except:
            return "Error: Can't parse file"
    elif len(argv) == 2:
        try:
            markov.parse_n_file(argv[0], int(argv[1]))
            return "Success: Parsed file"
        except:
            return "Error: Can't parse file"
    return "Error: Invalid number of arguments"


functions = {
    "is_model": is_model,
    "new": new_markov,
    "open": open_markov,
    "close": close_markov,
    "generate": generate_cmd,
    "save": save_cmd,
    "file": file_cmd
}


def msg_parser(msg):
    cmd = msg.split()
    if 1 < len(cmd) and cmd[1] in functions:
        return functions.get(cmd[1])(cmd[2:])
    else:
        return "Invalid Syntax (@" + client.user.display_name + " command [arg1 arg2 ...])"


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if client.user != message.author:
        if client.user in message.mentions:
            await message.channel.send(msg_parser(message.content))
        elif markov is not None:
            formated_msg = message.content.strip()
            if formated_msg[-1] != "." and formated_msg[-1] != "!" and formated_msg[-1] != "?":
                formated_msg += ". "
            else:
                formated_msg += " "
            if markov.t == "letters":
                markov.parse(formated_msg)
            elif markov.t == "words":
                markov.parse(tuple(formated_msg.split(" ")))



if __name__ == "__main__":
    try:
        f = open("token.txt", "r")
        client.run(f.read())
    except:
        print("Invalid Token")
        exit(1)
