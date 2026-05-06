# Dummy dataset (replace later with DB)
BUSINESS_DATA = {
    1: {"name": "ABC Traders", "pincode": 560001, "transactions": 120},
    2: {"name": "XYZ Stores", "pincode": 560001, "transactions": 5},
    3: {"name": "Fresh Mart", "pincode": 560002, "transactions": 0},
    4: {"name": "Tech Solutions", "pincode": 560001, "transactions": 60},
}


# ---------------------------
# ACTIVITY STATUS
# ---------------------------
def get_activity_status(record_id: int):
    business = BUSINESS_DATA.get(record_id)

    if not business:
        return {
            "business": "Unknown",
            "status": "Not Found",
            "explanation": "No record found for given ID"
        }

    tx = business["transactions"]

    if tx > 50:
        status = "Active"
        explanation = "High transaction volume"
    elif tx > 0:
        status = "Dormant"
        explanation = "Low activity detected"
    else:
        status = "Closed"
        explanation = "No transactions found"

    return {
        "business": business["name"],
        "status": status,
        "explanation": explanation
    }


# ---------------------------
# QUERY ENGINE
# ---------------------------
def query_by_pincode(pincode: int):
    results = []

    for record_id, business in BUSINESS_DATA.items():
        if business["pincode"] == pincode:

            tx = business["transactions"]

            if tx > 50:
                status = "Active"
                issue = "No issues"
            elif tx > 0:
                status = "Dormant"
                issue = "Low activity"
            else:
                status = "Closed"
                issue = "No transactions"

            results.append({
                "id": record_id,
                "name": business["name"],
                "status": status,
                "issue": issue
            })

    return {"results": results}
