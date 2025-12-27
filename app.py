from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import supplier_pydantic, supplier_pydanticIn, Supplier, product_pydantic, product_pydanticIn, Product

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

    
    # serializing an instance of the data
    response = await supplier_pydantic.from_tortoise_orm(supplier_info)

    return {"status": "ok", "data": response}

@app.get('/supplier/{supplier_id}') # specified dynamic value
async def get_specific_supplier(supplier_id: int): # look up type notation in fastapi
    response = await supplier_pydantic.from_queryset_single(Supplier.get(id = supplier_id))

    return {'status': "ok", "data": response}

@app.put('/supplier/{supplier_id}')
async def update_supplier(supplier_id: int, update_info: supplier_pydanticIn):
    supplier = await Supplier.get(id=supplier_id)
    update_info = update_info.dict(exclude_unset=True)
    supplier.name = update_info['name']
    supplier.company = update_info['company']
    supplier.phone = update_info['phone']
    supplier.email = update_info['email']
    await supplier.save()
    # get the updated serialized supplier and then return it
    response = await supplier_pydantic.from_tortoise_orm(supplier)

    return {'status': "ok", "data": response}
    
@app.delete('/supplier/{supplier_id}')
async def delete_supplier(supplier_id:int):
    response = supplier_pydantic.from_queryset_single(Supplier.get(id = supplier_id))
    
    await Supplier.get(id = supplier_id).delete
    
    return {'status': "ok", "message" : "deleted: {response}"  }

@app.get('/product')
async def get_all_products():
    response = await product_pydantic.from_queryset() 

    return {"status": "ok", "data": response}

@app.post('/product')
async def add_product(product_info : product_pydanticIn):
    # we gotta tell the product class to create it. SO creating an class instance
    product_obj = await Product.create(**product_info.dict(exclude_unset=True))

    response = await product_pydantic.from_tortoise_orm(supplier_info)


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