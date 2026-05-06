from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routes import auth, problems, judge

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CodeSphere API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(problems.router, prefix="", tags=["problems"])
app.include_router(judge.router, prefix="", tags=["judge"])

@app.get("/")
def root():
    return {"message": "CodeSphere API is running"}
