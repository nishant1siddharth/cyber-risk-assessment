from models.mitigation import Mitigation

def get_recommendations(threat_id, risk_level):
    """
    Returns mitigations for a given threat, potentially ordered or filtered by risk level.
    For this framework, we'll return all mitigations for the threat but 
    we could highlight critical ones if the risk_level is high/critical.
    """
    mitigations = Mitigation.query.filter_by(threat_id=threat_id).all()
    
    # Simple logic: if risk is critical, sort Critical priorities first
    # For now, just return them as they are or sort by a predefined priority weight
    priority_map = {'Critical': 1, 'High': 2, 'Medium': 3, 'Low': 4}
    
    mitigations.sort(key=lambda m: priority_map.get(m.priority, 5))
    return mitigations
