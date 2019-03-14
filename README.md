# slick-mobile-python

These are helper libraries for writing mobile tests that you can use and inherit from to customize to your needs.

How you implement appium and its client is on you.

To make these libraries function you will need to run the setup.sh before you start

## slick_mobile_app
The SlickMobileApp class helps you to interact with the mobile devices
It has many tweaks for ios and android

## slick_mobile_locator
the SlickMobileLocator class allows you to easily find elements.
It allows you to find elements starting at a parent locator
It allows you to interact with the element or elements from the locator
All the functions in this class only interact with the specific locator, not the app as a whole.

## slick_mobile_locator_helper
The Gen class makes it easier for you to create SlickMobileLocators. 
It has functions in there for you to determine which mobile device type you are from whatever location. (You have to run the set_target function first)
It makes it so that you don't need to worry about fat fingering things or trying to remember what xpath syntax to use or how to get an ios predicate type...
