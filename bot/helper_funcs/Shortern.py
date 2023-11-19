import requests
import random
import base64
from urllib.parse import quote
from urllib3 import disable_warnings

SHORTENER = "https://atglinks.com/"
SHORTENER_API = "498ee7efdd27b59fa6436070a5a3eb28d1a39e80"


def short_url(longurl):
    disable_warnings()
    return requests.get(f'{SHORTENER}api?api={SHORTENER_API}&url={longurl}&format=text').text  
  
def checking_access(user_id, button=None):
    if not config_dict['TOKEN_TIMEOUT']:
        return None, button
    user_data.setdefault(user_id, {})
    data = user_data[user_id]
    expire = data.get('time')
    isExpired = (expire is None or expire is not None and (
        time() - expire) > config_dict['TOKEN_TIMEOUT'])
    if isExpired:
        token = data['token'] if expire is None and 'token' in data else str(
            uuid4())
        if expire is not None:
            del data['time']
        data['token'] = token
        user_data[user_id].update(data)
        if button is None:
            button = ButtonMaker()
        button.ubutton('Refresh Token', short_url(
            f'https://t.me/{bot_name}?start={token}'))
        return 'Token is expired, refresh your token and try again.', button
    return None, button

async def start(_, message):
    if len(message.command) > 1:
        userid = message.from_user.id
        input_token = message.command[1]
        if userid not in user_data:
            return await sendMessage(message, 'Who are you?')
        data = user_data[userid]
        if 'token' not in data or data['token'] != input_token:
            return await sendMessage(message, 'This is a token already expired')
        data['token'] = str(uuid4())
        data['time'] = time()
        user_data[userid].update(data)
        return await sendMessage(message, 'Token refreshed successfully!')
    elif config_dict['DM_MODE']:
        start_string = 'Bot Started.\n' \
            'Now you can change settings and encode.\n'
    else:
        start_string = '🌹 Welcome To One Of A Modified zenith encode bot\n' \
            'This bot can encode your videos and you can change the settings !\n' \
            '👨🏽‍💻 Powered By: "https://t.me/AnimeZenith"'
    await sendMessage(message, start_string)
