from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

app = FastAPI()

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET = "b3157a92c23fdbaa6d539ceec6560c4d9a64c9c4ad41812e3f55b7bdc607c7e1"

cript = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserInDB(User):
    password: str

users_db = {
    "Mamut": {
        "username" : "Mamut",
        "full_name" : "Antonio Hernandez",
        "email" : "mamut@gmm.com",
        "disabled" : False,
        "password" : "$2a$12$LM9FGjYpdqS31ot1UAg/Gu/WGLMEN7yYh3vBjHGZWnzZcidOEesJu"
    },
    "mgPrueba": {
        "username" : "mgPrueba",
        "full_name" : "Maria Gonzalez",
        "email" : "mgprueba@gmm.com",
        "disabled" : True,
        "password" : "$2a$12$oBsEZD9JzkoJuHCcyURgAutWNfaeXQ3OzGdmPrqd3iargJrDh7PEy"
    },
    "ppPrueba": {
        "username" : "ppPrueba",
        "full_name" : "Pedro Perez",
        "email" : "ppprueba@gmm.com",
        "disabled" : False,
        "password" : "$2a$12$tDg.b4WRfpUnul.sl8hSmedwW.5z48d8cISXiGVnVexGx9V6CfpO."
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserInDB(**users_db[username])
    return None

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    return None

async def auth_user(token: str = Depends(oauth2_scheme)):
    
    exception = HTTPException(status_code=400, detail="Credenciales incorrectas")

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception

    return search_user(username)    


def current_user(user: User  = Depends(auth_user)):
    
    if user.disabled:
        raise HTTPException(status_code=400, detail="Usuario deshabilitado")
    return user

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail="Usuario incorrecto")
    
    user = search_user_db(form.username)

    if not cript.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    
    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)}

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
