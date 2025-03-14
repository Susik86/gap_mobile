from appium.webdriver.common.appiumby import AppiumBy

class GMExploreTeamLocators:
    ANDROID = {
        "GM_PAGE": {
            "screen_title":(AppiumBy.ID, ""),
            "back_button":(AppiumBy.ID, ""),
            "legend_icon": (AppiumBy.ID, ""),
            "team_edit_btn": (AppiumBy.XPATH, ""),
            "project_edit_btn": (AppiumBy.XPATH, ""),
            "outcome_edit_btn": (AppiumBy.XPATH, ""),

        }
    }

    IOS = {
        "GM_PAGE": {
            "screen_title":(AppiumBy.IOS_PREDICATE, 'label == "Invite to Team""'),
            "back_button":(AppiumBy.IOS_PREDICATE, 'label == "Create a Team"'),
            "legend_icon": (AppiumBy.ID, ""),
            "team_edit_btn": (AppiumBy.XPATH, "(//XCUIElementTypeButton[@name='D Edit'])[1]"),
            "project_edit_btn": (AppiumBy.XPATH, "(//XCUIElementTypeButton[@name='D Edit'])[2]"),
            "outcome_edit_btn": (AppiumBy.XPATH, "(//XCUIElementTypeButton[@name='D Edit'])[3]"),
            "info_btn":(AppiumBy.ACCESSIBILITY_ID, "infoIcon"),
            "add_member_btn":(AppiumBy.ACCESSIBILITY_ID, "add member"),
            "launch_pulse_btn":(AppiumBy.XPATH, '//XCUIElementTypeStaticText[@name="Launch Genius Pulse"]'),
            "my_scores_tab":(AppiumBy.ACCESSIBILITY_ID, 'My Scores'),
            "team_scores_tab":(AppiumBy.ACCESSIBILITY_ID, 'Team Scores'),
            "no_data_txt":(AppiumBy.IOS_PREDICATE, "label CONTAINS 'There is no data for your team'"),
            "team_members_txt":(AppiumBy.ACCESSIBILITY_ID, "Team Members"),
            "view_all_btn":(AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`label == "View All"`]'),
            "leave_team_btn":(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="Leave Team"]'),
            "delete_team_btn":(AppiumBy.XPATH, '//XCUIElementTypeButton[@name="Delete Team"]'),






    }
    }

    @staticmethod
    def get_locators(page_name, platform):
        locators = getattr(GMExploreTeamLocators, platform.upper(), None)
        if locators is None:
            raise ValueError(f"❌ Unsupported platform: {platform}")

        page_locators = locators.get(page_name, None)
        if page_locators is None:
            raise ValueError(f"❌ No locators found for page: {page_name} on platform: {platform}")

        return page_locators

    @staticmethod
    def get_team_edit_locator(team_name):
        """
        Generates a locator for the Edit button next to the given team name.
        :param team_name: The name of the team (e.g., "Team A").
        :return: Tuple with AppiumBy strategy and dynamic XPath locator.
        """
        return (AppiumBy.XPATH, f"//XCUIElementTypeStaticText[@label='{team_name}']/following-sibling::XCUIElementTypeButton[@name='D Edit']")
