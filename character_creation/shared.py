import discord
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

CAREER_EMOJIS = {
    "Colonial Marine": "🔫",
    "Colonial Marshal": "⭐",
    "Company Agent": "💼",
    "Medic": "💉",
    "Pilot": "✈️",
    "Roughneck": "🛠️",
    "Kid": "🧸",
    "Officer": "🎖️",
    "Wildcatter": "⛏️",
    "Scientist": "🧪",
    "Entertainer": "🎤"
}

async def update_user_roles_and_nickname(user: discord.User, character, guild: discord.Guild) -> Tuple[bool, str]:
    """Update a user's roles and nickname based on their character."""
    try:
        member = guild.get_member(user.id)
        if not member:
            return False, f"User {user.name} not found in guild {guild.name}"

        # Get the career role with emoji
        emoji = CAREER_EMOJIS.get(character.career, "👤")
        role_name = f"{emoji} {character.career}"
        career_role = discord.utils.get(guild.roles, name=role_name)
        
        if not career_role:
            # Try to create the role if it doesn't exist
            try:
                career_role = await guild.create_role(
                    name=role_name,
                    reason=f"Career role for {character.name}",
                    hoist=True,
                    mentionable=False
                )
                logger.debug(f"Created role: {role_name}")
            except discord.Forbidden:
                return False, f"Bot lacks permission to create role {role_name}"
            except discord.HTTPException as e:
                return False, f"Failed to create role {role_name}: {str(e)}"

        # Remove all career roles first
        success, message = await remove_character_roles(user, guild)
        if not success:
            return False, f"Failed to remove existing roles: {message}"

        # Add the new career role
        try:
            await member.add_roles(career_role)
            logger.debug(f"Added role {career_role.name} to user {user.name}")
        except discord.Forbidden:
            return False, f"Bot lacks permission to add role {career_role.name}"
        except discord.HTTPException as e:
            return False, f"Failed to add role {career_role.name}: {str(e)}"

        # Update nickname if user is not the server owner
        if member.id != guild.owner_id:
            try:
                # Set nickname to just the emoji and character name
                new_nickname = f"{emoji} {character.name}"
                # If that's too long, truncate the character name
                if len(new_nickname) > 32:
                    max_name_length = 32 - len(emoji) - 2  # -2 for the space and emoji
                    new_nickname = f"{emoji} {character.name[:max_name_length]}"
                
                await member.edit(nick=new_nickname)
                logger.debug(f"Updated nickname to {new_nickname} for user {user.name}")
            except discord.Forbidden:
                return False, f"Bot lacks permission to update nickname for {user.name}"
            except discord.HTTPException as e:
                return False, f"Failed to update nickname: {str(e)}"
            return True, f"Updated roles and nickname for {user.name}"
        else:
            return True, f"Updated roles for {user.name} (nickname unchanged for server owner)"

    except Exception as e:
        logger.error(f"Error updating roles and nickname: {e}")
        return False, f"Error updating roles and nickname: {str(e)}"

async def remove_character_roles(user: discord.User, guild: discord.Guild) -> Tuple[bool, str]:
    """Remove all career roles from a user."""
    try:
        member = guild.get_member(user.id)
        if not member:
            return False, f"User {user.name} not found in guild {guild.name}"

        # Get all career roles (those with emojis)
        career_roles = [role for role in guild.roles if any(emoji in role.name for emoji in CAREER_EMOJIS.values())]
        
        # Remove each career role
        for role in career_roles:
            if role in member.roles:
                try:
                    await member.remove_roles(role)
                    logger.debug(f"Removed role {role.name} from user {user.name}")
                except discord.Forbidden:
                    return False, f"Bot lacks permission to remove role {role.name}"
                except discord.HTTPException as e:
                    return False, f"Failed to remove role {role.name}: {str(e)}"

        return True, f"Removed all career roles from {user.name}"
    except Exception as e:
        logger.error(f"Error removing roles: {e}")
        return False, f"Error removing roles: {str(e)}" 