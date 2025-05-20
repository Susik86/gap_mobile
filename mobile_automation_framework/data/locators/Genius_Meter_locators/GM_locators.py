from appium.webdriver.common.appiumby import AppiumBy

class GMLocators:
    ANDROID = {
        "GM_PAGE": {
            "screen_title": (AppiumBy.ID, "com.gapinternational.genius.qa:id/title"),
            "legend_icon": (AppiumBy.ID, "com.gapinternational.genius.qa:id/secondEndActionImageView"),
            "create_team_btn": (AppiumBy.ID, "com.gapinternational.genius.qa:id/createGroupButton"),
            "join_team_btn": (AppiumBy.ID, "com.gapinternational.genius.qa:id/joinGroupButton"),
            "take_genius_pulse_btn": (AppiumBy.ID, "com.gapinternational.genius.qa:id/launchGeniusPulseButton"),
            "close_genius_pulse_btn": (AppiumBy.ID, "com.gapinternational.genius.qa:id/closePulseButton"),


        }
    }

    IOS = {
        "GM_PAGE": {
            "screen_title":(AppiumBy.IOS_PREDICATE, 'label == "Genius Meter"'),
            "legend_icon": (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "?"`]'),
            "create_team_btn":(AppiumBy.IOS_PREDICATE, 'label == "Create a Team" AND name == "Create a Team" AND type == "XCUIElementTypeButton"'),
            "join_team_btn": (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "Join a Team"`]'),


        }
    }

    @staticmethod
    def get_locators(page_name, platform):
        locators = getattr(GMLocators, platform.upper(), None)
        if locators is None:
            raise ValueError(f"❌ Unsupported platform: {platform}")

        page_locators = locators.get(page_name, None)
        if page_locators is None:
            raise ValueError(f"❌ No locators found for page: {page_name} on platform: {platform}")

        return page_locators

