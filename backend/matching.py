from fuzzywuzzy import fuzz

def compute_similarity(record1, record2):
    name_score = fuzz.token_sort_ratio(record1['name'], record2['name']) / 100
    address_score = fuzz.token_sort_ratio(record1['address'], record2['address']) / 100
    
    pan_match = 1 if record1['pan'] and record1['pan'] == record2['pan'] else 0
    gstin_match = 1 if record1['gstin'] and record1['gstin'] == record2['gstin'] else 0

    confidence = (0.4 * name_score) + (0.3 * address_score) + (0.15 * pan_match) + (0.15 * gstin_match)

    return {
        "confidence": round(confidence, 2),
        "explanation": {
            "name_similarity": name_score,
            "address_similarity": address_score,
            "pan_match": pan_match,
            "gstin_match": gstin_match
        }
    }
