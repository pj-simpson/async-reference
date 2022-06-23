import uvicorn
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.applications import Starlette
from starlette.responses import JSONResponse

# Effectively the same ASGI application as 14, but bypassing the 'databases' pakcage and using
# SQLAlchemy's ORM directly

# https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html

engine = create_async_engine("sqlite+aiosqlite:///bands.db")

Base = declarative_base()


class JsonMixin(object):
    def resp_for_json(self):
        resp_dict = self.__dict__.copy()
        del resp_dict["_sa_instance_state"]
        return resp_dict


class Artist(Base, JsonMixin):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    biog = Column(String)
    releases_uri = Column(String)
    external_id = Column(Integer)

    __mapper_args__ = {"eager_defaults": True}


class Releases(Base, JsonMixin):
    __tablename__ = "releases"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    link = Column(String)
    external_id = Column(Integer)
    artist_external_id = Column(Integer, ForeignKey("artist.external_id"))
    artist_id = Column(Integer, ForeignKey("artist.id"))


async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

app = Starlette()


@app.route("/artist/{artist_id}", methods=["GET"])
async def artist_homepage(request):
    """
    Returns a JSON serialized representation of a single artist

    """
    artist_id = request.path_params["artist_id"]
    async with async_session() as session:
        result = await session.execute(select(Artist).where(Artist.id == artist_id))
        artist_result = result.mappings().one()
        artist = artist_result["Artist"]
    return JSONResponse(artist.resp_for_json())


@app.route("/artist/{artist_id}/releases", methods=["GET"])
async def release_list(request):
    """
    Returns a JSON serialized list of all of an artist's releases
    """
    artist_id = request.path_params["artist_id"]
    async with async_session() as session:
        result = await session.execute(
            select(Releases).where(Releases.artist_id == artist_id)
        )
        release_result = result.mappings().all()
        release_list = []
        for item in release_result:
            release = item["Releases"]
            release_list.append(release.resp_for_json())
    return JSONResponse(release_list)


@app.route("/release/{release_id}", methods=["GET"])
async def release_detail(request):
    """
    Returns a JSON serialized representation of a single release

    """
    release_id = request.path_params["release_id"]
    async with async_session() as session:
        result = await session.execute(
            select(Releases).where(Releases.id == release_id)
        )
        release_result = result.mappings().one()
        release = release_result["Releases"]
    return JSONResponse(release.resp_for_json())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
