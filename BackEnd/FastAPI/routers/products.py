from fastapi import APIRouter

router = APIRouter(prefix="/products", tags=["Products"])

products_list = [{"Nombre": "Producto 1", "Precio": 100},
                {"Nombre": "Producto 2", "Precio": 200},
                {"Nombre": "Producto 3", "Precio": 300}]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def get_product_by_id(id: int):
    if id < 0 or id >= len(products_list):
        return {"Error": "Producto no encontrado"}
    return products_list[id]
        

