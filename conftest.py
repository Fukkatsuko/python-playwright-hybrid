import allure
import pytest
import requests

from src.config.base_settings import settings
from src.api.clients.petstore.pet_client import PetClient
from src.api.clients.petstore.store_client import OrderClient
from src.api.clients.petstore.user_client import UserClient
from src.api.clients.conduit.conduit_client import ConduitClient
from playwright.sync_api import Page, expect
from src.config.env import settings
from src.ui.pages.article_creation_page import ArticleCreationPage
from src.ui.pages.article_page import ArticlePage
from src.ui.pages.login_page import LoginPage
from src.ui.pages.main_page import MainPage
from src.ui.pages.profile_page import ProfilePage
from src.ui.pages.register_page import RegisterPage
from src.ui.pages.settings_page import SettingsPage
from utils.generators import generate_conduit_user, generate_article_data


# --- Petstore. Sessions---
@pytest.fixture(scope="session")
def auth_session():
    s = requests.Session()
    s.headers.update({"api_key": settings.petstore_api_key})
    return s


@pytest.fixture(scope="session")
def un_auth_session():
    return requests.Session()


# --- Petstore. Clients ---

def _build_pet_api(session):
    client = PetClient(base_url=settings.petstore_api_url)
    client.session = session
    return client


def _build_order_api(session):
    client = OrderClient(base_url=settings.petstore_api_url)
    client.session = session
    return client


def _build_user_api(session):
    client = UserClient(base_url=settings.petstore_api_url)
    client.session = session
    return client


# --- Petstore. Fixtures suppliers ---

@pytest.fixture(scope="session")
def pet_api(auth_session):
    return _build_pet_api(auth_session)


@pytest.fixture(scope="session")
def un_auth_pet_api(un_auth_session):
    return _build_pet_api(un_auth_session)


@pytest.fixture(scope="session")
def order_api(auth_session):
    return _build_order_api(auth_session)


@pytest.fixture(scope="session")
def un_auth_order_api(un_auth_session):
    return _build_order_api(un_auth_session)


@pytest.fixture(scope="session")
def user_api(auth_session):
    return _build_user_api(auth_session)


# --- CONDUIT ---
# --- Conduit. API FIXTURE ---

@pytest.fixture(scope="session")
def conduit_auth_session():
    session = requests.Session()
    temp_client = ConduitClient(base_url=settings.conduit_api_url)
    temp_client.session = session

    response = temp_client.users.login(settings.user_email, settings.user_password)

    if response.status_code == 200:
        token = response.json()["user"]["token"]
        session.headers.update({"Authorization": f"Token {token}"})

    return session


@pytest.fixture(scope="session")
def conduit_api(conduit_auth_session):
    client = ConduitClient(base_url=settings.conduit_api_url)
    client.session = conduit_auth_session
    return client


# --- Conduit. HYBRID FIXTURE: AUTHORIZED USER ---

@pytest.fixture
def auth_user(page: Page, conduit_api):
    from src.api.clients.conduit.conduit_client import ConduitClient
    clean_client = ConduitClient(base_url=settings.conduit_api_url)

    with allure.step("Precondition: Registering a new user via API"):
        user_data = generate_conduit_user()
        response = clean_client.users.register_user(user_data)

        if response.status_code != 201:
            raise Exception(f"Reg failed: {response.text}")

        token = response.json()["user"]["token"]

    with allure.step("UI: Forwarding the token to the browser"):
        page.goto("/")
        page.evaluate(f"window.localStorage.setItem('jwtToken', '{token}')")
        page.reload()

        expect(page.get_by_role("link", name="Sign in")).not_to_be_visible(timeout=10000)

        conduit_api.session.headers.update({"Authorization": f"Token {token}"})

    return user_data["user"]


@pytest.fixture
def api_article(auth_user, conduit_api):

    article_data = generate_article_data()
    response = conduit_api.articles.create_article(article_data)

    if response.status_code != 201:
        raise Exception(f"Failed to create article! Status: {response.status_code}, Text: {response.text}")

    article = response.json()["article"]
    yield article

    conduit_api.articles.delete_article(article["slug"])


# --- Conduit. Preparation for article creation ---

@pytest.fixture
def editor_page(auth_user, article_creation_page):

    article_creation_page.visit("/editor")
    expect(article_creation_page.title_field).to_be_visible(timeout=10000)
    return article_creation_page


# --- BROWSER SETTINGS ---

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "base_url": settings.conduit_ui_url,
        "viewport": {"width": 1280, "height": 720},
    }


# --- Conduit. Fixtures of pages (Page Objects) ---

@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)


@pytest.fixture
def register_page(page: Page):
    return RegisterPage(page)


@pytest.fixture
def main_page(page: Page):
    return MainPage(page)


@pytest.fixture
def settings_page(page: Page):
    return SettingsPage(page)


@pytest.fixture
def profile_page(page: Page):
    return ProfilePage(page)


@pytest.fixture
def article_page(page: Page):
    return ArticlePage(page)


@pytest.fixture
def article_creation_page(page: Page):
    return ArticleCreationPage(page)
