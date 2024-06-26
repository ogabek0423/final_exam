from fastapi import APIRouter
from database import Session, ENGINE
from schemas import *
from db_models import *
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT


session = Session(bind=ENGINE)
blog_router = APIRouter(prefix="/blogs")


@blog_router.get('/')
async def get_blogs( Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        blogs = session.query(Blog).all()
        context = [
            {
                "id": blog.id,
                "user": {
                    "id": blog.user.id,
                    "first_name": blog.user.first_name,
                    "last_name": blog.user.last_name,
                    "email": blog.user.email,


                },
                "text": blog.text,
                "time": blog.created_time
            }
            for blog in blogs
        ]

        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@blog_router.get('/{id}')
async def get_one(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_active:
        blog = session.query(Blog).filter(Blog.id == id).first()
        context = [
            {
                "blog_id": blog.id,
                "user": {
                    "id": blog.user.id,
                    "first_name": blog.user.first_name,
                    "last_name": blog.user.last_name,
                    "email": blog.user.email,

                },
                "text": blog.text,
                "time": blog.created_time
            }

        ]

        return jsonable_encoder(context)
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')


@blog_router.post('/create')
async def create(blog: BlogBase, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        adr_check = session.query(Blog).filter(Blog.id == blog.id).first()
        if adr_check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="blog is already registered")

        new_adr = Blog(
            id=blog.id,
            text=blog.text,
            user_id=blog.user_id,
            created_time=blog.created_time,
            slug=blog.slug
        )
        session.add(new_adr)
        session.commit()

        return HTTPException(status_code=status.HTTP_201_CREATED, detail="blog has been added")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only admins can create new blog")


@blog_router.put('/{id}')
async def update(id: int, blog: BlogBase, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        adr_check = session.query(Blog).filter(Blog.id == id).first()
        new_id_check = session.query(Blog).filter(Blog.id == blog.id).first()
        user_check = session.query(User).filter(User.id == blog.user_id).first()
        if adr_check:
            if user_check:
                if new_id_check is None:
                    for key, value in blog.dict().items():
                        setattr(adr_check, key, value)
                        session.commit()

                    data = {
                        "code": 200,
                        "message": "blog updated"
                    }
                    return jsonable_encoder(data)
                elif new_id_check.id == adr_check.id:
                    for key, value in blog.dict().items():
                        setattr(adr_check, key, value)
                        session.commit()

                    data = {
                        "code": 200,
                        "message": "blog updated"
                    }
                    return jsonable_encoder(data)
                return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Berilgan id da malumot mavjud!")
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="berilgan blog id mavjud emas!")
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Malumot topilmadi")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Only admins can edit this blog')


@blog_router.delete('/{id}')
async def delete(id: int, Authentiztion: AuthJWT = Depends()):
    try:
        Authentiztion.jwt_required()

    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='unauthorized')

    check_user_token = Authentiztion.get_jwt_subject()
    check_user = session.query(User).filter(User.username == check_user_token).first()
    if check_user.is_superuser:
        item = session.query(Blog).filter(Blog.id == id).first()
        if item:
            session.delete(item)
            session.commit()
            return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Deleted")

        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Malumot topilmadi")
    return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Only admins can delete this blog")
