from sqlalchemy.orm import Session
from insurance_app.models.product import Product
from insurance_app.schemas.product_schema import ProductCreate, ProductUpdate
import uuid

class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_data: ProductCreate) -> Product:
        product = Product(
            id=uuid.uuid4(),
            name=product_data.name,
            type=product_data.type,
            description=product_data.description,
            rate_table=product_data.rate_table,
            status=product_data.status
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_all_products(self):
        return self.db.query(Product).all()

    def get_product_by_id(self, product_id: uuid.UUID):
        return self.db.query(Product).filter(Product.id == product_id).first()

    def update_product(self, product_id: uuid.UUID, product_data: ProductUpdate):
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        for field, value in product_data.dict(exclude_unset=True).items():
            setattr(product, field, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: uuid.UUID):
        product = self.get_product_by_id(product_id)
        if product:
            self.db.delete(product)
            self.db.commit()



