MEDIA PLAYER SYSTEM - QUICK START
==================================

You now have two separate media players:

1. SPOTIFY MUSIC PLAYER (spotify_player.py)
   - Displays currently playing Spotify music with album cover
   - Shows song title, artist, and album name
   - Full playback control: SPACE=Play/Pause, N=Next, P=Previous
   - Auto-opens Spotify if not running
   - Real-time updates every 2 seconds
   - Works like a car stereo - seamless control

2. YOUTUBE VIDEO PLAYER (youtube_player.py)
   - Search and play YouTube videos
   - Opens video in VLC player
   - Shows video title in the terminal
   - Commands: search, play, stop, quit

QUICK SETUP:

=== SPOTIFY PLAYER ===
1. Add your Spotify credentials to .env:
   - Get them from https://developer.spotify.com/dashboard
   - Fill in: SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET

2. First run will open browser for authorization:
   python spotify_player.py

3. Authorize the app and paste the redirect URL back into the terminal

=== YOUTUBE PLAYER ===
1. Install VLC Media Player:
   - https://www.videolan.org/vlc/

2. Run the player:
   python youtube_player.py

3. Use commands:
   search Never Gonna Give You Up
   play
   stop
   quit

TIPS:
- Run both players in separate terminal windows
- Spotify player auto-opens Spotify and gives you full playback control
- Use keyboard shortcuts for hands-free music control (perfect for smart mirror!)
- YouTube player searches the web, so any URL or video title works
- Spotify: SPACE=Play/Pause, N=Next, P=Previous, ESC=Exit
- Type 'quit' to exit the YouTube player

NEXT STEPS:
- Combine both into a unified smart mirror interface
- Add controls to play/pause/skip within the players
- Add playlist support
