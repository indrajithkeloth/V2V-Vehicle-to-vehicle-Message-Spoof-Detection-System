import random

def generate_message():
    vehicle_ids = ["V1", "V2", "X999"]
    vid = random.choice(vehicle_ids)
    speed = random.randint(40, 300)
    location = (random.uniform(10, 11), random.uniform(76, 77))
    return {"vehicle_id": vid, "speed": speed, "location": location}
