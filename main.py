#!/usr/bin/env python3

import discord
from rich import print
from pathlib import Path
from discord.ext import commands
from discord import app_commands

from settings import TOKEN


def main():
    # Create bot instance

    bot = commands.Bot(
        command_prefix = "$",
        intents = discord.Intents.all(),
        help_command = None,
    )

    # Load cogs when the bot is ready
    @bot.event
    async def on_ready():
        print(f'[green]Initialized as [/green][purple]{bot.user}[/purple]')
        await bot.change_presence(activity=discord.Game(name="/help"))

        for file in Path('src/cogs').glob('**/*.py'):
            *tree, _ = file.parts
            extension_name = f"{'.'.join(tree)}.{file.stem}"
            if extension_name not in bot.extensions:
                try:
                    await bot.load_extension(extension_name)
                    print(f"[green] Loaded extension:[/green] [yellow]{extension_name}[/yellow]")
                except Exception as e:
                    print(f"[red]Failed to load extension {extension_name}: {e}[/red]")

        await bot.tree.sync()

    bot.run(TOKEN)


if __name__ == "__main__":   
    print(f"[white]Token: [/white][red]{TOKEN}[/red]")
    main()