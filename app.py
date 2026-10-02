import time
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class IndustrialWorkflowEngine:
    def __init__(self, tolerance_limit: float = 100.0):
        self.tolerance_limit = tolerance_limit

    def parse_sensor_payload(self, raw_payload: str) -> dict:

        try:
            data = json.loads(raw_payload)
            logging.info(f"Successfully parsed payload for Device ID: {data.get('device_id')}")
            return data
        except json.JSONDecodeError as e:
            logging.error(f"Data ingestion parsing error: {str(e)}")
            return {}

    def validate_parameters(self, parsed_data: dict) -> bool:
        if not parsed_data:
            return False
        
        temperature = parsed_data.get("temperature", 0.0)
        pressure = parsed_data.get("pressure", 0.0)

        if temperature > self.tolerance_limit or pressure > self.tolerance_limit:
            logging.warning(f"Parameter anomaly detected! Temp: {temperature}, Pressure: {pressure}")
            return False
        
        logging.info("Parameters within safe operational limits.")
        return True

if __name__ == "__main__":
    engine = IndustrialWorkflowEngine(tolerance_limit=85.0)
    sample_payload = '{"device_id": "DEV_404", "temperature": 78.5, "pressure": 42.1}'
    parsed_result = engine.parse_sensor_payload(sample_payload)
    
    if engine.validate_parameters(parsed_result):
        print("Data Ingestion Pipeline Executed Smoothly!")
    else:
        print("Automated Error Triggered: Pipeline Paused.")
