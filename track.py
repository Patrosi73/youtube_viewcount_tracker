import subprocess
import psycopg2
import datetime
import os
import argparse
from dotenv import load_dotenv
load_dotenv()
postgres_passwd=os.getenv("POSTGRES_PASSWD")
postgres_dbname=os.getenv("POSTGRES_DBNAME")
postgres_username=os.getenv("POSTGRES_USERNAME")
postgres_host=os.getenv("POSTGRES_HOST")
postgres_port=os.getenv("POSTGRES_PORT")

def get_count(url):
    viewercount = subprocess.check_output(['yt-dlp', f"--print", f"concurrent_view_count", url, f"--ignore-no-formats-error"])
    viewercount = viewercount.decode('utf-8').partition('\n')[0]
    return viewercount
def import_to_database(viewercount, url):
    if viewercount.isdigit():
        viewercount = int(viewercount)
        conn = psycopg2.connect(dbname=postgres_dbname, user=postgres_username, password=postgres_passwd, host=postgres_host, port=postgres_port)
        cur = conn.cursor()
        cur.execute("INSERT INTO viewers (viewercount, videoid, time) VALUES (%s, %s, %s)", (viewercount, url, datetime.datetime.now()))
        conn.commit()
        cur.close()
        conn.close()
    else:
        print(f"invalid viewer count retrieved: {viewercount}")

def main(url):
    if not url:
        print("video URL is not provided")
        return
    viewercount = get_count(url)
    if viewercount is not None:
        import_to_database(viewercount, url)
    else:
        print("failed to retrieve view count")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube viewer count tracker")
    parser.add_argument("video_url", type=str, help="URL of the YouTube video")
    args = parser.parse_args()

    video_url = args.video_url
    if video_url:
        main(video_url)
    else:
        print("no video URL provided")