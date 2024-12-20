import secrets


def PARTICLES_STEP_ERROR() -> int:
    return secrets.choice(range(-10, 11))


def PARTICLES_ANGLE_ERROR() -> float:
    return secrets.choice(range(-10, 11))


def PARTICLES_DIRECTION_ERROR() -> float:
    return secrets.choice(range(-90, 91))
