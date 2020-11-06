import uuid


def response_id():
    random = uuid.uuid1()
    rid = random.hex
    return rid
