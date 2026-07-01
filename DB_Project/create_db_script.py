import mysql.connector
from mysql.connector import errorcode

# DATABASE CONFIGURATION
DB_CONFIG = {
    'user': 'abufanni',
    'password': 'abufanni1',
    'host': 'localhost',
    'database': 'abufanni',
    'port': 3305,
    'raise_on_warnings': True,
    'use_pure': True,
    'connection_timeout': 10
}


def create_database(config):
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        #  Drop existing tables
        #  Drop tables with Foreign Keys first
        tables_drop = [
            "Movie_Language", "Movie_Country", "Staff_Movie",
            "Language", "Country", "Person", "Movie"
        ]

        # Disable FK checks to allow dropping tables in any order
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

        for table in tables_drop:
            try:
                cursor.execute(f"DROP TABLE IF EXISTS `{table}`;")
                print(f"Table {table} dropped.")
            except mysql.connector.Error as err:
                # Ignore specific "Unknown table" errors if they somehow bypass IF EXISTS
                if err.errno == 1051:
                    print(f"Table {table} did not exist (skipped).")
                else:
                    print(f"Warning dropping {table}: {err}")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

        #  Define Tables
        tables = {}
        tables['Movie'] = (
            "CREATE TABLE `Movie` ("
            " `movie_id` INT NOT NULL AUTO_INCREMENT,"
            " `title` VARCHAR(255),"
            " `average_rating` FLOAT,"
            " `release_date` DATE,"
            " `budget` BIGINT,"
            " `revenue` BIGINT,"
            " `runtime` FLOAT,"
            " `meta_score` INT,"
            " PRIMARY KEY (`movie_id`)"
            ");"
        )
        tables['Person'] = (
            "CREATE TABLE `Person` ("
            " `name` VARCHAR(255) NOT NULL,"
            " PRIMARY KEY (`name`)"
            ")"
        )
        tables['Staff_Movie'] = (
            "CREATE TABLE `Staff_Movie` ("
            " `person_name` VARCHAR(255) NOT NULL,"
            " `movie_id` INT NOT NULL,"
            " `role` ENUM('actor', 'writer', 'director'),"
            " FOREIGN KEY (`person_name`) REFERENCES `Person`(`name`),"
            " FOREIGN KEY (`movie_id`) REFERENCES `Movie`(`movie_id`),"
            " PRIMARY KEY (`person_name`, `movie_id`, `role`)"
            ");"
        )
        tables['Country'] = (
            "CREATE TABLE `Country` ("
            " `country_name` VARCHAR(255) NOT NULL,"
            " PRIMARY KEY (`country_name`)"
            ")"
        )
        tables['Movie_Country'] = (
            "CREATE TABLE `Movie_Country` ("
            " `movie_id` INT NOT NULL,"
            " `country_name` VARCHAR(255) NOT NULL,"
            " FOREIGN KEY (`movie_id`) REFERENCES `Movie`(`movie_id`),"
            " FOREIGN KEY (`country_name`) REFERENCES `Country`(`country_name`)"
            ")"
        )
        tables['Language'] = (
            "CREATE TABLE `Language` ("
            " `language_name` VARCHAR(255) NOT NULL,"
            " PRIMARY KEY (`language_name`)"
            ")"
        )
        tables['Movie_Language'] = (
            "CREATE TABLE `Movie_Language` ("
            " `movie_id` INT NOT NULL,"
            " `language_name` VARCHAR(255) NOT NULL,"
            " FOREIGN KEY (`movie_id`) REFERENCES `Movie`(`movie_id`),"
            " FOREIGN KEY (`language_name`) REFERENCES `Language`(`language_name`)"
            ")"
        )

        #  create Tables
        for table_name, table_description in tables.items():
            try:
                print(f"Creating table {table_name}: ", end="")
                cursor.execute(table_description)
                print("OK")
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)

        #  Create Full-Text Indices
        print("Creating Full-Text Indices...")
        try:
            cursor.execute("CREATE FULLTEXT INDEX idx_movie_title ON Movie(title);")
            cursor.execute("CREATE FULLTEXT INDEX idx_person_name ON Staff_Movie(person_name);")
            print("Indices created.")
        except mysql.connector.Error as err:
            print(f"Index warning: {err.msg}")

        conn.commit()
        print("Database schema created successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


if __name__ == "__main__":
    create_database(DB_CONFIG)