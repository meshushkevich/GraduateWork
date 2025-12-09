# Collector

Collector service for sensor data gathering and transmission.

## Features

- Streamlit dashboard for monitoring MCUs and sensor data
- Support for both real MCUs and imitators
- API connection status indicator
- Real-time sensor data visualization

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the Streamlit dashboard:

```bash
streamlit run main.py
```

## Usage

1. The left sidebar shows all connected MCUs
2. Click on any MCU to view its sensor data
3. Use the "Add New MCU" buttons to add additional MCUs
4. The API connection status indicator shows whether the dashboard can communicate with the backend API
5. Sensor data is automatically collected from imitators and sent to the API (simulated)

## Components

- `main.py`: Main Streamlit application
- `src/collector/imitator/sensor_simulator.py`: Sensor data simulation logic
- `requirements.txt`: Python dependencies

## Architecture

The application uses a modular architecture:
- MCU abstraction layer for both real hardware and simulated devices
- Sensor data simulation for testing
- API integration for data transmission
- Streamlit frontend for visualization
```
