#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach
# http://www.bentedder.com/use-pgadmin-access-postgres-database-within-vagrant-box/
# Database connection

DB = []


# Get posts from database.
def GetAllPosts():
    """Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    """
    try:
    # "postgresql://vagrant:vagrant@localhost/forum"
        conn = psycopg2.connect("dbname=forum")
    except psycopg2.Error as e:
        print("Error: Unable to connect to the database", e)
        exit(-1)
    cur = conn.cursor()
    cur.execute('SELECT * FROM posts;')
    DB = cur.fetchall()
    print(DB)
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    posts.sort(key=lambda row: row['time'], reverse=False)
    conn.close()
    return posts


# Add a post to the database.
def AddPost(content):
    """Add a new post to the database.

    Args:
      content: The text content of the new post.
    """
    try:
        # "postgresql://vagrant:vagrant@localhost/forum"
        conn = psycopg2.connect("dbname=forum")
    except psycopg2.Error as e:
        print("Error: Unable to connect to the database", e)
        exit(-1)
    cur = conn.cursor()
    cur.execute('INSERT INTO posts VALUES (%s);', (bleach.clean(content),))
    conn.commit()
    conn.close()


print('Calling function')
GetAllPosts()

# conn.close()
