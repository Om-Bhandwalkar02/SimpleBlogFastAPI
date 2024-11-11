from fastapi import FastAPI, Depends, status, Response, HTTPException
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from hashing import Hash
import schemas
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=['blogs'])
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog", response_model=List[schemas.Blog], tags=['blogs'])
async def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get("/blog/{blog_id}", status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['blogs'])
async def show_blog(blog_id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).get(blog_id)
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': 'Blog does not exist'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

@app.delete("/blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['blogs'])
async def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return None  # Explicitly return None for a 204 No Content response

@app.put("/blog/{blog_id}", status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
async def update_blog(blog_id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")

    blog.title = request.title
    blog.body = request.body
    db.commit()
    db.refresh(blog)

    return {"message": "Blog updated successfully", "updated_blog": blog}


@app.post('/user', response_model=schemas.ShowUser, tags=['users'])
async def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.get_password_hash(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/user/{user_id}', response_model=schemas.ShowUser, tags=['users'])
async def read_user(user_id:int ,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user