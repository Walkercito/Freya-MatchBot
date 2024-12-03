import os
import discord
from discord.ext import commands
from discord import app_commands, ui

from settings import COG_DIR


class CommandSelect(ui.Select):
    def __init__(self, commands_dict):
        options = []
        for cmd_name, cmd_info in commands_dict.items():
            options.append(discord.SelectOption(
                label = cmd_name,
                description = cmd_info['brief_desc'][:100]
            ))
        
        super().__init__(
            placeholder = "🔍 Choose a command",
            options = options[:25],  # limit of 25 options
            min_values = 1,
            max_values = 1
        )
        self.commands_dict = commands_dict

    
    async def callback(self, interaction: discord.Interaction):
        cmd_name = self.values[0]
        cmd_info = self.commands_dict[cmd_name]
        
        embed = discord.Embed(
            title = f"📝 Command: /{cmd_name}",
            description = cmd_info['description'],
            color = discord.Color.pink()
        )
        
        if cmd_info['parameters']:
            embed.add_field(name = "⚙️ Parameters", value = cmd_info['parameters'], inline = False)
        
        await interaction.response.edit_message(embed = embed, view = CommandView(self.commands_dict))


class CommandView(ui.View):
    def __init__(self, commands_dict):
        super().__init__()
        self.add_item(CommandSelect(commands_dict))
        self.help_cog = None
        
    
    @ui.button(label = "↩️ Return to menu", style = discord.ButtonStyle.secondary)
    async def show_overview(self, interaction: discord.Interaction, button: ui.Button):
        if not self.help_cog:
            self.help_cog = interaction.client.get_cog('HelpCommand')
        embed = self.help_cog.create_overview_embed()
        
        await interaction.response.edit_message(embed = embed, view = self)


class HelpCommand(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        
    
    def get_commands_dict(self):
        commands_dict = {}
        
        for cog_name, cog in self.bot.cogs.items():
            for cmd in cog.walk_app_commands():
                parameters = ""
                if hasattr(cmd, 'parameters'):
                    parameters = "\n".join([f"📌 {param.name}: {param.description}" for param in cmd.parameters])
                
                commands_dict[cmd.name] = {
                    'description': cmd.description or "No description available",
                    'brief_desc': cmd.description[:50] + "..." if cmd.description and len(cmd.description) > 50 else cmd.description or "No description",
                    'parameters': parameters,
                    'cog_name': cog_name
                }
        
        return commands_dict
    

    def create_overview_embed(self):
        embed = discord.Embed(
            title = "<:serverdiscovery:1313354019464282134> Available Commands",
            description = " > Find your perfect match! Select a command below to discover all the dating features available.",
            color = discord.Color.pink()
        )
        
        for cog_name, cog in self.bot.cogs.items():
            commands_list = []
            for cmd in cog.walk_app_commands():
                desc = cmd.description[:30] + "..." if cmd.description and len(cmd.description) > 30 else cmd.description or "No description"
                commands_list.append(f"💫 /{cmd.name} - {desc}")
            
            if commands_list:
                embed.add_field(
                    name = f"🔹 {cog_name}",
                    value = "\n".join(commands_list),
                    inline = False
                )
        
        return embed
    
   
    @app_commands.command(name = "help", description = "Shows all available dating commands")
    async def help_command(self, interaction: discord.Interaction):
        commands_dict = self.get_commands_dict()
        embed = self.create_overview_embed()
        
        await interaction.response.send_message(embed = embed, view = CommandView(commands_dict))


async def setup(bot) -> None:
    await bot.add_cog(HelpCommand(bot))