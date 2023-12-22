from typing import Any, Dict

from fastapi import FastAPI

from core.entities.business.queries import BusinessListQuery
from core.services.business_service import BusinessService
from db.engine import Session
from db.models import Business
from db.repositories.business_repository import DBBusinessRepository

app = FastAPI()

from datetime import time


@app.get("/")
async def test_route(request) -> Dict[str, Any]:
    with Session() as session:
        # result = connection.execute(text("SELECT * FROM information_schema.tables; "))
        results = session.query(Business).limit(10).all()

        print("Database connectivity test successful:", results)
    return {"message": "Hey, ba7besh started here!"}


@app.post("/search")
async def search():
    query = BusinessListQuery(
        day_filter=1,
        status="draft",
        min_opening_time=time(10, 0, 0),
        max_closing_time=time(23, 59, 59),
        page_size=10,
        page_number=2,
    )
    business = BusinessService(DBBusinessRepository()).list_all(query)
    print("Database connectivity test successful:", business)
    return {"message": "Hey, ba7besh started here!"}
