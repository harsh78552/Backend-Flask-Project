import uuid


def generate_id():
    data = int(str(uuid.uuid4().int)[:4])
    return data
