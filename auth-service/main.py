from fastapi import FastAPI

app = FastAPI(root_path="/auth")

@app.get("/")
def read_auth():
    return {"message": "Auth service is running"}