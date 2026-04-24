from playwright.sync_api import Page

from src.ui.pages.base_page import BasePage


class ProfilePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.empty_feed_message = self.page.get_by_text("No articles are here... yet.")
