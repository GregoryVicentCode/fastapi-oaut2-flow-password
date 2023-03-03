from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer("/token")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "secret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "secret2",
        "disabled": True,
    },
}


@app.get("/")
def root():
    return "Hi I am FastAPI"


@app.get("/users/me")
def user(token: str = Depends(oauth2_scheme)):
    user = fake_users_db.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    return "Has ingresado en esta ruta"


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if not user:
        raise HTTPException(
            status_code=400, detail="Contraseña o Usuario invalido")
    if not form_data.password == user["hashed_password"]:
        raise HTTPException(
            status_code=400, detail="Contraseña o Usuario invalido")
    return {
        "access_token": form_data.username,
        "token_type": "bearer"
    }
