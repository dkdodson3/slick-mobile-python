class Gen:
    """
    Gen or Generator is a helper class for building locators

    To utilize this, when you initialize the mobile app you need to call Gen.set_target with the target (android, ios, android_simulator, ios_simulator)
    """
    TARGET = None
    IS_DEMO = False
    PRECEDING_SIBLING = "preceding-sibling"
    FOLLOWING_SIBLING = "following-sibling"

    # ANDROID
    ACTION_BAR_TAB = None
    ANDROID_HOME = 3
    ANDROID_ID = None
    ANDROID_CHROME_ID = None
    ANDROID_INSTALLER_ID = None
    BUTTON = None
    CHECK_BOX = None
    FRAME_LAYOUT = None
    HORIZONTAL_SCROLL_VIEW = None
    IMAGE_BUTTON = None
    IMAGE_VIEW = None
    LINEAR_LAYOUT = None
    LINEAR_LAYOUT_COMPAT = None
    RECYCLER_VIEW = None
    RELATIVE_LAYOUT = None
    SCROLL_VIEW = None
    SOFT_KEYBOARD = None
    SWITCH = None
    TEXT_EDIT = None
    TEXT_INPUT_LAYOUT = None
    TEXT_SWITCHER = None
    TEXT_VIEW = None
    VIEW = None
    VIEW_GROUP = None
    VIEW_PAGER = None

    # IOS
    ALERT = None
    CELL = None
    COLLECTION_VIEW = None
    IMAGE = None
    INDICATOR = None
    NAVIGATIONBAR = None
    OTHER = None
    PICKER_WHEEL = None
    SEARCH = None
    SEGMENT_CONTROL = None
    SHEET = None
    STATIC_TEXT = None
    TABLE = None
    TEXT_FIELD = None
    TEXT_FIELD_SECURE = None
    TOOLBAR = None

    @staticmethod
    def is_ios():
        return "ios" in Gen.get_target()

    @staticmethod
    def is_android():
        return "android" in Gen.get_target()

    @staticmethod
    def is_simulator():
        target = Gen.get_target()
        return "simulator" in target or "emulator" in target

    @staticmethod
    def get_target():
        if Gen.TARGET is None:
            raise Exception("Target was not set. {}".format(Gen.TARGET))

        return Gen.TARGET

    @staticmethod
    def set_target(target):
        if target is None:
            raise Exception("**** Gen TARGET cannot be set to None, Check your config file. ****")

        print("SETTING Gen TARGET: {}".format(target))
        Gen.TARGET = target.lower()
        if "ios" in target:
            Gen.set_ios()
        else:
            Gen.set_android()

    # HELPER FUNCTIONS
    @staticmethod
    def set_ios():
        Gen.ALERT = "XCUIElementTypeAlert"
        Gen.BUTTON = "XCUIElementTypeButton"
        Gen.CELL = "XCUIElementTypeCell"
        Gen.COLLECTION_VIEW = "XCUIElementTypeCollectionView"
        Gen.IMAGE = "XCUIElementTypeImage"
        Gen.INDICATOR = "XCUIElementTypePageIndicator"
        Gen.NAVIGATIONBAR = "XCUIElementTypeNavigationBar"
        Gen.OTHER = "XCUIElementTypeOther"
        Gen.PICKER_WHEEL = "XCUIElementTypePickerWheel"
        Gen.SCROLL_VIEW = "XCUIElementTypeScrollView"
        Gen.SEARCH = "XCUIElementTypeSearchField"
        Gen.SEGMENT_CONTROL = "XCUIElementTypeSegmentedControl"
        Gen.SHEET = "XCUIElementTypeSheet"
        Gen.SOFT_KEYBOARD = "XCUIElementTypeKeyboard"
        Gen.STATIC_TEXT = "XCUIElementTypeStaticText"
        Gen.SWITCH = "XCUIElementTypeSwitch"
        Gen.TABLE = "XCUIElementTypeTable"
        Gen.TEXT_FIELD = "XCUIElementTypeTextField"
        Gen.TEXT_FIELD_SECURE = "XCUIElementTypeSecureTextField"
        Gen.TOOLBAR = "XCUIElementTypeToolbar"

    @staticmethod
    def set_android():
        Gen.ACTION_BAR_TAB = "android.support.v7.app.ActionBar.Tab"
        Gen.ANDROID_ID = "android:id"
        Gen.ANDROID_CHROME_ID = "com.android.chrome:id"
        Gen.ANDROID_INSTALLER_ID = "com.android.packageinstaller:id"
        Gen.BUTTON = "android.widget.Button"
        Gen.CHECK_BOX = "android.widget.CheckBox"
        Gen.FRAME_LAYOUT = "android.widget.FrameLayout"
        Gen.HORIZONTAL_SCROLL_VIEW = "android.widget.HorizontalScrollView"
        Gen.IMAGE_BUTTON = "android.widget.ImageButton"
        Gen.IMAGE_VIEW = "android.widget.ImageView"
        Gen.LINEAR_LAYOUT = "android.widget.LinearLayout"
        Gen.LINEAR_LAYOUT_COMPAT = "android.support.v7.widget.LinearLayoutCompat"
        Gen.RECYCLER_VIEW = "android.support.v7.widget.RecyclerView"
        Gen.RELATIVE_LAYOUT = "android.widget.RelativeLayout"
        Gen.SCROLL_VIEW = "	android.widget.ScrollView"
        Gen.SOFT_KEYBOARD = "UIAKeyboard"
        Gen.SWITCH = "android.widget.Switch"
        Gen.TEXT_EDIT = "android.widget.EditText"
        Gen.TEXT_INPUT_LAYOUT = "TextInputLayout"
        Gen.TEXT_SWITCHER = "android.widget.TextSwitcher"
        Gen.TEXT_VIEW = "android.widget.TextView"
        Gen.VIEW = "android.view.View"
        Gen.VIEW_GROUP = "android.view.ViewGroup"
        Gen.VIEW_PAGER = "android.support.v4.view.ViewPager"

    @staticmethod
    def get_xpath_resource(text):
        return "@resource-id='{}'".format(text)

    @staticmethod
    def get_xpath_id(text):
        return "@id='{}'".format(text)

    @staticmethod
    def get_xpath_name(text):
        return "@name='{}'".format(text)

    @staticmethod
    def get_xpath_label(text):
        return "@label='{}'".format(text)

    @staticmethod
    def get_xpath_text(text):
        return "@text='{}'".format(text)

    @staticmethod
    def get_xpath_value(text):
        return "@value='{}'".format(text)

    @staticmethod
    def get_xpath_content_description(text):
        return "@content-desc='{}'".format(text)

    @staticmethod
    def get_xpath_contains(value, text):
        return "contains(@{}, '{}')".format(value, text)

    @staticmethod
    def get_xpath_name_contains(text):
        return Gen.get_xpath_contains("name", text)

    @staticmethod
    def get_xpath_text_contains(text):
        return Gen.get_xpath_contains("text", text)

    @staticmethod
    def get_element_contains(element_type, value, text):
        from slick_mobile_locator import SlickMobileLocator, Find
        return SlickMobileLocator("Element contains text for value xpath", Find.by_xpath('//{}[{}]'.format(element_type, Gen.get_xpath_contains(value, text))))

    @staticmethod
    def get_element_xpath_contains(element_type, value, text):
        return '{}[{}]'.format(element_type, Gen.get_xpath_contains(value, text))

    @staticmethod
    def get_contains_case_insensitive():
        # This is more here so if we need it in the future we can figure it out
        return '//*[contains(translate(@text, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "support")]'

    @staticmethod
    def get_element_by_xpath_text(text):
        return Gen.get_element_contains(Gen.TEXT_VIEW, "text", text)

    @staticmethod
    def get_ios_predicate_type(tag_type):
        return "type == '{}'".format(tag_type)

    @staticmethod
    def get_android_id(text):
        return "{}/{}".format(Gen.ANDROID_ID, text)

    @staticmethod
    def get_android_installer_id(text):
        return "{}/{}".format(Gen.ANDROID_INSTALLER_ID, text)

    @staticmethod
    def get_android_resource_id(text):
        return "@resource-id='{}/{}'".format(Gen.ANDROID_ID, text)

    @staticmethod
    def get_android_chrome_id(text):
        return "{}/{}".format(Gen.ANDROID_CHROME_ID, text)

    @staticmethod
    def get_xpath_enabled(value):
        if value:
            text = "true"
        else:
            text = "false"
        return "@enabled='{}'".format(text)

    @staticmethod
    def get_xpath_visible(value):
        if value:
            text = "true"
        else:
            text = "false"
        return "@visible='{}'".format(text)

    @staticmethod
    def get_xpath_checked(value):
        if value:
            text = "true"
        else:
            text = "false"
        return "@checked='{}'".format(text)