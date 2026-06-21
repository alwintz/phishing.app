from fastapi import FastAPI

from controllers.analysis_controller import router
from database.database import create_table

app = FastAPI()

# Create SQLite table when application starts
create_table()

app.include_router(router)