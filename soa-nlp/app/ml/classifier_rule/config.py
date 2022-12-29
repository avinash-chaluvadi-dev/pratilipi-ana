"""
Config file:-
- Contains path to vocab
- Contains path to Corex model
- List of labels
"""
vocab = r"app/ml/classifier_rule/model/voicemail_vocab.pkl"
model = r"app/ml/classifier_rule/model/corex_final_v2.pkl"
categories = [
    "Claim",
    "Benefits",
    "Grievance or Appeal",
    "Membership or Enrollment",
    "OTC",
    "ID Card",
    "Need Case Management",
    "EE Benefits",
    "Authorization",
    "RX or Pharmacy",
    "Provider",
    "Transportation",
    "Nurse Line",
    "Access to Care",
    "Monthly Premium",
    "No Reason Given",
]
