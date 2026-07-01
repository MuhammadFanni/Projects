import mysql.connector
import pandas as pd
from datetime import datetime
import numpy as np
import os

# DATABASE CONFIGURATION
DB_CONFIG = {
    'user': 'abufanni',
    'password': 'abufanni1',
    'host': 'localhost',
    'database': 'abufanni',
    'port': 3305,
    #  Must be False to allow 'INSERT IGNORE' to work
    'raise_on_warnings': False,

    'use_pure': True,
    'connection_timeout': 10
}


def parse_date(date_string):
    if not isinstance(date_string, str): return None
    cleaned_date = date_string.split('(')[0].strip()
    formats = ["%B %d, %Y", "%B %Y", "%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(cleaned_date, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def convert_to_runtime_float(runtime_string):
    if not isinstance(runtime_string, str): return 0.0
    components = runtime_string.split()
    hours, minutes = 0, 0
    for i in range(0, len(components), 2):
        if i + 1 >= len(components): break
        val = int(components[i])
        unit = components[i + 1].lower()
        if "hour" in unit:
            hours = val
        elif "minute" in unit:
            minutes = val
    return hours + (minutes / 60)


def insert_data(db_config, csv_file_path):
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file '{csv_file_path}' not found.")
        return

    conn = None
    cursor = None
    try:
        print(f"Connecting to {db_config['host']}...")
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # turn off foreign key checks temporarily to speed up bulk insertion
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        print(f"Reading CSV from {csv_file_path}...")
        df = pd.read_csv(csv_file_path).replace({np.nan: None})

        print("Starting data insertion...")
        count = 0

        #  CACHES TO PREVENT DUPLICATE INSERTS
        inserted_people = set()
        inserted_countries = set()
        inserted_languages = set()

        for i, row in df.iterrows():
            if count >= 5500: break

            title = row.get('Title')
            if not title: continue

            # Clean Money
            try:
                b_str = str(row.get('Budget', '0')).replace('$', '').replace(',', '').split(' ')[0]
                budget = int(b_str) if b_str.isdigit() else 0
                r_str = str(row.get('Worldwide Gross', '0')).replace('$', '').replace(',', '').split(' ')[0]
                revenue = int(r_str) if r_str.isdigit() else 0
            except:
                budget = 0;
                revenue = 0

            # clean Other Fields
            avg_rating = float(row.get('Average Rating', 0)) if row.get('Average Rating') else 0.0
            meta_score = int(row.get('Metascore', 0)) if row.get('Metascore') and not pd.isna(
                row.get('Metascore')) else 0

            #  insert Movie
            cursor.execute("""
                INSERT INTO Movie (title, average_rating, release_date, budget, revenue, runtime, meta_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (title, avg_rating, parse_date(row.get('Release Date', '')), budget, revenue,
                  convert_to_runtime_float(row.get('Runtime', '')), meta_score))
            movie_id = cursor.lastrowid

            def split_clean(val):
                return [x.strip() for x in str(val).split(',')] if val else []

            #  Process People
            directors = split_clean(row.get('Director'))
            writers = split_clean(row.get('Writer'))
            actors = split_clean(row.get('Cast'))

            all_people_in_row = set(directors + writers + actors)

            for person in all_people_in_row:
                if person not in inserted_people:
                    # INSERT IGNORE handles duplicates gracefully IF raise_on_warnings is False
                    cursor.execute("INSERT IGNORE INTO Person (name) VALUES (%s)", (person,))
                    inserted_people.add(person)

            # link Staff
            for d in directors: cursor.execute(
                "INSERT IGNORE INTO Staff_Movie (person_name, movie_id, role) VALUES (%s, %s, %s)",
                (d, movie_id, 'director'))
            for w in writers: cursor.execute(
                "INSERT IGNORE INTO Staff_Movie (person_name, movie_id, role) VALUES (%s, %s, %s)",
                (w, movie_id, 'writer'))
            for a in actors: cursor.execute(
                "INSERT IGNORE INTO Staff_Movie (person_name, movie_id, role) VALUES (%s, %s, %s)",
                (a, movie_id, 'actor'))

            #  Process Countries
            countries = split_clean(row.get('Country of Origin'))
            for c in countries:
                if c not in inserted_countries:
                    cursor.execute("INSERT IGNORE INTO Country (country_name) VALUES (%s)", (c,))
                    inserted_countries.add(c)
                cursor.execute("INSERT INTO Movie_Country (movie_id, country_name) VALUES (%s, %s)", (movie_id, c))

            #  Process Languages
            languages = split_clean(row.get('Languages'))
            for l in languages:
                if l not in inserted_languages:
                    cursor.execute("INSERT IGNORE INTO Language (language_name) VALUES (%s)", (l,))
                    inserted_languages.add(l)
                cursor.execute("INSERT INTO Movie_Language (movie_id, language_name) VALUES (%s, %s)", (movie_id, l))

            count += 1
            if count % 100 == 0:
                print(f"Inserted {count} movies...")
                conn.commit()

        # re-enable checkss
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()
        print(f"Finished! Total movies inserted: {count}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


if __name__ == "__main__":
    insert_data(DB_CONFIG, "IMDB_Movies_Dataset.csv")