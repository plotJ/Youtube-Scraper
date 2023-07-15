import pandas as pd
import re
import html

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

# Set up the YouTube API client
api_key = 'INSERT API KEY HERE'
youtube = build('youtube', 'v3', developerKey=api_key)

# Prompt the user to enter a channel URL
channel_url = input("Enter the URL of the YouTube channel: ")

# Check if the input is a custom URL (vanity URL)
if "user" in channel_url:
    custom_url = channel_url.split('/')[-1]

    # Call the API to retrieve the channel ID from the custom URL
    try:
        request = youtube.channels().list(
            part="id",
            forUsername=custom_url
        )
        response = request.execute()
        channel_id = response['items'][0]['id']
    except HttpError as error:
        print(f'An error occurred: {error}')
        channel_id = None
else:

    import re

# Check the URL pattern and extract the channel ID or custom URL
url_pattern = re.compile(
    r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:channel\/|user\/)?([a-zA-Z0-9_-]+)"
)
match = url_pattern.match(channel_url)
url_part = match.group(1) if match else None

if url_part and "user" in channel_url:
    # If it's a custom URL (vanity URL), retrieve the channel ID
    try:
        request = youtube.channels().list(
            part="id",
            forUsername=url_part
        )
        response = request.execute()
        channel_id = response['items'][0]['id']
    except HttpError as error:
        print(f'An error occurred: {error}')
        channel_id = None
elif url_part:
    # If it's a channel URL, extract the channel ID
    channel_id = url_part
else:
    print("Invalid URL")
    channel_id = None

# Define the columns for the Excel file
columns = ['Title', 'Published At', 'Views']

# Create an empty list to store the video data
video_data = []

# Call the API to retrieve the channel's videos
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

        # Loop through the videos and extract the data
        for item in response['items']:
            if item['id']['kind'] == 'youtube#video':
                video_id = item['id']['videoId']
                video_title = html.unescape(item['snippet']['title'])  # Decode HTML entities
                video_published_at = item['snippet']['publishedAt']
                video_views = youtube.videos().list(
                    part='statistics',
                    id=video_id
                ).execute()['items'][0]['statistics']['viewCount']
                video_data.append([video_title, video_published_at, video_views])

        # Check if there are more pages of results
        if 'nextPageToken' in response:
            next_page_token = response['nextPageToken']
        else:
            break

except HttpError as error:
    print(f'An error occurred: {error}')
    video_data = []

# Create a DataFrame from the video data and sort by date published
df = pd.DataFrame(video_data, columns=columns)
df['Published At'] = pd.to_datetime(df['Published At'])
df['Published At'] = df['Published At'].apply(lambda x: x.replace(tzinfo=None))  # Add this line
df = df.sort_values('Published At', ascending=False)


# Save the DataFrame to an Excel file
now = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
filename = f'{channel_id}_{now}.xlsx'
df.to_excel(filename, index=False)

print(f'Success! Saved {len(video_data)} videos to {filename}.')
