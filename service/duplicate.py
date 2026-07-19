import numpy as np
from geopy.distance import geodesic

from service.embedding import (
    generate_embedding,
    string_to_embedding
)


SIMILARITY_THRESHOLD = 0.90
DISTANCE_THRESHOLD = 50   # meters


def cosine_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors.
    """

    return np.dot(vec1, vec2)


def find_duplicate(
    summary: str,
    latitude: float,
    longitude: float,
    incident_type: str,
    existing_reports: list
):
    """
    Returns:
    (True, report) if duplicate found

    (False, None) otherwise
    """

    new_embedding = generate_embedding(summary)

    for report in existing_reports:

        if report.embedding is None:
            continue

        if report.incident_type != incident_type:
            continue

        old_embedding = string_to_embedding(
            report.embedding
        )

        similarity = cosine_similarity(
            new_embedding,
            old_embedding
        )

        distance = geodesic(
            (latitude, longitude),
            (report.latitude, report.longitude)
        ).meters

        if (
            similarity >= SIMILARITY_THRESHOLD
            and distance <= DISTANCE_THRESHOLD
        ):

            return True, report

    return False, None