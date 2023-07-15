

STAFF_TITLE = (
    ("Prof","Prof"),
    ("Associate Prof","Associate Prof"),
    ("Dr","Dr"),
    ("Engr","Engr"),
    ("Mr","Mr"),
    ("Mrs","Mrs"),
)


STAFF_TYPE = (
    ("Internal_Evaluator", "Internal Evaluator"),
    ("External_Evaluator", "External Evaluator"),
    ("Supervisor_and_Evaluator", "Supervisor and Evaluator"),
)

GENDER = (
    ("Male", "Male"),
    ("Female", "Female"),
    ("Others", "Others"),
)


EVALUATION_TYPES = {
    "proposal": "Proposal Presentation",
    "work_progress": "Work Progress",
    "internal_defence": "Internal Defense",
    "external_defence": "External Defense",
}


STUDENT_TABLE_HEADER = [
    "Name",
    "Matric Number",
    "Project",
    "Supervisor Approval",
    "Comment",
    "Cordinator Approval",
    "Comment"
]

STAFF_TABLE_HEADER = [
    "Name",
    "Email",
    "Staff Type",
    "Students",
]

APPROVAL_STATUS = (
    ("Approved", "Approved"),
    ("Pending", "Pending"),
    ("Not Approved", "Not Approved"),
)