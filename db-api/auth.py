from passlib.context import CryptContext
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from models import UserModel, UserCollection, Token
import os
import motor.motor_asyncio
from fastapi import FastAPI, Body, HTTPException, status, Security
from bd import users_collection, get_collection, dietas_collection, mealrec_collection
from bson import ObjectId
from models import DietModel

# Generada con openssl rand -hex 32
SECRET_KEY = "51a93d01e2d95e91826109b07d4cd852dcdd4ad781988f0d8b018bc4bea81fca"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

router = APIRouter()

# Crear un cliente de Motor para MongoDB
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client["tfg"]

def verify_password(plain_password, hashed_password): # Verifica la contraseña
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(email: str):
    user_dict = await users_collection.find_one({"email": email})
    if user_dict:
        # Obtener las dietas completas del usuario
        diet_ids = user_dict.get("diets", [])
        diets = []
        for diet_id in diet_ids:
            diet = await dietas_collection.find_one({"_id": ObjectId(diet_id)})
            if diet:
                # Obtener los detalles de las recetas y sus títulos
                if diet.get("appetizerID"):
                    appetizer = await mealrec_collection.find_one({"_id": ObjectId(diet["appetizerID"])})
                    if appetizer:
                        diet["appetizer_title"] = appetizer.get("title")
                if diet.get("main_dishID"):
                    main_dish = await mealrec_collection.find_one({"_id": ObjectId(diet["main_dishID"])})
                    if main_dish:
                        diet["main_dish_title"] = main_dish.get("title")
                if diet.get("dessertID"):
                    dessert = await mealrec_collection.find_one({"_id": ObjectId(diet["dessertID"])})
                    if dessert:
                        diet["dessert_title"] = dessert.get("title")
                diets.append(DietModel(**diet))

        user_dict["diets"] = diets

    return user_dict

async def create_user(user: UserModel):
    user.password = get_password_hash(user.password)
    await users_collection.insert_one(user.model_dump(by_alias=True))
    print("Usuario creado")

async def authenticate_user(email: str, password: str):
    user_dict = await get_user(email)
    if not user_dict:
        return False
    user = UserModel(**user_dict)
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=UserModel)
async def register_user(user: UserModel):
    db_user = await get_user(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    await create_user(user)
    print("Usuario registrado")
    return user

@router.post("/token", response_model=Token) 
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")  # Devolvemos un objeto Token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_dict = await get_user(email)
    if user_dict is None:
        raise credentials_exception

    return UserModel(**user_dict)

@router.get("/users/me", response_model=UserModel)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify-token")
async def verify_token(current_user: UserModel = Depends(get_current_user)):
    return current_user