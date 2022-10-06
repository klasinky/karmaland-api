from typing import List

import requests
from sqlalchemy.orm import Session

import utils.crud as controller
from schemas.channels import Channel
from settings import Settings
from utils.constants import URL_USER, TWITCH, VALIDATE_TOKEN, GENERATE_TOKEN_TWITCH, GET_CHANNEL_INFO, YOUTUBE


def check_users_list(channels: List[Channel], db: Session, settings: Settings):
    results = []
    
    token_twitch = controller.get_token(db)
    if not token_twitch or not validate_twitch_token(token_twitch):
        # Get new token
        twitch_data = get_new_twitch_token(settings.SECRET_ID_TWITCH, settings)
        # Create or update token
        token_twitch = twitch_data['access_token']
        expire_twitch = twitch_data['expires_in']
        controller.create_or_update_token(db, token_twitch, expire_twitch)

    for channel in channels:
        if channel.platform == TWITCH:
            data = check_twitch_user(channel.name, token_twitch, settings)
        else:
            data = check_youtube_user(channel.name, channel.channel_id, settings.API_KEY_YOUTUBE)
        if data:
            results.append(data)
    return results


def check_twitch_user(twitch_name, token, settings):
    url = URL_USER + twitch_name
    # Post request to Twitch API
    token = "Bearer " + token
    response = requests.get(url, headers={'Client-Id': settings.CLIENT_ID_TWITCH, 'Authorization': token})
    data = response.json()['data']
    # Check if user is online
    if len(data) > 0:
        data_channel = data[0]
        if data_channel['game_name'] == 'Minecraft':
            ctx = {
                'user_name': twitch_name,
                'title': data_channel['title'],
                'platform': TWITCH,
                'viewer_count': data_channel['viewer_count'],
            }
            return ctx
    return None


def check_youtube_user(youtube_name, channel_id, api_key):
    url_channel_info = GET_CHANNEL_INFO.format(channel_id, api_key)
    response = requests.get(url_channel_info)
    data = response.json()
    
    if len(data['items']) > 0:
        data_channel = data['items'][0]['snippet']
        ctx = {
            'user_name': youtube_name,
            'title': data_channel['title'],
            'platform': YOUTUBE,
        }
        return ctx
    return None


def validate_twitch_token(token) -> bool:
    response = requests.get(VALIDATE_TOKEN, headers={'Authorization': "Bearer " + token})
    return True if response.status_code == 200 else False


def get_new_twitch_token(secret_id, settings):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'client_id': settings.CLIENT_ID_TWITCH,
        'client_secret': secret_id,
        'grant_type': 'client_credentials',
    }
    response = requests.post(GENERATE_TOKEN_TWITCH, headers=headers, data=data)
    return response.json()
