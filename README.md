# YouTube viewcount tracker
Get the current livestream viewer count and save it in a postgresql database along with the URL and time

(also my first time working with databases... absolute hell. what am i doing what am i doing)

![Beekeeper_Studio_Ultimate_tA4TpKa0vk](https://github.com/user-attachments/assets/7d25ba02-9caa-4e88-95e2-8681433fb54d)

# Requirements
- [postgresql server](https://www.postgresql.org/download/) already set up
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) in PATH
- [Python](https://www.python.org/downloads/) in PATH

# Setup
> [!NOTE]
> For Windows users, please check if Python is in PATH. And make sure to run Python correctly as most times it's `py` or `python` instead of `python3` (at least on Windows systems). In this guide, this will be referred to as `python` at the start of the command.
0. Git clone the repository/download it as a .zip
1. Open your postgresql console and the `viewcounts.sql` file
2. Make sure you're connected to a database, copy the command in the .sql file and paste it in
3. Rename `.env.example` to `.env` and enter your postgresql information
4. Run `python track.py` appended with a valid YouTube Live URL
> [!NOTE]
> Make sure the stream is live and is not in a "waiting" state.
> [yt-dlp was supposed to capture data in that state anyway](https://github.com/yt-dlp/yt-dlp/pull/5152#:~:text=for%20youtube%2C%20this%20also%20applies%20to%20upcoming%20streams%2Fpremieres%20where%20they%20have%20the%20%22waiting%22%20count.), but it errors out.. don't know why.
5. If completed successfully you should have an entry in the newly created `viewers` table.

# Automation
I've pre-included a batch file for Windows users that automatically scrapes the viewer count every minute (because that's around the time YouTube takes to refresh the count on their frontend). Edit **run_example.bat** with your livestream's ID.
If anyone's willing to do a bash version, go right ahead! PRs are welcome.
