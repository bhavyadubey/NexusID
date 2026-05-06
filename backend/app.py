from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from matching import match_records
from activity import get_activity_status, query_by_pincode

app = FastAPI()

# ---------------------------
# CORS
# ---------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# ROOT
# ---------------------------
@app.get("/")
def root():
    return {"message": "NexusID API Running"}

# ---------------------------
# MATCH ENDPOINT
# ---------------------------
@app.get("/match")
def match(id1: int, id2: int):
    return match_records(id1, id2)

# ---------------------------
# ACTIVITY ENDPOINT
# ---------------------------
@app.get("/activity/{id}")
def activity(id: int):
    return get_activity_status(id)

# ---------------------------
# QUERY ENDPOINT
# ---------------------------
@app.get("/query")
def query(pincode: int):
    return query_by_pincode(pincode)
