def match_records(id1: int, id2: int):

    # Dummy logic
    confidence = 0.87

    if confidence > 0.8:
        decision = "AUTO-MERGE"
    elif confidence > 0.5:
        decision = "REVIEW"
    else:
        decision = "NO MATCH"

    explanation = {
        "name_match": "High",
        "dob_match": "Exact",
        "address_match": "Partial",
        "phone_match": "Exact"
    }

    return {
        "confidence": confidence,
        "decision": decision,
        "explanation": explanation
    }
