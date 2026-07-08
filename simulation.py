# ============================================
# 🚆 SIMULATION ENGINE (Member 1)
# ============================================

import random

# ---------- CONFIGURATION ----------
SECTION_LENGTH = 300   # km
NUM_TRAINS = 20
TIME_STEP = 1          # minute
SAFE_DISTANCE = 15     # km

# ---------- INITIALIZE TRAINS ----------
def initialize_trains():

    trains = []

    base_position = 0

    for i in range(NUM_TRAINS):

        trains.append({
            "id": i + 1,
            "position": base_position - (i * 12),   # spaced initially
            "speed": random.randint(70, 110),
            "delay": 0
        })

    return trains


# ---------- MOVE TRAINS ----------
def move_trains(trains):
    for train in trains:
        distance = train["speed"] * (TIME_STEP / 60)
        train["position"] += distance
    return trains


# ---------- SAFETY RULE ----------
def safety_rule(trains):

    trains = sorted(trains, key=lambda x: x["position"])

    for i in range(1, len(trains)):
        gap = trains[i]["position"] - trains[i - 1]["position"]

        if gap < SAFE_DISTANCE:
            trains[i]["speed"] = max(50, trains[i]["speed"] - 10)
            trains[i]["delay"] += 1

    return trains


# ---------- RANDOM DELAY ----------
def random_delay(trains):
    for train in trains:
        if random.random() < 0.15:   # 15% chance
            train["delay"] += random.randint(1, 3)
            train["speed"] = max(50, train["speed"] - 10)
    return trains


# ---------- MAIN SIMULATION ----------
def run_simulation(simulation_time=15):

    trains = initialize_trains()

    for _ in range(simulation_time):
        trains = move_trains(trains)
        trains = safety_rule(trains)
        trains = random_delay(trains)

    return trains


# ---------- TEST MODE ----------
if __name__ == "__main__":

    print("🚆 Running Train Simulation with 20 Trains...\n")

    result = run_simulation()

    for train in result:
        print(
            f"Train {train['id']} | "
            f"Position: {round(train['position'],2)} km | "
            f"Speed: {train['speed']} km/h | "
            f"Delay: {train['delay']} min"
        )

    print("\n✅ Simulation Complete")
