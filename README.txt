
# System Resource Monitor in python.

## Overview
This Python project monitors and displays key OS resource utilization metrics, including CPU times, core utilization percentages, and system information. It provides statistics in a user-friendly tabular format using libraries like `psutil`, `datetime`, `tabulate` and `prettytable`.

## Features
- Monitors and Displays CPU, Memory, Disk, Network and Process information.
- Displays system platform details.
- Outputs data in a structured and visually appealing graphs and tables.

## Requirements
Make sure python is installed on your computer.	
The project uses the following Python libraries:
- psutil: For accessing system resource metrics.
- datetime: For managing timestamps and durations.
- prettytable: For displaying data in tables.
- tabulate: For alternate tabular formatting.

Install the required libraries using:
pip install psutil prettytable tabulate

## How to Run
1. Download the project files.
2. Navigate to the project directory:
   cd <project-directory>
3. Execute the script:
   python ResourceMonitor.py

## Example Usage
When you run the script, it outputs statistics like this:
{CPU times}
USER: 123.45 s    SYSTEM: 67.89 s    IDLE: 234.56 s

{CPU cores utilization percents}
Core 1: 12%
Core 2: 15%
Core 3: 20%
Core 4: 10%


## Project Structure
ResourceMonitor/
├── ResourceMonitor.py   # Main script to run the utility
├── README.txt            # Project documentation


## Modules Used
- psutil: Fetch system metrics like CPU times and utilization.
- datetime: Manage timestamps for recorded metrics.
- prettytable: Display data in tabular format.
- tabulate: For alternate table formatting.

## Future Enhancements
- Include logging capabilities to save resource usage over time.
- Provide a graphical user interface (GUI) for better user interaction.
- Make the data display in realtime.

## Contributions
- Allen Chacko Johny: CPU & Disk Monitoring, Combining Modules, User Interface.
- Tejen Anilbhai Thakkar: Memory & Network Monitoring.
- Dathwik Kollikonda: Process Monitoring & Sensor/System Information, Project Documentation.
