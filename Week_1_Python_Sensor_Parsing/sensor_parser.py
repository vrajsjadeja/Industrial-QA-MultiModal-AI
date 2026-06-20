"""
Week 1: Core Python & Data Parsing
Industrial Application: Parsing manufacturing sensor logs to detect early anomalies.
"""

import random
from datetime import datetime, timedelta

def generate_mock_sensor_data(num_records: int = 50) -> list:
    """Generates mock sensor data representing a manufacturing assembly line."""
    data = []
    base_time = datetime.now()
    
    for i in range(num_records):
        record = {
            "timestamp": (base_time - timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M:%S"),
            "machine_id": f"MACH-{random.randint(100, 105)}",
            "temperature_c": round(random.uniform(60.0, 110.0), 2),
            "vibration_hz": round(random.uniform(10.0, 60.0), 2)
        }
        data.append(record)
    return data

def flag_anomalies(sensor_data: list, temp_threshold: float, vib_threshold: float) -> list:
    """Parses the data and flags any machines exceeding safe operational thresholds."""
    anomalies = []
    
    for reading in sensor_data:
        is_overheating = reading["temperature_c"] > temp_threshold
        is_vibrating = reading["vibration_hz"] > vib_threshold
        
        if is_overheating or is_vibrating:
            reading["anomaly_type"] = []
            if is_overheating:
                reading["anomaly_type"].append("OVERHEATING")
            if is_vibrating:
                reading["anomaly_type"].append("EXCESSIVE_VIBRATION")
            anomalies.append(reading)
            
    return anomalies

def main():
    print("🏭 Industrial QA: Sensor Parsing Module Initialized")
    raw_logs = generate_mock_sensor_data(num_records=100)
    
    MAX_SAFE_TEMP = 95.0
    MAX_SAFE_VIB = 45.0
    
    critical_flags = flag_anomalies(raw_logs, MAX_SAFE_TEMP, MAX_SAFE_VIB)
    
    print("\n⚠️ CRITICAL ALERTS DETECTED ⚠️")
    if not critical_flags:
        print("All systems operating within normal parameters.")
    else:
        for alert in critical_flags[:5]:
            issues = " & ".join(alert["anomaly_type"])
            print(f"[{alert['timestamp']}] {alert['machine_id']} | Issue: {issues} | Temp: {alert['temperature_c']}C")

if __name__ == "__main__":
    main()
