from typing import Dict


# Incident -> Department Mapping
DEPARTMENT_MAPPING: Dict[str, str] = {
    "Pothole": "Road Department",
    "Waterlogging": "Drainage Department",
    "Accident": "Traffic Police",
    "Signal Failure": "Traffic Police",
    "Blocked Road": "Municipal Corporation",
    "Construction": "Road Department",
    "Normal Road": "No Action Required"
}


def assign_department(incident_type: str) -> str:
    """
    Assign the appropriate department
    based on the detected incident type.
    """

    return DEPARTMENT_MAPPING.get(
        incident_type,
        "Municipal Corporation"
    )


if __name__ == "__main__":

    incidents = [
        "Pothole",
        "Accident",
        "Waterlogging",
        "Signal Failure",
        "Construction",
        "Blocked Road",
        "Normal Road",
        "Unknown"
    ]

    for incident in incidents:
        department = assign_department(incident)

        print(f"{incident} --> {department}")