# ============================================
# 🚆 MAIN SYSTEM CONTROLLER
# ============================================

from simulation import run_simulation
from ai_engine import ai_optimization, traditional_performance


def run_system():
    """
    Runs full railway AI system:
    1. Simulation
    2. AI Optimization
    3. Traditional Comparison
    """

    # Step 1: Run Simulation (20 trains)
    simulation_data = run_simulation()

    # Step 2: AI Optimization
    ai_result = ai_optimization(simulation_data)

    # Step 3: Traditional System Performance
    traditional_result = traditional_performance(simulation_data)

    # Step 4: Combine everything
    return {
        "simulation_data": simulation_data,  # optional but useful
        "ai_result": ai_result,
        "traditional_result": traditional_result
    }


# ---------- DIRECT TEST ----------
if __name__ == "__main__":

    result = run_system()

    print("\n===== SYSTEM OUTPUT =====")

    print("\n--- AI SYSTEM ---")
    print("Throughput:", result["ai_result"]["throughput"])
    print("Average Delay:", result["ai_result"]["average_delay"])
    print("Congestion Points:", result["ai_result"]["congestion_points"])

    print("\n--- TRADITIONAL SYSTEM ---")
    print("Throughput:", result["traditional_result"]["throughput"])
    print("Average Delay:", result["traditional_result"]["average_delay"])

    print("\n✅ System Running Successfully")
