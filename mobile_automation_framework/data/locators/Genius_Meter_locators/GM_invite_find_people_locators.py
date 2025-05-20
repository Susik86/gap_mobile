from appium.webdriver.common.appiumby import AppiumBy

class GMInviteFindPeopleLocators:
    ANDROID = {
        "GM_PAGE": {
            "screen_title":(AppiumBy.XPATH, "//*[@text='Invite to Team']"),
            "back_button":(AppiumBy.XPATH, "//android.widget.ImageView[@resource-id='com.gapinternational.genius.qa:id/startActionImage']"),
            "search_field": (AppiumBy.ID, ""),
            "invite_button": (AppiumBy.ID, ""),


        }
    }

    IOS = {
        "GM_PAGE": {
            "screen_title":(AppiumBy.IOS_PREDICATE, 'label == "Invite to Team""'),
            "back_button":(AppiumBy.IOS_PREDICATE, 'label == "Create a Team"'),
            "search_field": (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeSearchField[`label == "Search"`][2]'),
            "invite_button": (AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="Invite"]'),

        }
    }

    @staticmethod
    def get_locators(page_name, platform):
        locators = getattr(GMInviteFindPeopleLocators, platform.upper(), None)
        if locators is None:
            raise ValueError(f"❌ Unsupported platform: {platform}")

        page_locators = locators.get(page_name, None)
        if page_locators is None:
            raise ValueError(f"❌ No locators found for page: {page_name} on platform: {platform}")

        return page_locators

