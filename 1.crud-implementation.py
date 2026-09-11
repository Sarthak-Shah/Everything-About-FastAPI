from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

# Data Structure Definition
class Tea(BaseModel):
    id: int
    name: str
    origin: str

teas: List[Tea] = []

# Decorators gives super powers to the functions
# / -> Welcome message

@app.get("/")
def read_root():
    return {"message": "Welcome to the Tea House !"}

@app.get("/teas")
def get_teas():
    return teas

@app.post("/teas")
def add_tea(new_tea: Tea):
    teas.append(new_tea)
    return {"message": "Tea added successfully!"}

@app.put("/teas/{tea_id}")
def update_tea(tea_id: int, updated_tea: Tea):
    for index, tea in enumerate(teas):
        if tea.id == tea_id:
            teas[index] = updated_tea
            return {"message": "Tea updated successfully!"}
    return {"message": "Tea not found!"}

@app.delete("/teas/{tea_id}")
def delete_tea(tea_id: int):
    for index, tea in enumerate(teas):
        if tea.id == tea_id:
            del teas[index]
            return {"message": "Tea deleted successfully!"}
    return {"message": "Tea not found!"}


# This block ensures the server only runs if the script is executed directly
if __name__ == "__main__":
    uvicorn.run(":app", host="127.0.0.1", port=8000, reload=True)
