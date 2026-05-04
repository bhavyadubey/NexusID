from fastapi import FastAPI
import pandas as pd
from matching import compute_similarity
from activity import classify_activity

app = FastAPI()

data = pd.read_csv("../data/sample_data.csv")

@app.get("/")
def home():
    return {"message": "NexusID API Running"}

@app.get("/match")
def match_records(id1: int, id2: int):
    r1 = data[data['id'] == id1].iloc[0]
    r2 = data[data['id'] == id2].iloc[0]

    result = compute_similarity(r1, r2)

    decision = "REJECT"
    if result["confidence"] > 0.9:
        decision = "AUTO-MERGE"
    elif result["confidence"] > 0.6:
        decision = "REVIEW"

    return {
        "record_1": r1.to_dict(),
        "record_2": r2.to_dict(),
        "confidence": result["confidence"],
        "decision": decision,
        "explanation": result["explanation"]
    }

@app.get("/activity/{id}")
def activity_status(id: int):
    record = data[data['id'] == id].iloc[0]
    status = classify_activity(record['last_activity_months'])

    return {
        "business": record['name'],
        "status": status,
        "last_activity_months": record['last_activity_months'],
        "explanation": f"No activity for {record['last_activity_months']} months"
    }

@app.get("/query")
def query(pincode: int):
    filtered = data[data['pincode'] == pincode]

    result = []
    for _, row in filtered.iterrows():
        status = classify_activity(row['last_activity_months'])
        if status == "Active" and row['last_activity_months'] > 12:
            result.append({
                "name": row['name'],
                "status": status,
                "issue": "No recent inspection"
            })

    return {"results": result}
