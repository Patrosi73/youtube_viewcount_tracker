import subprocess
import psycopg2
import datetime
def get_count(url):
    viewercount = subprocess.check_output(['yt-dlp', f"--print", f"concurrent_viewers", url])
    viewercount = viewercount.decode('utf-8').partition('\n')[0]
    return viewercount
def import_to_database(viewercount, url):


