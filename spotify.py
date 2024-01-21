import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import youtube_dl
# Replace with your own credentials
client_id = ''
client_secret = ''

# # Authenticate with Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# # Replace with the playlist ID 
playlist_id = '2XsjngUvAZ1Ya96t83GUWj'

# # Get the playlist tracks
results = sp.playlist_tracks(playlist_id)
tracks = results['items']

# # List to store track names
track_names_list = []

# # Store track names in the list
for track in tracks:
    track_name = track['track']['name']
    track_names_list.append(track_name)

# # Print track names list
print("Track Names List:")
# print(track_names_list)
song_names = [track_names_list]
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
def download_song(song_name):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            search_query = f"{song_name} audio"
            info = ydl.extract_info(f"ytsearch:{search_query}", download=False)['entries'][0]
            ydl.download([info['webpage_url']])
            print(f"Downloaded: {song_name}")
        except Exception as e:
            print(f"Failed to download {song_name}: {e}")
for song in song_names:
    download_song(song)

