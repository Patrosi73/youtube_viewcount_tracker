import subprocess
import psycopg2
import datetime
import os
import argparse
from dotenv import load_dotenv

load_dotenv()
postgres_passwd = os.getenv("POSTGRES_PASSWD")
postgres_dbname = os.getenv("POSTGRES_DBNAME")
postgres_username = os.getenv("POSTGRES_USERNAME")
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")

def get_count(url):
    viewercount = subprocess.check_output(['yt-dlp', "--print", "concurrent_view_count", url, "--ignore-no-formats-error"])
    viewercount = viewercount.decode('utf-8').partition('\n')[0]
    return viewercount

def import_to_database(viewercount, video_id):
    if viewercount.isdigit():
        viewercount = int(viewercount)
        conn = psycopg2.connect(dbname=postgres_dbname, user=postgres_username, password=postgres_passwd, host=postgres_host, port=postgres_port)
        cur = conn.cursor()
        cur.execute(f"INSERT INTO viewers (viewercount, videoid, time) VALUES (%s, %s, %s)", (viewercount, video_id, datetime.datetime.now()))
        conn.commit()
        cur.close()
        conn.close()
    else:
        print(f"invalid viewer count retrieved: {viewercount}")

def get_video_id(url):
    video_id = subprocess.check_output(['yt-dlp', "--print", "id", url, "--ignore-no-formats-error"])
    video_id = video_id.decode('utf-8').partition('\n')[0]
    return video_id

def table_exists(video_id):
    conn = psycopg2.connect(dbname=postgres_dbname, user=postgres_username, password=postgres_passwd, host=postgres_host, port=postgres_port)
    cur = conn.cursor()
    cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)", (video_id,))
    exists = cur.fetchone()[0]
    cur.close()
    conn.close()
    return exists

def create_table(video_id):
    if not table_exists(video_id):
        conn = psycopg2.connect(dbname=postgres_dbname, user=postgres_username, password=postgres_passwd, host=postgres_host, port=postgres_port)
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE {video_id} (viewercount int, videoid text, time TIMESTAMPTZ)")
        conn.commit()
        cur.close()
        conn.close()

def main(url):
    if not url:
        print("video URL is not provided")
        return
    viewercount = get_count(url)
    video_id = get_video_id(url)
    if viewercount != "NA":
        #create_table(video_id)
        import_to_database(viewercount, video_id)
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