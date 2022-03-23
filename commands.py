import discord
from discord.ext import commands
from discord_slash import SlashContext, SlashCommand, manage_commands

import config
import helper
import quotes

intents = discord.Intents.all()


def setupBotCommands(bot: commands.Bot):
    slash = SlashCommand(bot, sync_commands=True)
    butler = bot.get_cog("GameButler")

    # vgmg rules command
    @slash.slash(name="vgmg", description="Display VGMG rules", guild_ids=config.GUILD_IDS)
    async def vgmg(ctx):
        await ctx.send(quotes.vgmgRules)

    # list role command
    @slash.slash(name="listroles", description="List all game rolls", guild_ids=config.GUILD_IDS)
    async def listroles(ctx: SlashContext):
        roles = ["{0.name}".format(role) for role in ctx.guild.roles if helper.isGameRole(role)]
        await ctx.send(', '.join(roles))

    # Join role command
    @slash.slash(
        name="join",
        description="Join game role",
        options=[
            manage_commands.create_option(
                name="role",
                description="Name of game role",
                option_type=8,  # role
                required=True
            )
        ],
        guild_ids=config.GUILD_IDS
    )
    async def join(ctx: SlashContext, role: discord.Role):
        await helper.executeRoleCommand(
            ctx,
            role,
            lambda c, r: c.author.add_roles(r),
            "Role assigned",
            "This is not a valid game role"
        )

    # Leave role command
    @slash.slash(
        name="leave",
        description="Leave game role",
        options=[
            manage_commands.create_option(
                name="role",
                description="Name of game role",
                option_type=8,  # role
                required=True
            )
        ],
        guild_ids=config.GUILD_IDS
    )
    async def leave(ctx: SlashContext, role: discord.Role):
        await helper.executeRoleCommand(
            ctx,
            role,
            lambda c, r: c.author.remove_roles(r),
            "Role removed",
            "You do not have this role"
        )

    # Create role command
    @slash.slash(
        name="create",
        description="Create game role - Must have Manage role Permission",
        options=[
            manage_commands.create_option(
                name="role",
                description="Name of game role",
                option_type=3,  # string
                required=True
            )
        ],
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_roles=True)
    async def create(ctx: SlashContext, role: str):
        role = role.lower()
        try:
            if not ctx.author.guild_permissions.manage_roles:
                await ctx.send("You have insufficient permissions to modify roles")
            else:
                # check if role with same name already exists
                if any([role == r.name for r in ctx.guild.roles]):
                    await ctx.send(f"{role} already exists")

                newRole: discord.Role = await ctx.guild.create_role(name=role, colour=discord.Colour(config.HEXCOLOUR),
                                                                    mentionable=True)
                await ctx.send(f"{newRole.mention} role created")
                await helper.log(f"{ctx.author.mention} created {newRole.mention}")
        except:
            await ctx.send("An error occurred")
            await helper.log(f"An error occured when {ctx.author.mention} attempted to create a role called {role}")

    # Delete role command
    @slash.slash(
        name="delete",
        description="Delete game role - Must have Manage role Permission",
        options=[
            manage_commands.create_option(
                name="role",
                description="Name of game role",
                option_type=8,  # role
                required=True
            )
        ],
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_roles=True)
    async def delete(ctx: SlashContext, role: discord.Role):
        if ctx.author.guild_permissions.manage_roles:
            roleName = role.mention
            await helper.executeRoleCommand(
                ctx,
                role,
                lambda c, r: r.delete(reason=f"Deleted by {c.author}"),
                "Role deleted",
                "This is not a valid game role"
            )
            await helper.log(f"{ctx.author.mention} deleted {roleName}")
        else:
            await ctx.send("You have insufficient permissions")

    # list role member command
    @slash.slash(
        name="list",
        description="List all members in game role",
        options=[
            manage_commands.create_option(
                name="role",
                description="Name of game role",
                option_type=8,  # role
                required=True
            )
        ],
        guild_ids=config.GUILD_IDS
    )
    async def list(ctx: SlashContext, role: discord.Role):
        async def listMembersWithRole(c: SlashContext, r: discord.Role):
            members = [member.display_name for member in role.members]
            if len(members) == 0:
                await c.send(f"Nobody has the role {r.mention}")
            else:
                await c.send(f"Members with the {role.name} role: " + ', '.join(members))

        await helper.executeRoleCommand(
            ctx,
            role,
            lambda c, r: listMembersWithRole(c, r),
            "",
            f"Unknown error when attempting to list members with {role.name} role"
        )

    @slash.slash(
        name="anti_ad",
        description="Toggles Discord server invite removal",
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_messages=True)
    async def anti_ad(ctx: SlashContext):
        butler.antiAdverts = not butler.antiAdverts
        await helper.log(f"Anti Server Invites Toggled to: {butler.antiAdverts}")
        await ctx.send(f"Anti Server Invites Toggled to: {butler.antiAdverts}")

    @slash.slash(
        name="antispam",
        description="Toggles gif antispam",
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_messages=True)
    async def antispam(ctx: SlashContext):
        butler.antispam = not butler.antispam
        await helper.log(f"Anti Gifspam Toggled to: {butler.antispam}")
        await ctx.send(f"Anti Gifspam Toggled to: {butler.antispam}")

    @slash.slash(
        name="gifban",
        description="Toggles gif censorship",
        guild_ids=config.GUILD_IDS
    )
    @commands.has_permissions(manage_messages=True)
    async def gifban(ctx: SlashContext):
        butler.censor = not butler.censor
        if butler.antispam:
            butler.antispam = not butler.antispam
            await ctx.send("Gif antispam has been disabled")
        await helper.log(f"Gif censorship Toggled to: {butler.censor}")
        await ctx.send(f"Gif censorship Toggled to: {butler.censor}")
