import os
from webexteamssdk import WebexTeamsAPI
from webexteamssdk.models.cards.card import AdaptiveCard
from webexteamssdk.models.cards.inputs import Toggle, Text
from webexteamssdk.models.cards.components import TextBlock, Image
from webexteamssdk.models.cards.actions import OpenUrl
from webexteamssdk.utils import make_attachment
from webexteamssdk.models.cards.options import ImageSize

room_id = "Y2lzY29zcGFyazovL3VzL1JPT00vNGM5MjY5NzAtZGM1NC0xMWVjLTg2NWItYmJhYTc3ZmE1ZTU0"

pipe_img = Image(url='https://img.icons8.com/ios/344/merge-git.png',
    size=ImageSize("small"), separator=True)
greeting = TextBlock("Meraki - New Branch Commit")
submit = OpenUrl(os.getenv("CI_PROJECT_URL"), title="Open Project")

card = AdaptiveCard(body=[pipe_img, greeting], actions=[submit])

wxapi = WebexTeamsAPI()
wxapi.messages.create(text="fallback", roomId=room_id, attachments=[make_attachment(card)])
