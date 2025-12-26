from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import (supplier_pydantic, supplier_pydanticIn, Supplier)

app = FastAPI()

@app.get('/')
def index():
    return {"description": "a fastapi application", "Message:" : "go to /docs to see all endpoints"}

# @app.get("/{full_path:path}")
# async def capture_routes(request: Request, full_path: str):


@app.post('/supplier')
# making it read only so we dont accidently update ID
### gotta learn how to stop it from getting in duplicates
async def add_supplier(supplier_info: supplier_pydanticIn):
    # we gonna create a instance of the data that we gonna supply
    # exclude= True so we exclude the fields that are not provided
    supplier_obj = await Supplier.create(**supplier_info.dict(exclude_unset=True))

    #this is gonna add our supplier to the database
    # serializing an instance of the data
    response = await supplier_pydantic.from_tortoise_orm(supplier_info)

    return {"status": "ok", "data": response}

@app.get('/supplier/{supplier_id}') # specified dynamic value
async def get_specific_supplier(supplier_id: int): # look up type notation in fastapi
    response = await supplier_pydantic.from_queryset_single(Supplier.get(id = supplier_id))

    return {'status': "ok", "data": response}

# we gonna use async here cuz we will have to wait for db
@app.get('/supplier')
async def get_all_suppliers():
    # serializing
    response = await supplier_pydantic.from_queryset(Supplier.all())

    return {"status": "ok", "data": response}



# register models
register_tortoise(
    app,
    db_url="postgres://postgres:admin88@localhost:5432/fastapi",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)