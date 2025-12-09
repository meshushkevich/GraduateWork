import hashlib
import platform
import uuid


def get_machine_fingerprint():
    raw = (
        platform.node()
        + platform.machine()
        + platform.processor()
        + str(uuid.getnode())
    )
    return hashlib.sha256(raw.encode()).hexdigest()
