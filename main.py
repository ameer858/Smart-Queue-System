from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Security settings to allow the website to communicate with Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core Data Structures
queue = []
current_serving = {"token": 0, "name": "None"}

@app.get("/status")
def get_status():
    return {
        "serving_token": current_serving["token"],
        "serving_name": current_serving["name"],
        "waiting_count": len(queue)
    }

@app.get("/get-token")
def get_token(name: str):
    token_number = len(queue) + 1 if current_serving["token"] == 0 else len(queue) + current_serving["token"] + 1
    new_entry = {"token": token_number, "name": name}
    queue.append(new_entry)
    return {"message": f"Token {token_number} issued to {name}", "token": token_number}

@app.get("/next")
def call_next():
    global current_serving
    if queue:
        current_serving = queue.pop(0)
        return {"message": f"Now serving {current_serving['name']}", "token": current_serving["token"]}
    return {"message": "No one in line", "token": 0}