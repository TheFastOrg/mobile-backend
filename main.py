from fastapi import FastAPI
from db.engine import Session
from db.models import Ba7beshBusiness

from typing import Any, Dict

app = FastAPI()


@app.get("/")
async def test_route() -> Dict[str, Any]:
    # try:
    with Session() as session:
        # result = connection.execute(text("SELECT * FROM information_schema.tables; "))
        results = session.query(Ba7beshBusiness).limit(10).all()
        print("Database connectivity test successful:", results)
        # return {"message": f"Database connectivity test successful: {result.scalar()}"}
    # print("Database connectivity test successful:", result.scalar() == 1)
    # except Exception as e:
    #     print("Error connecting to the database:", e)
    return {"message": "Hey, ba7besh started here!"}
