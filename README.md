# slick-mobile-python

These are helper libraries for writing mobile tests that you can use and inherit from to customize to your needs.

How you implement appium and its client is on you.

To make these libraries function you will need to run the setup.sh before you start

## slick_mobile_app
The SlickMobileApp class helps you to interact with the mobile devices
It has many tweaks for ios and android

## slick_mobile_locator_helper
The Gen class makes it easier for you to create SlickMobileLocators. 
It has functions in there for you to determine which mobile device type you are from whatever location. (You have to run the set_target function first)
It makes it so that you don't need to worry about fat fingering things or trying to remember what xpath syntax to use or how to get an ios predicate type...

## slick_mobile_locator
the SlickMobileLocator class allows you to easily find elements.
It allows you to find elements starting at a parent locator
It allows you to interact with the element or elements from the locator
All the functions in this class only interact with the specific locator, not the app as a whole.

#### Purpose of MobileLocator:
- The mobilelocator class is used as a wrapper for basic appium functionality.  An instance of the class stores found element(s), how to find the element, and various methods allowing you to determine if the element is displayed, get text from the element, size and position of the element, etc.

##
#### \__init__(desc. finder, attr, text, parent, num, screenshot, visible, tag_name, case_insensitive, throw_exception) 
This method will initialize the class and set these variables
- self.driver - (appium.webdriver.Remote object)
- self.app - (MobileApp object)
- self.locator - (MobileElementLocator object)
- self.element  - (WebElement object)
- self.elements - (list of WebElement objects)
- self.app_init_timeout - (int)
- self.is_ios - (bool)
- self.is_android - (bool)

Param Definitions
- desc - (text), no default, description of what the element is
- finder - (MobileFind object), no default, how the element will be found, using "by" and "value"
  - "by": id/accessibility, name, xpath, class name, link text, partial link text, css selector, tag name, android ui automator, ios predicate, or ios uiautomation
  - "value" is the text of the element's attribute the "by" searches for
  - Example: MobileFind.by_name("qa_add_user_cell")
- attr - (text), default = None, an attribute of an element for use in 1) finding an element using the text of the attribute during gimme() or 2) verifying the text of the elements attribute during get_text()
- text - (text), default = None, used for selecting the correct element based on the supplied text matching the text in the element when one or more elements are found
- parent - (MobileLocator object), default = None, used when the current element can only or more easily be found after first finding a parent/grandparent element then finding this element in the context of the parent element
- num - (int) default = None, used when finding multiple elements and no way to select a specific element using attr or text, you can specify the number of the element you want to use
- screenshot - (bool), default = True, deprecated, using flick to record test, used to take a screenshot of the current screen after finding an element
- visible - (bool), default = False, used as an extra check (mostly for iOS) that the element is truly visible on the screen
- tag_name - (text), default = None, used when multiple elements are found but with different class/tag types you can specify the element you want that matches the supplied class/tag
- case_insensitive - (bool), default = True, used to determine if you want to match case and spelling when comparing text of if you just want to see if the spelling is correct
- throw_exception - (bool or None), default = None, used for specifying if you want an error thrown when the element isn't found
##
#### gimme(timeout, log, throw_exception, num)
Will call gimme_all() if self.parent, self.text, self.num, self.visible, or self.tag_name are not None or False
##
#### gimme_all(timeout, log, throw_exception, num)
This method is used to find multiple elements and sets self.elements
- Will call deliver() if self.parent is not None
##
#### deliver(timeout, log, refresh)
This method will use a self.parent element to find the child element
##
#### (exists/not_exists)(timeout, log, num, throw_exception, refresh)
These methods determine if the element exists currently returns bool
- exists() calls wait_for() with gimme() as a lambda function
- not_exists() calls exists() and wait_for_not() with exists() as a lambda function
##
#### (is_displayed/is_not_displayed)(timeout, log, num, throw_exception, refresh, wait_for_interval)
These methods determine if the element is visible on the screen or not, return bool
- is_displayed() call exists(), gimme(), and wait_for() with is_element_displayed() as a lambda function
- is_not_displayed() calls is_displayed() and wait_for_not() with is_element_displayed() as a lambda function
##
#### (is_enabled/is_not_enabled)(timeout, log, num, throw_exception, refresh, wait_for_interval)
These methods determine if the element is enabled or not, returns bool
- is_enabled() calls is_displayed() and wait_for() with element.is_enabled() as the lambda function
- is_not_enabled() calls is_enabled() and wait_for_not() with element.is_enabled() as the lambda function
##
#### (is_selected/is_not_selected)(timeout, log, num, throw_exception, refresh, wait_for_interval)
These methods determine if radio button, etc. element is selected or not, returns bool
- is_selected() calls is_displayed() and wait_for() with element.is_selected() as the lambda function
- is_not_selected() calls is_selected() and wait_for_not() with element.is_selected() as the lambda function
##
#### (wait_for/wait_for_not)(description, func, timeout, interval, throw_exception)
These methods periodically check for an element to be/not be for the specified length of time, returns bool)
- Calls the passed in function (e.g, is_displayed(), exists(), etc.)
##
#### is_checked(timeout, log, num, refresh)
This method determines if a check box element is checked, returns bool
- Calls is_displayed() and element.get_attribute()
##
#### get_text(timeout, num, log, throw_exception, refresh)
This method uses self.attr to extract the text from the attribute of the element, returns text
- Calls exists() and element.get_attribute()
##
#### tap(timeout, count, offset_x, offset_y, log, wait, raise_exception, duration, num, refresh, wait_for_interval)
This method taps/clicks on an element, returns True
- Calls is_displayed()

Param Definitions
- count - how many times to tap
- offset_x - tap a number of pixels down from the top of the element 
- offset_y - tap a number of pixels right of the left of the element
- duration - how long to hold the tap
##
#### send_keys(keys, timeout, log, clear, hide_keyboard, key_name, wait, tap, type, num, checkmark, throw_exception, refresh, wait_for_interval)

This method taps a text field then enters text into the field
- Calls is_displayed()
##
#### Helper Functions
- configure()
- get_app()
- get_driver()
- get_default_attr()
- take_screenshot()
- refresh()
- print_page_source()
- print_element_data()
- show_locator_info()
- get_locator_num()
- get_visible_elements()
- get_elements_with_tag_name()
- get_elements_with_text()
- is_element_displayed()
- is_on_screen()
- is_element_on_screen()
- get_locator_coordinates()
- get_element_coordinates()
- get_locator_size()
- get_rect()
- get_coordinate_location()
- refresh_element()

