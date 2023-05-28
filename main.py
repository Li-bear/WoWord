from youtube_transcript_api import YouTubeTranscriptApi
import requests
from bs4 import BeautifulSoup
import re

# Replace the VIDEO_ID with the ID of the YouTube video you want to get the transcript for
VIDEO_ID = '70dS-T5p07U'
# Call the YouTubeTranscriptApi to get the transcript data
try:
    transcript_list = YouTubeTranscriptApi.get_transcript(VIDEO_ID)
    # Join the text of each transcript segment to form the full transcript
    transcript = '\n'.join([t['text'] for t in transcript_list])
    #print(transcript)
except:
    print('An error occurred while retrieving the video transcript.')

#####   INPUT   #####
# Replace the SEARCH_TERM with the term you want to search for on YouTube
SEARCH_TERM = 'animals'
# Set the number of search results you want to retrieve
NUM_RESULTS = 10
#####   INPUT   #####

# Set the base URL for YouTube search queries
BASE_URL = 'https://www.youtube.com'

# Construct the search query URL
query = '+'.join(SEARCH_TERM.split())
url = f'{BASE_URL}/results?search_query={query}'

# Send a GET request to the search query URL
response = requests.get(url)

# Parse the HTML content of the response using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Search for the pattern "videoId":"\w+" in the HTML content of soup
matches = re.findall(r'"videoId":"\w+"', str(soup))

# Print the matches
print(matches)

# Extract the video IDs from the video links
video_ids = []
for match in matches:
    video_id = re.search(r'"videoId":"(\w+)"', match)
    if video_id:
        video_ids.append(video_id.group(1))

# Print the video IDs
print('Video IDs:', video_ids)

for i in range(10):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_ids[i])
        # Join the text of each transcript segment to form the full transcript
        transcript = '\n'.join([t['text'] for t in transcript_list])
        print(transcript)
    except:
        print('An error occurred while retrieving the video transcript.')