import pandas as pd
import re
import html

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

# Set up the YouTube API client
api_key = 'AIzaSyA7O31notbQM4XXa226uoCDxwc26rLrD0E'
youtube = build('youtube', 'v3', developerKey=api_key)

# Prompt the user to enter a channel URL
channel_input = input("Enter the channel URL: ")

# Extract the channel name from the URL
url_pattern = re.compile(
    r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/\@([a-zA-Z0-9_-]+)"
)
match = url_pattern.match(channel_input)
channelname = match.group(1) if match else None

if not channelname:
    print("Invalid URL")
else:
    # Call the API to retrieve the channel ID from the channel name
    try:
        request = youtube.search().list(
            part="id",
            q=channelname,
            type="channel",
            maxResults=1
        )
        response = request.execute()
        channel_id = response['items'][0]['id']['channelId']
    except HttpError as error:
        print(f'An error occurred: {error}')
        channel_id = None
    except KeyError:
        print("Channel not found.")
        channel_id = None

if channel_id is None:
    print("Invalid input. Please try again.")
else:
    columns = ['Title', 'Published At', 'Views']
    video_data = []

    try:
        next_page_token = None
        while True:
            request = youtube.search().list(
                part='id,snippet',
                channelId=channel_id,
                maxResults=50,
                order='date',
                pageToken=next_page_token
            )
            response = request.execute()

            if not response['items']:
                print('No videos found.')
                break

            for item in response['items']:
                if item['id']['kind'] == 'youtube#video':
                    video_id = item['id']['videoId']
                    video_title = html.unescape(item['snippet']['title'])
                    video_published_at = item['snippet']['publishedAt']
                    try:
                        video_views = youtube.videos().list(
                            part='statistics',
                            id=video_id
                        ).execute()['items'][0]['statistics']['viewCount']
                    except KeyError:
                        video_views = 'N/A'
                    video_data.append([video_title, video_published_at, video_views])

            if 'nextPageToken' in response:
                next_page_token = response['nextPageToken']
            else:
                break

    except HttpError as error:
        print(f'An error occurred: {error}')
        video_data = []

    df = pd.DataFrame(video_data, columns=columns)
    df['Published At'] = pd.to_datetime(df['Published At'])
    df['Published At'] = df['Published At'].apply(lambda x: x.replace(tzinfo=None))
    df = df.sort_values('Published At', ascending=False)

    now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    filename = f'{channel_id}_{now}.xlsx'
    df.to_excel(filename, index=False)

    print(f'Success! Saved {len(video_data)} videos to {filename}.')
