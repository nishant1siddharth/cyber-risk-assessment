def calculate_risk(likelihood, impact):
    """
    Calculates the risk score and classification based on likelihood and impact.
    
    Args:
        likelihood (int): 1-5 scale
        impact (int): 1-5 scale
        
    Returns:
        dict: containing 'score' and 'level'
    """
    try:
        l = int(likelihood)
        i = int(impact)
        if not (1 <= l <= 5 and 1 <= i <= 5):
            raise ValueError("Likelihood and Impact must be between 1 and 5.")
    except (ValueError, TypeError):
        raise ValueError("Invalid input for likelihood or impact.")

    score = l * i
    
    if 1 <= score <= 5:
        level = "Low"
    elif 6 <= score <= 10:
        level = "Medium"
    elif 11 <= score <= 15:
        level = "High"
    elif 16 <= score <= 25:
        level = "Critical"
    else:
        level = "Unknown"
        
    return {
        "likelihood": l,
        "impact": i,
        "score": score,
        "level": level
    }
