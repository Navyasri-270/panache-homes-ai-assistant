def calculate_lead_grade(lead_data):
    """
    Calculates lead grade (A, B, C, or D) based on luxury real estate qualification:
    - Grade A: Budget >= AED 1,000,000 and Timeline <= 3 Months
    - Grade B: Budget >= AED 1,000,000 and Timeline > 3 Months
    - Grade C: Budget < AED 1,000,000 or Budget unconfirmed but engaged
    - Grade D: Refuses budget/timeline or browsing only
    """
    budget_str = str(lead_data.get('budget', '')).strip()
    timeline = str(lead_data.get('timeline', '')).strip()
    notes = str(lead_data.get('notes', '')).lower()
    
    # Check for refusal / browsing indicators
    refusal_keywords = ["refuse", "not sharing", "no timeline", "secret", "private", "browsing only", "just looking", "no budget"]
    is_refusal = (
        any(k in budget_str.lower() for k in refusal_keywords) or
        any(k in timeline.lower() for k in refusal_keywords) or
        any(k in notes for k in refusal_keywords)
    )
    
    if is_refusal:
        return "D"
        
    if not budget_str or not timeline:
        # If blank/missing but still in chat loop, mark unconfirmed engaged
        return "C"
        
    try:
        budget_val = int(budget_str)
    except ValueError:
        # Budget not numeric (unconfirmed but user is active)
        return "C"

    # Timeline check (Immediate, 2 Months, 3 Months are <= 3 months)
    is_timeline_short = any(t in timeline for t in ["Immediate", "2 Months", "3 Months"])
    
    if budget_val >= 1000000:
        if is_timeline_short:
            return "A"
        else:
            return "B"
    else:
        return "C"
