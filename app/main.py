from fastapi import FastAPI

from controllers.analysis_controller import router
from database.database import create_table

app = FastAPI()

# Create SQLite table when application starts
create_table()

app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )