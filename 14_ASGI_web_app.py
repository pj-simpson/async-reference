import uvicorn
from databases import Database
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey

from starlette.applications import Starlette
from starlette.responses import JSONResponse

# This is an ASGI web application, using the Starlette framework and Uvicorn ASGI Server
# I am using the 'databases' package, which gives asyncio support for interacting
# with different databaess using the SQLAlchemy package's 'core expressions'
# The database being used is the one created by the script in 13


# https://www.starlette.io/ ASGI web application framework (and toolkit!)
# https://github.com/encode/databases asyncio support for dtabases using SQLAlchemy Core Expression Language


# Connect to the database
db = Database("sqlite+aiosqlite:///bands.db")

# declare the db tables in the code
metadata = MetaData()

artist = Table(
    "artist",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String()),
    Column("biog", String()),
    Column("releases_uri", String()),
    Column("external_id", Integer),
)

releases = Table(
    "releases",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String()),
    Column("year", Integer),
    Column("link", String()),
    Column("external_id", Integer),
    Column("artist_external_id", Integer, ForeignKey("artist.external_id")),
    Column("artist_id", Integer, ForeignKey("artist.id")),
)

# Declare a Starlette Application
app = Starlette()

# Hook the db connection and disconnection into the app's startup or shutdown events
@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.route("/artist/{artist_id}", methods=["GET"])
async def artist_homepage(request):
    """
    Returns a JSON serialized representation of a single artist

    """
    artist_id = request.path_params["artist_id"]
    query = artist.select().where(artist.c.id == artist_id)
    row = await db.fetch_one(query=query)
    return JSONResponse(
        {
            "id": row.id,
            "name": row.name,
            "biog": row.biog,
            "releases_uri": row.releases_uri,
            "external_id": row.external_id,
        }
    )


@app.route("/artist/{artist_id}/releases", methods=["GET"])
async def release_list(request):
    """
    Returns a JSON serialized list of all of an artist's releases
    """
    artist_id = request.path_params["artist_id"]
    query = releases.select().where(releases.c.artist_id == artist_id)
    row = await db.fetch_all(query=query)
    releases_list = []
    for item in row:
        release = dict()

        release["id"] = item[0]
        release["title"] = item[1]
        release["year"] = item[2]
        release["link"] = item[3]
        release["external_id"] = item[4]
        release["artist_external_id"] = item[5]

        releases_list.append(release)

    return JSONResponse(releases_list)


@app.route("/release/{release_id}", methods=["GET"])
async def release_detail(request):
    """
    Returns a JSON serialized representation of a single release

    """
    release_id = request.path_params["release_id"]
    query = releases.select().where(releases.c.id == release_id)
    row = await db.fetch_one(query=query)
    return JSONResponse(
        {
            "id": row.id,
            "title": row.title,
            "year": row.year,
            "link": row.link,
            "external_id": row.external_id,
            "artist_external_id": row.artist_external_id,
        }
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
