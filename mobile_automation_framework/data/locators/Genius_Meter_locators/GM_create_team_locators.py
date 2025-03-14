from appium.webdriver.common.appiumby import AppiumBy

class GMCreateTeamLocators:
    ANDROID = {
        "GM_PAGE": {
            "screen_title":(AppiumBy.ID, "com.gapinternational.genius.qa:id/title"),
            "back_button":(AppiumBy.ID, ""),
            "legend_icon": (AppiumBy.ID, "com.gapinternational.genius.qa:id/secondEndActionImageView"),
            "team_name_field": (AppiumBy.ID, ""),
            "project_name_field": (AppiumBy.ID, ""),
            "outcome_field": (AppiumBy.ID, ""),
            "submit_btn": (AppiumBy.ID, ""),
            "cancel_btn": (AppiumBy.ID, ""),
        }
    }

    IOS = {
        "GM_PAGE": {
            "screen_title":(AppiumBy.IOS_PREDICATE, 'label == "Create a Team"'),
            "back_button":(AppiumBy.ACCESSIBILITY_ID, "Genius Meter"),
            "legend_icon":(AppiumBy.IOS_PREDICATE, '"label == "?" AND name == "?" AND value == "?"'),
            "team_name_field": (AppiumBy.ACCESSIBILITY_ID, "Enter team name…"),
            "project_name_field": (AppiumBy.ACCESSIBILITY_ID, "Enter project name…"),
            "outcome_field": (AppiumBy.ACCESSIBILITY_ID, "Enter outcome…"),
            "submit_btn": (AppiumBy.XPATH, '//XCUIElementTypeButton[@name="Submit"]'),
            "cancel_btn": (AppiumBy.XPATH, '//XCUIElementTypeButton[@name="Cancel"]')
        }
    }

    @staticmethod
    def get_locators(page_name, platform):
        locators = getattr(GMCreateTeamLocators, platform.upper(), None)
        if locators is None:
            raise ValueError(f"❌ Unsupported platform: {platform}")

        page_locators = locators.get(page_name, None)
        if page_locators is None:
            raise ValueError(f"❌ No locators found for page: {page_name} on platform: {platform}")

        return page_locators

