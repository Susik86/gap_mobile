from appium.webdriver.common.appiumby import AppiumBy

class DashboardLocators:
    ANDROID = {
        "DASHBOARD_PAGE": {
            "title":(AppiumBy.ID, "com.gapinternational.genius.qa:id/swipeForGeniusTextView"),
            "sub_title":(AppiumBy.ID, "com.gapinternational.genius.qa:id/subtitle"),  # ✅ Fixed ID
            "dashboard_tab_btn":(AppiumBy.ID, "com.gapinternational.genius.qa:id/dashboard"),
            "accomplishments_tab_btn":(AppiumBy.ID, "com.gapinternational.genius.qa:id/accomplishments"),
            "maxioms_tab_btn":(AppiumBy.ID, "com.gapinternational.genius.qa:id/maxioms"),
            "outcomes_tab_btn":(AppiumBy.ID, "com.gapinternational.genius.qa:id/outcomes"),
            "gm_tab_btn":(AppiumBy.ID, "com.gapinternational.genius.qa:id/group"),
            "menu_tab_btn":(AppiumBy.ID, "com.gapinternational.genius.qa:id/menu"),
        }
    }

    IOS = {
        "DASHBOARD_PAGE": {
            "title":(AppiumBy.ACCESSIBILITY_ID, "Swipe for Genius"),
            "sub_title":(AppiumBy.ACCESSIBILITY_ID, "Where can you apply this Genius thinking today?"),
            "dashboard_tab_btn":(AppiumBy.ACCESSIBILITY_ID, "dashboard icon"),
            "accomplishments_tab_btn":(AppiumBy.ACCESSIBILITY_ID, "accomplishments icon"),
            "maxioms_tab_btn":(AppiumBy.ACCESSIBILITY_ID, "maxioms icon"),
            "outcomes_tab_btn":(AppiumBy.ACCESSIBILITY_ID, "outcomes icon"),
            "gm_tab_btn":(AppiumBy.IOS_PREDICATE, 'label == "icon genius meter"'),  # ✅ Fixed locator strategy
            "menu_tab_btn":(AppiumBy.ACCESSIBILITY_ID, "menu icon"),
        }
    }


    @staticmethod
    def get_locators(page_name, platform):
        """Retrieve locators for a given page and platform."""
        if not isinstance(platform, str):
            raise ValueError("❌ Platform must be a string (either 'android' or 'ios').")

        platform_key = platform.upper()
        if platform_key not in ["ANDROID", "IOS"]:
            raise ValueError(f"❌ Unsupported platform: {platform}. Use 'android' or 'ios'.")

        locators = getattr(DashboardLocators, platform_key, None)
        if not locators:
            raise ValueError(f"❌ No locators found for platform: {platform}")

        page_locators = locators.get(page_name)
        if not page_locators:
            raise ValueError(f"❌ No locators found for page: {page_name} on platform: {platform}")

        return page_locators
