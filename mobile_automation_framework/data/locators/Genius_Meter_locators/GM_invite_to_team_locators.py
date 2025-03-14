from appium.webdriver.common.appiumby import AppiumBy

class GMInviteToTeamTeamLocators:
    ANDROID = {
        "GM_PAGE": {
            "screen_title":(AppiumBy.ID, "com.gapinternational.genius.qa:id/title"),
            "back_button":(AppiumBy.ID, ""),
            "digit_txt": (AppiumBy.ID, ""),
            "share_invitation": (AppiumBy.ID, ""),
            "add_members_btn":(AppiumBy.ID, ""),
            "done_btn":(AppiumBy.ID, ""),



        }
    }

    IOS = {
        "GM_PAGE": {
            "screen_title":(AppiumBy.IOS_PREDICATE, 'label == "Invite to Team""'),
            "back_button":(AppiumBy.IOS_PREDICATE, 'label == "Create a Team"'),
            "digit_txt": (AppiumBy.ACCESSIBILITY_ID, "This team’s unique  five-digit code"),
            "share_invitation": (AppiumBy.ACCESSIBILITY_ID, "share invitation"),
            "add_members_btn":(AppiumBy.IOS_PREDICATE, 'label == "Add Members" AND name == "Add Members" AND type == "XCUIElementTypeButton"'),
            "done_btn":(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="Done"]')
        }
    }

    @staticmethod
    def get_locators(page_name, platform):
        locators = getattr(GMInviteToTeamTeamLocators, platform.upper(), None)
        if locators is None:
            raise ValueError(f"❌ Unsupported platform: {platform}")

        page_locators = locators.get(page_name, None)
        if page_locators is None:
            raise ValueError(f"❌ No locators found for page: {page_name} on platform: {platform}")

        return page_locators

