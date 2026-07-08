# ============================================
# 🤖 AI OPTIMIZATION ENGINE (Member 2)
# Compatible with 20-Train Simulation
# ============================================

# ---------- CONFIGURATION ----------
SAFE_DISTANCE = 15     # km
MAX_SPEED = 120        # km/h
MIN_SPEED = 40         # km/h
SPEED_ADJUSTMENT = 15  # km/h

# ---------- MAINTAIN SAFE HEADWAY ----------
def maintain_headway(train_data):

    # Initialize recommended speed
    for train in train_data:
        train["recommended_speed"] = train["speed"]

    # Sort by position (important for 20 trains)
    train_data = sorted(train_data, key=lambda x: x["position"])

    for i in range(1, len(train_data)):

        distance = train_data[i]["position"] - train_data[i - 1]["position"]

        # If too close → reduce speed proportionally
        if distance < SAFE_DISTANCE:

            reduction_factor = (SAFE_DISTANCE - distance) * 1.2

            train_data[i]["recommended_speed"] = max(
                train_data[i]["recommended_speed"] - reduction_factor,
                MIN_SPEED
            )

    return train_data


# ---------- DELAY OPTIMIZATION ----------
def optimize_delay(train_data):

    for train in train_data:

        # Bigger delay → stronger speed boost
        delay_boost = train["delay"] * 0.8

        train["recommended_speed"] = min(
            train["recommended_speed"] + delay_boost,
            MAX_SPEED
        )

    return train_data


# ---------- THROUGHPUT CALCULATION ----------
def calculate_throughput(train_data):

    avg_speed = sum(t["recommended_speed"] for t in train_data) / len(train_data)

    throughput = (avg_speed / SAFE_DISTANCE) * len(train_data)

    return round(throughput, 2)


# ---------- AVERAGE DELAY ----------
def calculate_average_delay(train_data):

    total_delay = sum(t["delay"] for t in train_data)

    return round(total_delay / len(train_data), 2)


# ---------- CONGESTION DETECTION ----------
def detect_congestion(train_data):

    congestion_count = 0

    train_data = sorted(train_data, key=lambda x: x["position"])

    for i in range(1, len(train_data)):
        distance = train_data[i]["position"] - train_data[i - 1]["position"]

        if distance < SAFE_DISTANCE:
            congestion_count += 1

    return congestion_count


# ---------- MAIN AI OPTIMIZATION ----------
def ai_optimization(train_data):

    train_data = maintain_headway(train_data)
    train_data = optimize_delay(train_data)

    throughput = calculate_throughput(train_data)
    avg_delay = calculate_average_delay(train_data)
    congestion = detect_congestion(train_data)

    return {
        "optimized_trains": train_data,
        "throughput": throughput,
        "average_delay": avg_delay,
        "congestion_points": congestion
    }


# ---------- TRADITIONAL SYSTEM ----------
def traditional_performance(train_data):

    return {
        "throughput": len(train_data),
        "average_delay": 15
    }


# ---------- TEST MODE ----------
if __name__ == "__main__":

    print("🤖 Running AI Optimization Test with 20 Trains...\n")

    # Example dummy 20-train data
    sample_data = [
        {"id": i+1, "position": i*12, "speed": 80 + (i % 5)*5, "delay": i % 3}
        for i in range(20)
    ]

    ai_result = ai_optimization(sample_data)
    traditional_result = traditional_performance(sample_data)

    print("===== TRADITIONAL SYSTEM =====")
    print("Throughput:", traditional_result["throughput"])
    print("Average Delay:", traditional_result["average_delay"])

    print("\n===== AI OPTIMIZED SYSTEM =====")
    print("Throughput:", ai_result["throughput"])
    print("Average Delay:", ai_result["average_delay"])
    print("Congestion Points:", ai_result["congestion_points"])

    print("\nOptimized Train Recommendations (First 5 shown):")
    for train in ai_result["optimized_trains"][:5]:
        print(
            f"Train {train['id']} | "
            f"Pos: {round(train['position'],2)} km | "
            f"Orig: {train['speed']} | "
            f"Rec: {round(train['recommended_speed'],2)} | "
            f"Delay: {train['delay']}"
        )

    print("\n✅ Optimization Complete")
