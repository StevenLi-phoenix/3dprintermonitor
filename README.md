# 3D Printer Monitor

## Description
This project is a 3D printer monitor that allows you to monitor the status of multiple 3D printers. It is built using Python and FastAPI for the backend, and HTML, CSS, and JavaScript for the frontend.

## Features
- Monitor multiple 3D printers
- Fetch printer status
- Fetch print job details
- Fetch system details
- Fetch print job history

## Installation
1. Clone the repository to your local machine.
2. Install the required Python packages using pip: `pip install -r requirements.txt`
3. Run the main.py file: `python main.py`

## Usage
1. Open your web browser and navigate to `localhost:8000`.
2. You will see the status of all connected 3D printers.
3. You can click on the "Details" button of each printer to view more information about the print job, system, and history.

## Files
- `main.py`: This is the main file that runs the FastAPI server.
- `scan.py`: This file is used to scan the network for 3D printers.
- `config.py`: This file contains the configuration settings for the project.
- `index.html`: This is the main webpage that displays the status of all connected 3D printers.
- `printer.html`: This webpage displays detailed information about a specific printer.
