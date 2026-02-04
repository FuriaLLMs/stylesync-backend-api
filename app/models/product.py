from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId

class Product(BaseModel):
    """
    Modelo de dados para um Produto.
    """
    # Define o campo id mapeado para o _id do MongoDB
    id: Optional[ObjectId] = Field(None, alias='_id')
    name: str
    sku: str
    price: float
    description: Optional[str] = None
    stock: int

    # Configurações para aceitar ObjectId e usar o alias
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )

class UpdateProduct(BaseModel):
    """
    Modelo para atualização parcial: todos os campos são opcionais.
    """
    name: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class ProductDBModel(Product):
    """
    Classe especializada para serializar o retorno do banco (ObjectId -> str)
    """
    def model_dump(self, **kwargs):
        # Chama o dump original (transforma em dicionário)
        data = super().model_dump(**kwargs)
        
        # Se tiver _id (vinda do alias), converte para string
        if "_id" in data:
            data["_id"] = str(data["_id"])
            
        return data
