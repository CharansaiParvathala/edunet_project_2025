# disease_data.py

disease_info = {
    "Fungal infection": {
        "description": "A skin disease caused by fungus. Commonly affects moist areas.",
        "precautions": ["Keep infected area dry", "Avoid tight clothing", "Use antifungal creams"],
        "treatment": "Topical antifungals like clotrimazole or oral antifungals."
    },
    "Allergy": {
        "description": "A reaction of the immune system to foreign substances like pollen or food.",
        "precautions": ["Avoid known allergens", "Use antihistamines", "Keep clean environment"],
        "treatment": "Antihistamines, corticosteroids, and allergy shots if needed."
    },
    "GERD": {
        "description": "Gastroesophageal reflux disease, stomach acid flows back into the food pipe.",
        "precautions": ["Avoid fatty food", "Don’t lie down after eating", "Eat smaller meals"],
        "treatment": "Antacids, lifestyle changes, and in severe cases, surgery."
    },
    # Add more diseases as needed...
}

def get_disease_info(disease_name):
    return disease_info.get(disease_name, {
        "description": "Information not available.",
        "precautions": [],
        "treatment": "Consult a physician."
    })
  
