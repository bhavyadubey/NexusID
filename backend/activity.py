def classify_activity(months):
    if months <= 6:
        return "Active"
    elif months <= 24:
        return "Dormant"
    else:
        return "Closed"
