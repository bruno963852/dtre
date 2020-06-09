from discord.ext.commands import Context


def get_attachment(ctx: Context, url: str):
    """
    Returns the url of an attached image instead of a text url. If there's no attached image, returns the passed url
    @param ctx: Context of the command
    @param url: url of the
    @return:
    """
    attachments = ctx.message.attachments
    if len(attachments) > 0:
        url = attachments[0].url
    return url