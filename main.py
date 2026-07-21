import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routes.auth import router as auth_router
from routes.students import router as students_router
from routes.subjects import router as subjects_router
from routes.exams import router as exams_router
from routes.results import router as results_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Online Examination & Result Management System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router)
app.include_router(students_router)
app.include_router(subjects_router)
app.include_router(exams_router)
app.include_router(results_router)


@app.get("/")
def home():

    logger.info("Application Started Successfully")

    return {
        "message": "Online Examination & Result Management System"
    }
