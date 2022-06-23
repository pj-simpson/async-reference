import asyncio
import aiohttp
import aiosqlite

# This is an example of a more 'real life' script, which utilizes the aiohttp library to grab
# information about a musical artist from the discogs.com api and then aiosqlite to create and push that data
# into a sqlite database.

# https://www.discogs.com/developers
# https://pypi.org/project/aiosqlite/


async def create_artist_table() -> None:
    """
    Checks to see whether or not the Artist table exists in the SQLiteDB.
    Creates if it doesn't
    """
    async with aiosqlite.connect("bands.db") as db:
        check = await db.execute(
            """
            SELECT count(name) FROM sqlite_master 
            WHERE type='table' 
            AND name='artist'
            """
        )
        table_exists = await check.fetchone()
        if table_exists[0] == 0:
            await db.execute(
                """
                CREATE TABLE artist (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                biog TEXT NOT NULL,
                releases_uri TEXT NOT NULL,
                external_id INTEGER NOT NULL
            );
            """
            )
            await db.commit()


async def get_artist_details(artist_id: int) -> str:
    """
    Fetches an artists information from the discogs API

    :param artist_id: number representing the artist id in the discogs API
    :return: discogs API json representing a single artist
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.discogs.com/artists/{artist_id}") as resp:
            result = await resp.json(content_type=None)
            return result


async def create_artist(band_details: str) -> None:
    """
    Checks whether or not an artist record already exists in our SQLite DB
    If it doesnt, it creates the relevant record.

    :param band_details: json of single artist details from the discogs API
    """
    band_name = band_details["name"]
    band_biography = band_details["profile"]
    discogs_external_band_id = band_details["id"]
    releases_uri = band_details["releases_url"]

    # this will enforce connection only if the file exists
    async with aiosqlite.connect("file:bands.db?mode=rw", uri=True) as db:

        check = await db.execute(
            f"""
            SELECT count(*) FROM artist 
            WHERE external_id={discogs_external_band_id}
            """
        )
        table_exists = await check.fetchone()
        if table_exists[0] == 0:
            await db.execute(
                """
                INSERT INTO artist (name, biog, external_id,releases_uri)
                VALUES(?,?,?,?);
                """,
                (band_name, band_biography, discogs_external_band_id, releases_uri),
            )
            await db.commit()


async def create_releases_table():
    """
    Checks to see whether or not the Releases table exists in the SQLiteDB.
    Creates if it doesn't
    """
    async with aiosqlite.connect("bands.db") as db:
        check = await db.execute(
            """
            SELECT count(name) FROM sqlite_master 
            WHERE type='table' 
            AND name='releases'
            """
        )
        table_exists = await check.fetchone()
        if table_exists[0] == 0:
            await db.execute(
                """
                CREATE TABLE releases (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                link TEXT NOT NULL , 
                external_id INTEGER NOT NULL,
                artist_external_id INTEGER NOT NULL,
                artist_id INTEGER NOT NULL,
                
                FOREIGN KEY (artist_external_id) REFERENCES artist (external_id),
                FOREIGN KEY (artist_id) REFERENCES artist (id)
            );
            """
            )
            await db.commit()


async def get_artist_release_uri(band_details: int) -> str:
    """
    Fetches an artist's release URI from our SQLite DB

    :param artist_id: number representing the artist id in the discogs API
    """
    async with aiosqlite.connect("bands.db") as db:
        async with db.execute(
            f"""
            SELECT releases_uri FROM artist 
            WHERE external_id = {band_details}
            """
        ) as cursor:
            row = await cursor.fetchone()
            releases_uri = row[0]
            return releases_uri


async def get_artist_releases(releases_uri: str) -> str:
    """
    Fetches an artist's release information from the discogs API

    :param releases_uri: url of the resource at the Discogs end.
    :return: discogs API json representing a single artist
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(releases_uri) as resp:
            result = await resp.json(content_type=None)
            return result["releases"]


async def create_release(release: str, artist_external_id: int) -> str:
    """
    Checks whether or not asingle release has record already existing in our SQLite DB
    If it doesnt, it creates the relevant record.

    :param release: json of single artist's release details from the discogs API
    """
    title = release["title"]
    year = release["year"]
    link = release["resource_url"]
    external_id = release["id"]

    # this will enforce connection only if the file exists
    async with aiosqlite.connect("file:bands.db?mode=rw", uri=True) as db:
        check = await db.execute(
            f"""
            SELECT count(*) FROM releases 
            WHERE external_id={external_id} AND artist_external_id= {artist_external_id}
            """
        )
        release_exists = await check.fetchone()
        if release_exists[0] == 0:
            # get our internal unique identifier for the artist
            get_internal_artist_id = await db.execute(
                f"""
                        SELECT id FROM artist 
                        WHERE external_id={artist_external_id}
                        """
            )
            artist_internal_id = await get_internal_artist_id.fetchone()
            # crete the record for the release
            await db.execute(
                """
                INSERT INTO releases (title,year,link,external_id,artist_external_id,artist_id)
                VALUES(?,?,?,?,?,?);
                """,
                (title, year, link, external_id, artist_external_id,artist_internal_id[0]),
            )
            await db.commit()


async def main() -> None:
    """
    Fetches the details for the band 'Circuit Breaker' from the Discogs.com API and their release history.
    Pushes the data into a SQLite DB.
    """
    DISCOGS_ARTIST_ID = 3552343

    await create_artist_table()
    artist_details = await get_artist_details(DISCOGS_ARTIST_ID)
    await create_artist(artist_details)
    await create_releases_table()
    artist_release_uri = await get_artist_release_uri(DISCOGS_ARTIST_ID)
    artist_releases = await get_artist_releases(artist_release_uri)

    # This should be where most of the 'gains' from concurrency happen.
    tasks = []
    for release in artist_releases:
        tasks.append(create_release(release, DISCOGS_ARTIST_ID))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
