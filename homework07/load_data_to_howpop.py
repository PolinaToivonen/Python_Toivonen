import psycopg2
import csv

conn = psycopg2.connect("host=localhost port=5432 dbname=howpop user=postgres password=secret")
cursor = conn.cursor()

query = """
CREATE TABLE IF NOT EXISTS howpop (
    id SERIAL PRIMARY KEY,
    url VARCHAR,
    domain VARCHAR,
    post_id INTEGER,
    published TIMESTAMP,
    author VARCHAR,
    flow VARCHAR,
    polling BOOLEAN,
    content_len INTEGER,
    title VARCHAR,
    comments INTEGER,
    favs INTEGER,
    views INTEGER,
    votes_plus VARCHAR,
    votes_minus VARCHAR,
    views_lognorm NUMERIC,
    favs_lognorm NUMERIC,
    comments_lognorm NUMERIC
)
"""

cursor.execute(query)
conn.commit()

with open('data/howpop_train.csv', 'r', encoding="utf8") as f:
    reader = csv.reader(f)
    # Skip the header row
    next(reader)
    for Id, row in enumerate(reader):
        if row:
            cursor.execute(
                "INSERT INTO howpop VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                [Id] + row
                )
conn.commit()

cursor.execute(
    """
    ALTER TABLE howpop
    DROP COLUMN views_lognorm,
    DROP COLUMN favs_lognorm,
    DROP COLUMN comments_lognorm
    """
)
conn.commit()

cursor.execute(
    """
    ALTER TABLE howpop
    ADD COLUMN year INTEGER,
    ADD COLUMN month INTEGER,
    ADD COLUMN dayofweek INTEGER,
    ADD COLUMN hour INTEGER
    """
)
conn.commit()

cursor.execute(
    """
    UPDATE howpop
    SET year = date_part('year', published),
        month = date_part('month', published),
        dayofweek = date_part('dow', published),
        hour = date_part('hour', published)
    """
)
conn.commit()
