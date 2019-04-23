import time

from appium.webdriver import WebElement
from slickwd import WebElementLocator, Find, Timer

class SlickMobileLocator:
    def __init__(self, desc, finder, attr=None, text=None, parent=None, num=None, visible=False, tag_name=None, case_insensitive=True, throw_exception=None):
        """
        A customized locator for Mobile
        :param desc: Description of locator
        :param finder: A finder that the locator will use
        :param attr:
        :param text:
        :param parent:
        :param num:
        :param screenshot:
        :param visible:
        :param tag_name:
        :param case_insensitive:
        :param throw_exception:
        """
        if not isinstance(finder, Find):
            raise Exception("finder is not of type Find")

        if parent is not None:
            from appium.webdriver import WebElement
            if not isinstance(parent, SlickMobileLocator) and not isinstance(parent, WebElement):
                raise Exception("parent is not of type SlickMobileLocator or WebElement")

        self.desc = desc
        self.finder = finder
        self.attr = attr
        self.text = text
        self.parent = parent
        self.num = num
        self.visible = visible
        self.tag_name = tag_name
        self.case_insensitive = case_insensitive
        self.throw_exception = throw_exception

        self.locator = WebElementLocator(desc, finder)
        """:type: MobileElementLocator"""
        self.element = None
        """:type: WebElement"""
        self.elements = []
        """:type: list[WebElement]"""

        self.app_init_timeout = 180
        self.is_android = False
        self.is_ios = False
        
    @property
    def app(self):
        """
        This needs to be instantiated from a child class and should be of type appium.webdriver.Remote
        """
        raise NotImplementedError("Need to get the app from somewhere")

    @property
    def driver(self):
        """:type: appium.webdriver.Remote"""
        return self.app.driver

    def init_attr(self):
        if self.attr is None:
            if self.is_android:
                self.attr = "text"
            else:
                self.attr = "name"

    def refresh(self):
        """
        Remove the old elements
        :return:
        """
        self.element = None
        self.elements = []

    def print_page_source(self):
        print(self.app.get_page_source())

    def gimme(self, timeout=10, log=True, throw_exception=False, num=None):
        """
        Get a single element for the locator
        :param timeout:
        :param log:
        :param throw_exception:
        :param num: int
        :return:
        :rtype: SlickMobileLocator
        """
        if num is not None:
            self.num = num

        if self.parent or self.text or self.num is not None or self.visible or self.tag_name:
            self.gimme_all(timeout, log, throw_exception)

            if self.elements:
                self.element = self.elements[self.num if self.num is not None else 0]

        else:
            self.element = self.locator.find_element_matching(self.driver, timeout=timeout, log=log)

            if self.element is None:
                if (self.throw_exception is None and throw_exception) or self.throw_exception:
                    self.print_page_source()
                    raise Exception("Could not find element with description of {} and {}.".format(self.desc, self.finder.describe()))

                return self

            if not self.elements:
                self.elements.append(self.element)

            if self.visible and not self.element.is_displayed():
                raise Exception("Could not find element with description of {} and {} that was visible.".format(self.desc, self.finder.describe()))

        return self

    def gimme_all(self, timeout=10, log=True, throw_exception=False):
        """
        Get all the elements for the locator
        :param timeout:
        :param log:
        :param throw_exception:
        :return: SlickMobileLocator
        """
        if self.parent is not None:
            self.deliver(timeout=timeout, log=log)
        else:
            self.elements = self.locator.find_all_elements_matching(self.driver, timeout=timeout, log=log)

        if len(self.elements) < 1:
            if (self.throw_exception is None and throw_exception) or self.throw_exception:
                self.print_page_source()
                raise Exception("Could not find elements with description of {} and {}.".format(self.desc, self.finder.describe()))

            return self

        if self.visible:
            self.get_visible_elements()

            if len(self.elements) < 1:
                if (self.throw_exception is None and throw_exception) or self.throw_exception:
                    raise Exception("Could not find elements with description of {} and {} that were visible.".format(self.desc, self.finder.describe()))

                return self

        if self.text:
            self.get_elements_with_text()

            if len(self.elements) < 1:
                if (self.throw_exception is None and throw_exception) or self.throw_exception:
                    raise Exception("Could not find elements with description of {} and {} with text: {}.".format(self.desc, self.finder.describe(), self.text))

                return self

        if self.tag_name:
            self.get_elements_with_tag_name()

            if len(self.elements) < 1:
                if (self.throw_exception is None and throw_exception) or self.throw_exception:
                    raise Exception("Could not find elements with description of {} and {} with tag_name: {}.".format(self.desc, self.finder.describe(), self.tag_name))

                return self

        return self

    def deliver(self, timeout=10, log=True, refresh=True):
        """
        Get a child element from a parent
        :return: SlickMobileLocator
        """
        if isinstance(self.parent, WebElement):
            self.elements = self.locator.find_all_elements_from_parent_element(self.parent, wd_browser=self.driver, timeout=timeout, log=log)
        else:
            if self.parent.exists(timeout=timeout, log=log, throw_exception=True, refresh=refresh):
                self.elements = self.locator.find_all_elements_from_parent_element(self.parent.element, wd_browser=self.driver, timeout=timeout, log=log)

        return self

    def get_locator_num(self, num=None):
        if not self.elements:
            self.gimme_all()

        return self.elements[num]

    def get_visible_elements(self):
        elements = []
        for element in self.elements:
            if self.is_element_displayed(element):
                elements.append(element)

        self.elements = elements

    def get_elements_with_tag_name(self):
        elements = []
        for element in self.elements:
            if element.tag_name == self.tag_name:
                elements.append(element)

        self.elements = elements

    def get_elements_with_text(self):
        ret_val = []
        exact_ret_val2 = []
        text = self.text
        if self.case_insensitive:
            text = text.lower()
        for element in self.elements:
            if element.get_attribute(self.attr) is not None:
                value = element.get_attribute(self.attr)
                if self.case_insensitive:
                    value = value.lower()
                if text in value:
                    ret_val.append(element)

        for element2 in ret_val:
            value2 = element2.get_attribute(self.attr)
            if self.case_insensitive:
                value2 = value2.lower()
            if text == value2:
                exact_ret_val2.append(element2)

        self.elements = ret_val if len(exact_ret_val2) == 0 else exact_ret_val2

    def get_text(self, timeout=5, num=None, log=False, throw_exception=True, refresh=True):
        """
        Get the text for the locator by the attr
        :param timeout:
        :param log:
        :param throw_exception:
        :param refresh:
        :return: str
        """
        text = None
        if self.exists(timeout=timeout, num=num, log=log, throw_exception=throw_exception, refresh=refresh):
            if num is None:
                text = self.element.get_attribute(name=self.attr)
            else:
                text = self.elements[num].get_attribute(name=self.attr)

        return text.encode('utf-8') if text else ""

    def wait_for(self, description, func, timeout=60, interval=.5, throw_exception=False):
        """
        This is for waiting until the lambda function returns True
        :param description:
        :param func:
        :param timeout:
        :param interval:
        :param throw_exception:
        :return:
        """

        attempt = 1
        print("\nWaiting {} seconds for: {} to be".format(timeout, description))
        timer = Timer(timeout)
        last_result = False
        error_message = None
        try:
            last_result = func()
        except:
            pass
        while not last_result and not timer.is_past_timeout():
            try:
                last_result = func()
            except Exception as e:
                print(e.message)
                error_message = e.message

            print("Still not found... attempt: {}".format(attempt))
            time.sleep(interval)
            attempt += 1

        print("Wait for tried: {} times in {} seconds".format(attempt, timeout))
        if throw_exception and not last_result:
            raise Exception("Timeout failed with: {}".format(error_message))

        return last_result

    def wait_for_not(self, description, func, timeout=60, interval=.5, throw_exception=False):
        """
        This is for waiting until the lambda function returns False

        :param description:
        :param func:
        :param timeout:
        :param interval:
        :param throw_exception:
        :return:
        """
        attempt = 1
        print("\nWaiting {} seconds for: {} to not be".format(timeout, description))
        timer = Timer(timeout)
        last_result = False
        error_message = None
        try:
            last_result = func()
        except:
            pass
        while last_result and not timer.is_past_timeout():
            try:
                last_result = func()
            except Exception as e:
                print(e.message)
                error_message = e.message

            print("Still found... attempt: {}".format(attempt))
            time.sleep(interval)
            attempt += 1

        print("Wait for tried: {} times in {} seconds".format(attempt, timeout))
        if last_result:
            if throw_exception:
                raise Exception("Timeout failed with: {}".format(error_message))
            else:
                return False

        return True

    def exists(self, timeout=5, log=True, num=None, throw_exception=False, refresh=True):
        if refresh:
            self.gimme(timeout=timeout, log=log, num=num, throw_exception=throw_exception)

        return self.element is not None

    def is_displayed(self, timeout=5, log=True, num=None, throw_exception=False, refresh=True, wait_for_interval=.5):
        if not self.exists(timeout=timeout, log=log, num=num, throw_exception=throw_exception, refresh=refresh):
            return False

        if self.element is None:
            self.gimme(timeout=timeout, log=log, num=num, throw_exception=throw_exception)
            if self.element is None:
                return False

        return self.wait_for("Waiting for the {} element to be displayed".format(self.desc), lambda: self.is_element_displayed(self.element), timeout=timeout, interval=wait_for_interval, throw_exception=throw_exception)

    def is_element_displayed(self, element):
        if element is None:
            return False

        if self.is_android:
            displayed = element.is_displayed()
        else:
            displayed = self.is_element_on_screen(element)

        return displayed

    def is_on_screen(self, timeout=5, log=True, num=None, throw_exception=False, refresh=True):
        if refresh:
            self.refresh()

        if self.element is None:
            self.gimme(timeout=timeout, log=log, num=num, throw_exception=throw_exception)

        return self.is_element_on_screen(self.element)

    def is_element_on_screen(self, element=None):
        if element is None:
            return False

        x, y = self.get_element_coordinates(element)
        if x < 0 or y < 0:
            return False

        if x > self.app.screen_width or y > self.app.screen_height:
            return False

        return True

    def is_enabled(self, timeout=5, log=True, num=None, throw_exception=False, refresh=True, wait_for_interval=.5):
        if self.is_displayed(timeout=timeout, log=log, num=num, throw_exception=throw_exception, refresh=refresh, wait_for_interval=wait_for_interval):
            return self.wait_for("Waiting for the {} element to be enabled".format(self.desc), lambda: self.element.is_enabled(), timeout=timeout, interval=wait_for_interval, throw_exception=throw_exception)

        return False

    def is_selected(self, timeout=5, log=True, num=None, throw_exception=False, refresh=True, wait_for_interval=.5):
        if self.is_displayed(timeout=timeout, log=log, num=num, throw_exception=throw_exception, refresh=refresh, wait_for_interval=wait_for_interval):
            return self.wait_for("Waiting for the {} element to be selected".format(self.desc), lambda: self.element.is_selected(), timeout=timeout, interval=wait_for_interval, throw_exception=throw_exception)

        return False

    def is_checked(self, timeout=5, log=True, num=None, refresh=True):
        if self.is_displayed(timeout=timeout, log=log, num=num, refresh=refresh):
            if self.is_android:
                return self.element.get_attribute("checked") == "true"
            else:
                value = self.element.get_attribute(name="value")
                if value is None:
                    value = 0
                return int(value) == 1

        return False

    def not_exists(self, timeout=5, log=True, num=None, wait_for_interval=.5, refresh=True, throw_exception=False):
        if self.exists(timeout=5, log=log, num=num, refresh=refresh):
            self.wait_for_not("Waiting for the {} element to not be displayed".format(self.desc), lambda: self.exists(timeout=0, log=log, num=num, refresh=refresh), timeout=timeout, interval=wait_for_interval, throw_exception=throw_exception)

        return True

    def is_not_displayed(self, timeout=5, log=True, num=None, wait_for_interval=.5, refresh=True, throw_exception=False):
        if self.is_displayed(timeout=5, log=log, num=num, refresh=refresh, wait_for_interval=wait_for_interval):
            return self.wait_for_not("Waiting for the {} element to not be displayed".format(self.desc), lambda: self.is_element_displayed(self.element), timeout=timeout, interval=wait_for_interval, throw_exception=throw_exception)

        return True

    def is_not_enabled(self, timeout=5, log=True, num=None, throw_exception=False, refresh=True, wait_for_interval=.5):
        if self.is_enabled(timeout=1, log=log, num=num, refresh=refresh, wait_for_interval=wait_for_interval):
            return self.wait_for_not("Waiting for the {} element to not be enabled".format(self.desc), lambda: self.element.is_enabled(), timeout=timeout, interval=wait_for_interval, throw_exception=throw_exception)

        return True

    def is_not_selected(self, timeout=5, log=True, num=None, throw_exception=False, refresh=True, wait_for_interval=.5):
        if self.is_selected(timeout=1, log=log, num=num, refresh=refresh, wait_for_interval=wait_for_interval):
            return self.wait_for_not("Waiting for the {} element to not be selected".format(self.desc), lambda: self.element.is_selected(), timeout=timeout, interval=wait_for_interval, throw_exception=throw_exception)

        return True

    def tap(self, timeout=10, count=1, offset_x=1, offset_y=1, log=True, wait=0, raise_exception=True, duration=50, num=None, refresh=True, wait_for_interval=.5):
        positions = []

        if not self.is_displayed(timeout=timeout, log=log, num=num, refresh=refresh, wait_for_interval=wait_for_interval):
            msg = "Could not find the '{}' element to tap on.".format(self.desc)
            if isinstance(raise_exception, str):
                raise Exception(raise_exception)
            elif raise_exception:
                raise Exception(msg)
            else:
                print(msg)
                return False

        if offset_x != 1 or offset_y != 1:
            if not offset_x or not offset_y:
                size = self.element.size
                if not offset_x:
                    offset_x = size['width'] / 2
                if not offset_y:
                    offset_y = size['height'] / 2

            x, y = self.get_locator_coordinates()
            x = x + offset_x
            y = y + offset_y

            positions = [(x, y)]

        if positions:
            self.app.tap_position(positions=positions, count=count, duration=duration, wait=wait, log=log)
        else:
            for i in range(count):
                self.element.click()

        return True

    def send_keys(self, keys, timeout=5, log=True, clear=False, hide_keyboard=False, key_name=None, wait=None, tap=False, type=False, num=None, checkmark=False, throw_exception=True, refresh=True, wait_for_interval=.5):
        self.is_displayed(timeout=timeout, log=log, num=num, throw_exception=throw_exception, refresh=refresh, wait_for_interval=wait_for_interval)

        if self.element:
            if tap:
                self.element.click()

            text = self.element.text
            if text is None:
                text = ""
            else:
                text = str(text.encode("utf-8"))
            if clear:
                if len(text) > 0 and text not in ['Email', 'Password'] and text != keys:
                    self.element.clear()

            if keys != text:
                if type:
                    self.element.send_keys(keys)
                else:
                    self.driver.set_value(self.element, keys)

            if hide_keyboard or checkmark:
                self.app.hide_keyboard(checkmark=checkmark, key_name=key_name)

            if wait is not None:
                time.sleep(wait)

    def get_locator_coordinates(self, refresh=True):
        self.exists(throw_exception=True, refresh=refresh)
        return self.get_element_coordinates(self.element)

    def get_element_coordinates(self, element):
        location = element.location
        x = int(location["x"])
        y = int(location["y"])
        return x, y

    def get_locator_size(self, refresh=True):
        self.exists(throw_exception=True, refresh=refresh)
        size = self.element.size
        width = int(size["width"])
        height = int(size["height"])
        return width, height

    def get_rect(self):
        start_x, start_y = self.get_locator_coordinates()
        width, height = self.get_locator_size(refresh=False)
        return start_x, start_y, width, height

    def get_coordinate_location(self, side="MIDDLE"):
        start_x, start_y, width, height = self.get_rect()

        side = side.upper()
        if side == "TOP":
            x = (width / 2) + start_x
            y = start_y
        elif side == "BOTTOM":
            x = (width / 2) + start_x
            y = height + start_y
        elif side == "LEFT":
            x = start_x
            y = (height / 2) + start_y
        elif side == "RIGHT":
            x = width + start_x
            y = (height / 2) + start_y
        else:
            x = (width / 2) + start_x
            y = (height / 2) + start_y

        return x, y
