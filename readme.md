#DTRE - Discord Tabletop RPG Engine

DTRE is a tabletop rpg engine to be used in discord. If you're tired of complicated tools, but want some more functionality and want a simple streamlined roleplaying experience directly on discord, with no external apps, and that can be easily playable on mobile search no further.

![battle grid example](screenshot_dtre.png)

##How to Add to you Server
Still in development...

##Usage
The bot responds to user commands on text channels.
The prefix for all of the commands can be
* !dtre.
* ?dtre.
* !r.
* ?t.

For Example:

?dtre.create myscenario

that's the sintax of the "create" command.

##Commands
Here's a list with all the commands the bot responds.

###rualive
**aliases:** none <br>
**parameters:** none <br>
**description:** <br>
Just a simple command to test if the bot is alive.

**response:** <br>
message: "Yes, i'm alive!"

note as ncreate
    <size: 16><b>Command: create</b></size>
    <b>aliases: </b> c
    <b>parameters: </b>
    <u>name</u>: str
    the name of the scenario
    <i>optional</i> <u>image_url</u>: str
    the url off the background image for the scenario
    <i>optional</i> <u>square_size_pixels</u>: str
    <i>optional</i> <u>offset_pixels_left</u>: str
    <i>optional</i> <u>offset_pixels_top</u>: str
    <b>description: </b>
    Creates a scenario with the specified name
    Examples:
    ?r.c mydungeon
    ?r.c "just a bridge" https://i.imgur.com/G5kc4QX.jpg 45 17 17
end note

note as nset_offset
    <size: 16><b>Command: set_offset</b></size>
    <b>aliases: </b> so, setoffset, offset
    <b>parameters: </b>
    <u>name</u>: str
    <i>optional</i> <u>offset_pixels_left</u>: str
    <i>optional</i> <u>offset_pixels_top</u>: str
    <b>description: </b>
    Creates a scenario with the specified name
    Examples:
    ?r.c mydungeon
    ?r.c "just a bridge" https://i.imgur.com/G5kc4QX.jpg 45 17 17
end note

note as nset_text_color
    <size: 16><b>Command: set_offset</b></size>
    <b>aliases: </b> so, setoffset, offset
    <b>parameters: </b>
    <u>name</u>: str
    <i>optional</i> <u>offset_pixels_left</u>: str
    <i>optional</i> <u>offset_pixels_top</u>: str
    <b>description: </b>
    Creates a scenario with the specified name
    Examples:
    ?r.c mydungeon
    ?r.c "just a bridge" https://i.imgur.com/G5kc4QX.jpg 45 17 17
end note
end note