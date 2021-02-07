import requests
import json

import os
import datetime

import database as db
import discord_utils as disc


LOG_FILE = "db/log"


def get_content(file):
    # Read file content
    try:
        file = open(file, "r")
        s = file.read()
        file.close()
    except Exception as error:
        log("get_content", error, f"error reading file {file}")
        return ""

    return s


def log(fctname, error, message):
    """
    Pretty printer for logs
    """

    now = datetime.datetime.now()
    log = f"[{now}]: " + \
        str(error) + '\n' + ('+' * 4) + (' ' * 4) + \
        fctname + (" " * (20-len(fctname))) + \
        ': ' + message + '\n'

    print(log)

    f = open(LOG_FILE, "a+")

    f.write(log)
    f.close()


def check_member(message):
    if not db.member_exist(message.author.id, message.guild.id):
        log("check_member", "Adding member",
            f"Added member {message.author.id} with guild {message.guild.id}")
        db.member_add(message.author.id, message.guild.id)


async def add(self, message, args):
    if len(args) != 1:
        return await disc.error_message(message, title="Wrong usage",
                                        desc="The `add` function takes only `1` parameter, the Maiar wallet ID")

    # TODO: Need to check if wallet is valid.
    sql = """UPDATE members SET wallet = ? WHERE id = ? AND id_discord = ?"""
    args = [args[0], message.author.id, message.guild.id]
    db.exec(sql, args)


async def delete(self, message, args):
    sql = """UPDATE members SET wallet = ? WHERE id = ? AND id_discord = ?"""
    args = ["", message.author.id, message.guild.id]
    db.exec(sql, args)


if not os.path.exists("db"):
    os.mkdir("db")
    f = open(LOG_FILE, "w")
    f.close()

    # After because we need the folder
    log("DB folder", "DB folder did not exist", "Creating DB folder")
