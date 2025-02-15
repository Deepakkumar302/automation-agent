import requests
from fastapi import FastAPI, HTTPException
import os
from functions import *
import subprocess
import os
from dotenv import load_dotenv
import os

load_dotenv()  # Load .env variables
AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")

if not AIPROXY_TOKEN:
    raise RuntimeError("AIPROXY_TOKEN is missing. Check your .env file!")


app = FastAPI()
### /run and /read
# @app.get("/read")
# async def read_file(path: str):
#         if not path.startswith("/data"):
#              raise HTTPException(status_code = 403, detail = "Access to file is not allowed")
#         if not os.path.exists(path):
#              raise HTTPException(status_code = 404 , detail = "File is not found")
#         file = open(path, "r")
#         content = file.read()
#         return {"content": content}
    
import traceback

@app.post("/run")
async def run_task(task: str):
    try:
        print(f"Received task: {task}")  # Debugging
        task_output = get_task_output(AIPROXY_TOKEN, task)
        
        task_lower = task.lower()
        days = {"monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6}

        if "count" in task_lower:
            for day in days:
                if day in task_lower:
                    day = extract_dayname(task_lower)
                    count_days(day)
        elif "install" in task_lower:
            pkgname = extract_package(task_lower)
            correct_package = get_correct_pkgname(pkgname)
            if pkgname:
                print(f"Installing package: {correct_package}")  # Debugging
                subprocess.run(["pip", "install", correct_package], check=True)
        else:
            return {"status": "Task is recognized but not implemented yet"}
        
        return {"status": "success", "task_output": task_output}
    
    except Exception as e:
        error_message = str(e)
        print("ERROR: ", error_message)
        print(traceback.format_exc())  # Full stack trace
        raise HTTPException(status_code=500, detail=error_message)


import os

# Use a local directory instead of "/data"
DATA_DIR = os.path.join(os.getcwd(), "data")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

@app.get("/read")
async def read_file(path: str):
    full_path = os.path.join(DATA_DIR, os.path.basename(path))  # Ensure safe access
    
    if not os.path.exists(full_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(full_path, "r") as file:
        content = file.read()
    
    return {"content": content}
DATA_DIR = os.path.join(os.getcwd(), "data")
file_path = os.path.join(DATA_DIR, "dates-wednesdays.txt")

print("Checking if file exists:", os.path.exists(file_path))
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        print(f"File content:\n{f.read()}")
import datetime

DATA_DIR = "data"
input_file = f"{DATA_DIR}/dates.txt"
output_file = f"{DATA_DIR}/dates-wednesdays.txt"

try:
    with open(input_file, "r") as f:
        dates = [line.strip() for line in f.readlines()]

    wednesday_count = 0
    for date in dates:
        try:
            parsed_date = datetime.datetime.strptime(date, "%B %d, %Y")  # Correct format
            if parsed_date.weekday() == 2:  # Wednesday = 2
                wednesday_count += 1
        except ValueError as ve:
            print(f"Skipping invalid date: {date} - {ve}")

    with open(output_file, "w") as f:
        f.write(str(wednesday_count))

    print(f"✅ Successfully counted Wednesdays: {wednesday_count}")
except Exception as e:
    print(f"❌ Error: {e}")
print("Using AI Proxy Token:", AIPROXY_TOKEN)
