from faker import Faker

from src.api.models.conduit.article_model import ArticleModel
from src.api.models.conduit.user_model import ConduitUserModel
from src.api.models.petstore.order_model import OrderModel, OrderStatus
from src.api.models.petstore.pet_model import PetModel
from src.api.models.petstore.user_model import PetUserModel


fake = Faker()


# --- Swagger Petstore ---

def generate_petstore_user() -> PetUserModel:

    return PetUserModel(
        username=fake.user_name(),
        email=fake.email(),
        password=fake.password(length=10),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        phone=fake.phone_number()
    )


def generate_petstore_pet() -> PetModel:

    return PetModel(
        id=fake.random_int(min=100000, max=999999),
        name=fake.first_name(),
        status='available',
        photo_urls=[fake.image_url()]
    )


def generate_petstore_order(pet_id: int, quantity: int = 1, status: str = OrderStatus.PLACED) -> OrderModel:
    return OrderModel(
        id=fake.random_int(min=1, max=1000),
        pet_id=pet_id,
        quantity=quantity,
        status=status,
        complete=False
    )


# ---  Conduit (RealWorld App)  ---

def generate_conduit_user() -> dict:
    user = ConduitUserModel(
        username=fake.user_name(),
        email=fake.email(),
        password=fake.password()
    )
    user_data = user.model_dump(by_alias=True)
    return {"user": user_data}


def generate_article_data():
    article = ArticleModel(
        title=fake.sentence(),
        description=fake.paragraph(),
        body=fake.text(),
        tagList=[fake.word(), fake.word()]
    )
    return {"article": article.model_dump(by_alias=True)}
