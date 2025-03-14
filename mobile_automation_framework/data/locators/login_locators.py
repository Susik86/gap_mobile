from appium.webdriver.common.appiumby import AppiumBy

class LoginLocators:
    ANDROID = {
        "LOGIN_PAGE": {
            "title":(AppiumBy.ID, ''),
            "sub_title":(AppiumBy.ID, ''),
            "email_field":(AppiumBy.ID, "com.gapinternational.genius.qa:id/emailEditText"),
            "password_field":(AppiumBy.ID, "com.gapinternational.genius.qa:id/passwordEditText"),
            "show_btn":(AppiumBy.ID, ''),
            "reset_your_password_btn":(AppiumBy.ID, ''),
            "login_button":(AppiumBy.ID, "com.gapinternational.genius.qa:id/signInButton"),
            "login_pop_up":(AppiumBy.ID, "android:id/message"),
            "ok_btn":(AppiumBy.ID, "com.gapinternational.genius.qa:id/button1"),
            "email_error":(AppiumBy.ID, "com.gapinternational.genius.qa:id/textinput_helper_text"),
            "password_error":(AppiumBy.ID, ""),
            "bottom_txt":(AppiumBy.NAME, "Don’t have an account? Learn more about Genius"),
        }
    }

    IOS = {
        "LOGIN_PAGE": {
            "title":(AppiumBy.ACCESSIBILITY_ID, 'logo'),
            "sub_title":(AppiumBy.ACCESSIBILITY_ID, 'Sign in with your company email'),
            "email_field":(AppiumBy.IOS_PREDICATE, 'value == "Email"'),
            "password_field":(AppiumBy.IOS_PREDICATE, 'value == "Password"'),
            "show_btn":(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="Show"]'),
            "reset_your_password_btn":(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="Reset your password"]'),
            "login_button":(AppiumBy.IOS_PREDICATE, 'value == "Sign In"'),
            "login_pop_up":(AppiumBy.IOS_PREDICATE, 'type == "XCUIElementTypeAlert"'),
            "ok_btn":(AppiumBy.ACCESSIBILITY_ID, "signInButton"),
            "email_error": (AppiumBy.IOS_PREDICATE, "type == 'XCUIElementTypeStaticText' AND value CONTAINS 'Enter your company email'"),
            "password_error": (AppiumBy.IOS_PREDICATE, "type == 'XCUIElementTypeStaticText' AND value CONTAINS 'Enter your password'"),
            "bottom_txt":(AppiumBy.NAME, "Don’t have an account? Learn more about Genius"),
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

        locators = getattr(LoginLocators, platform_key, None)
        if not locators:
            raise ValueError(f"❌ No locators found for platform: {platform}")

        page_locators = locators.get(page_name)
        if not page_locators:
            raise ValueError(f"❌ No locators found for page: {page_name} on platform: {platform}")

        return page_locators
