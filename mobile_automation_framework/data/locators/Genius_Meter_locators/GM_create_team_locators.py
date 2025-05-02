from appium.webdriver.common.appiumby import AppiumBy

class GMCreateTeamLocators:
    ANDROID = {
        "GM_CREATE_TEAM_PAGE": {
            "screen_title":(AppiumBy.XPATH, "//*[@text='Create a Team']"),
            "back_button":(AppiumBy.XPATH, "//android.widget.ImageView[@resource-id='com.gapinternational.genius.qa:id/startActionImage']"),
            "legend_icon": (AppiumBy.ID, "com.gapinternational.genius.qa:id/secondEndActionImageView"),
            "team_name_field": (AppiumBy.ID, "com.gapinternational.genius.qa:id/groupNameEditText"),
            "project_name_field": (AppiumBy.ID, "com.gapinternational.genius.qa:id/projectNameEditText"),
            "outcome_field": (AppiumBy.ID, "com.gapinternational.genius.qa:id/outcomeEditText"),
            "submit_btn": (AppiumBy.ID, "com.gapinternational.genius.qa:id/submitButton"),
            "cancel_btn": (AppiumBy.ID, "com.gapinternational.genius.qa:id/cancelButton"),
        }
    }

    IOS = {
        "GM_CREATE_TEAM_PAGE": {
            "screen_title":(AppiumBy.IOS_PREDICATE, 'label == "Create a Team"'),
            "back_button":(AppiumBy.ACCESSIBILITY_ID, "Genius Meter"),
            # "legend_icon":(AppiumBy.IOS_PREDICATE, '"label == "?" AND name == "?" AND value == "?"'),
            "team_name_field": (AppiumBy.ACCESSIBILITY_ID, "Team Name"),
            "project_name_field": (AppiumBy.ACCESSIBILITY_ID, "Project Name"),
            "outcome_field": (AppiumBy.XPATH, '//XCUIElementTypeTextView[@name="Outcome"]'),
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

