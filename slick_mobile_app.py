import logging
from time import sleep
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver import WebElement
from selenium.webdriver.remote.command import Command
from slickwd import Browser, Find
from slick_mobile_locator import SlickMobileLocator


class SlickMobileApp(Browser):
    actual_screen_width = None
    actual_screen_height = None
    screen_width = None
    screen_height = None
    ratio = None
    multiplier = None
    platform_name = None
    device_name = None
    target_device = None

    def __init__(self, default_timeout=30):
        """
        Initializing the app with the appium driver and not initializing the parent
        You should inherit from this and replace driver
        :param desired_capabilities:
        :param remote_url:
        :param default_timeout:
        """
        self.default_timeout = default_timeout
        # self.remote_url = remote_url
        # self.desired_capabilities = desired_capabilities
        self.angular_mode = False

        # tame the huge logs from webdriver
        wdlogger = logging.getLogger('selenium.webdriver')
        wdlogger.setLevel(logging.WARNING)
        self.logger = logging.getLogger("slickwd.Appium")

        # self.wd_instance = appium.webdriver.Remote(command_executor=remote_url, desired_capabilities=desired_capabilities)
        # self.driver = self.wd_instance
        # self.driver.implicitly_wait(0)

        self.platform_name = self.get_capabilities()['platformName'].lower()
        self.device_name = self.get_capabilities()['deviceName'].lower()
        self.target_device = "{}_{}".format(self.platform_name, self.get_version())
        self.get_image_multiplier()

        # Screenshot properties
        self.unique_screenshots = True
        self.screenshot_dir = None
        self.screenshot_blob = None

    @property
    def touch_action(self):
        return TouchAction(self.driver)

    @property
    def driver(self):
        """
        This needs to be instantiated from a child class and should be of type appium.webdriver.Remote
        """
        raise NotImplementedError("Need to get the driver from somewhere")

    def set_log_level(self, level):
        self.logger.setLevel(level)

    def get_capabilities(self):
        return self.driver.desired_capabilities

    def is_android(self):
        return self.platform_name == "android"

    def is_ios(self):
        return self.platform_name == "ios"

    def is_simulator(self):
        return self.get_capabilities()['isSimulator']

    def is_ipad(self):
        if self.is_ios():
            return "ipad" in self.device_name

        return False

    def is_iphone(self):
        if self.is_ios():
            return "iphone" in self.device_name

        return False

    def no_reset_enabled(self):
        return self.get_capabilities()['noReset']

    def get_version(self):
        return self.get_capabilities()['platformVersion'].lower()

    def get_base_version(self):
        version = self.get_version()
        return int(version.split(".")[0])

    def refresh_cache(self):
        # This should reset the cache when we are having issues finding elements
        self.driver.execute(Command.GET_PAGE_SOURCE)['value'].encode("utf-8")

    def get_screen_size(self):
        if self.screen_width is None or self.screen_height is None:
            size = self.driver.get_window_size()
            self.screen_width = int(size["width"])
            self.screen_height = int(size["height"])

        return self.screen_width, self.screen_height

    def get_actual_screen_size(self):
        if self.actual_screen_width is None or self.actual_screen_height is None:
            screen_shot_blob = self.get_screenshot_blob()
            image = SlickMobileApp.create_image_from_screenshot(screen_shot_blob)
            self.actual_screen_width, self.actual_screen_height = SlickMobileApp.get_image_size(image)

        return self.actual_screen_width, self.actual_screen_height

    def get_image_ratio(self):
        if self.ratio is None:
            self.get_screen_size()
            self.get_actual_screen_size()

            self.ratio = self.screen_width / self.actual_screen_width

        return self.ratio

    def get_image_multiplier(self):
        if self.multiplier is None:
            self.get_image_ratio()

            self.multiplier = 1 / self.ratio

        return self.multiplier

    def get_actual_rect(self, rect):
        if self.multiplier is None:
            self.get_image_multiplier()

        actual_rect = (int(rect[0] * self.multiplier),
                       int(rect[1] * self.multiplier),
                       int(rect[2] * self.multiplier),
                       int(rect[3] * self.multiplier))

        return actual_rect

    def get_middle_coords(self):
        x, y = self.get_screen_size()
        return x / 2, y / 2

    def background_app(self, seconds=5):
        if self.is_ios():
            self.driver.background_app(seconds=seconds)
        else:
            self.driver.press_keycode(3)
            sleep(seconds)
            self.foreground_app_android()

    def restart_app(self, seconds=5):
        import time
        if self.driver is not None:
            self.driver.close_app()
            time.sleep(seconds)
            self.driver.launch_app()

    def lock_device(self, seconds=5):
        if self.is_ios():
            self.driver.lock(seconds=seconds)
        else:
            self.driver.press_keycode(26)
            sleep(seconds)
            self.driver.press_keycode(82)

    def foreground_app_android(self):
        activity = self.get_capabilities()['appActivity']
        package = self.get_capabilities()['appPackage']
        try:
            self.driver.start_activity(app_package=package, app_activity=activity, intent_action="android.intent.action.MAIN", intent_category="android.intent.category.LAUNCHER", intent_flags="0x10200000", dont_stop_app_on_reset=True)
        except:
            pass

    ##### APP/DRIVER ACTIONS #####

    def tap(self, locator, timeout=10, count=1, offset_x=1, offset_y=1, log=True, wait=0, raise_exception=True, duration=50, num=0):
        if isinstance(locator, list):
            return self.tap_position(positions=locator, count=count, duration=duration, wait=wait, log=log)

        if isinstance(locator, WebElement):
            return locator.click()

        locator.tap(timeout=timeout, count=count, offset_x=offset_x, offset_y=offset_y, log=log, wait=wait, raise_exception=raise_exception, duration=duration, num=0)

    def hide_keyboard(self, checkmark=False, key_name=None):
        try:
            if self.is_android():
                if checkmark:
                    self.tap_keyboard_checkmark()
                else:
                    self.driver.press_keycode(66)
            else:
                try:
                    if key_name:
                        self.driver.hide_keyboard(key_name=key_name)

                except:
                    self.driver.hide_keyboard(key_name="Done")
        except:
            pass

    def tap_keyboard_checkmark(self):
        x, y = self.get_screen_size()
        self.tap_position(positions=[(x - 150, y - 100)], count=1)

    def tap_position(self, positions, count=1, duration=50, wait=0, log=True):
        if log:
            print("Performing a mobile {} taps at positions: {}".format(count, positions))
        for i in range(count):
            if duration == 0:
                duration = None

            self.driver.tap(positions, duration=duration)
            sleep(wait)

    def compare_locator_center_coordinates(self, locator_one, locator_two, pixel_variation=5):
        """
        Compare the center coordinates of the locators passed in
        :param locator_one: SlickMobileLocator
        :param locator_two: SlickMobileLocator
        :param pixel_variation:
        :return:
        """

        loc_one_x, loc_one_y = locator_one.get_coordinate_location()
        loc_two_x, loc_two_y = locator_two.get_coordinate_location()

        if loc_one_x - pixel_variation <= loc_two_x <= loc_one_x + pixel_variation:
            if loc_one_y - pixel_variation <= loc_two_y <= loc_one_y + pixel_variation:
                return True
            else:
                print("The first center y coordinate ({}) wasnt within {} pixels of the second center y coordinate ({}).".format(loc_one_y, pixel_variation, loc_two_y))
                return False
        else:
            "The first center x coordinate ({}) wasnt within {} pixels of the second center x coordinate ({}).".format(loc_one_x, pixel_variation, loc_two_x)
            return False

    def get_orientation(self):
        return self.driver.orientation

    def rotate(self):
        if self.get_orientation() != "PORTRAIT":
            self.rotate_portrait()
        else:
            self.rotate_landscape()

    def rotate_portrait(self):
        try:
            if self.get_orientation() != "PORTRAIT":
                self.driver.orientation = "PORTRAIT"

            return True
        except:
            return False

    def rotate_landscape(self):
        try:
            if self.get_orientation() != "LANDSCAPE":
                self.driver.orientation = "LANDSCAPE"

            return True
        except:
            return False

    def is_portrait(self):
        if self.get_orientation() == "PORTRAIT":
            return True
        return False

    def swipe(self, start_locator, end_locator, transitional_locator=None, add_x=10, add_y=10, wait=.5):
        try:
            start_element = start_locator.gimme().element
            end_element = end_locator.gimme().element
            touch_action = self.touch_action

            if self.is_android():
                touch_action.long_press(start_element, add_x, add_y)
                transitional_element = transitional_locator.gimme().element
                touch_action.move_to(transitional_element)
            else:
                touch_action.press(start_element, add_x, add_y)
            touch_action.wait(wait * 1000)
            touch_action.move_to(end_element, add_x, add_y)
            touch_action.release()
            touch_action.perform()
        except:
            pass

    def swipe_direction(self, start_locator, end_locator, transitional_locator=None, add_x=10, add_y=10, wait=.5):
        start_element = start_locator.gimme().element
        end_element = end_locator.gimme().element
        touch_action = self.touch_action

        if self.is_android():
            touch_action.long_press(start_element, add_x, add_y)
            transitional_element = transitional_locator.gimme().element
            touch_action.move_to(transitional_element)
        else:
            touch_action.press(start_element, add_x, add_y)
        touch_action.wait(wait * 1000)
        touch_action.move_to(end_element, add_x, add_y)
        touch_action.release()
        touch_action.perform()

    def swipe_by_coordinates(self, start_coordinates, end_coordinates, transitional_coordinates=None, wait=.5):
        touch_action = self.touch_action

        if self.is_android():
            if wait is not None:
                touch_action.long_press(x=start_coordinates[0], y=start_coordinates[1])
            else:
                touch_action.press(x=start_coordinates[0], y=start_coordinates[1])

            if transitional_coordinates:
                touch_action.move_to(x=transitional_coordinates[0], y=transitional_coordinates[1])
        else:
            # touch_action.press(x=start_coordinates[0], y=start_coordinates[1])
            touch_action.long_press(x=start_coordinates[0], y=start_coordinates[1], duration=(wait * 1000))
        if wait is not None:
            touch_action.wait(wait * 1000)

        touch_action.move_to(x=end_coordinates[0], y=end_coordinates[1])
        touch_action.release()
        touch_action.perform()

    def scroll_to_element(self, locator, direction="UP", amount=100, start_x=None, start_y=None, allowed=10, timeout=5):
        for i in range(allowed):
            if locator.is_displayed(timeout=timeout, log=False):
                return True

            self.flick(direction=direction, amount=amount, start_x=start_x, start_y=start_y)

        return False

    def flick(self, direction="UP", amount=100, start_x=None, start_y=None, swipe=False):
        middle_x, middle_y = self.get_middle_coords()

        if not start_x:
            start_x = middle_x

        if not start_y:
            start_y = middle_y

        direction = direction.upper()
        if direction == "UP":
            end_x = start_x
            end_y = start_y - amount
        elif direction == "RIGHT":
            end_x = start_x + amount
            end_y = start_y
        elif direction == "LEFT":
            end_x = start_x - amount
            end_y = start_y
        else:
            end_x = start_x
            end_y = start_y + amount

        if self.is_android():
            if swipe:
                self.driver.swipe(start_x, start_y, end_x, end_y, duration=100)
            else:
                self.driver.flick(start_x, start_y, end_x, end_y)

        else:
            self.driver.swipe(start_x, start_y, end_x, end_y, duration=100)

    # IMAGES/SCREENSHOTS/VIDEOS
    def get_text_from_locator(self, locator):
        import os
        filepath = None
        try:
            filepath = self.save_screenshot_of_locator(locator)
            return self.get_text_from_file(filepath)
        finally:
            if filepath is not None:
                os.remove(filepath)

    def get_text_from_file(self, filepath):
        from pyocr import tesseract, builders
        from PIL import Image
        image = Image.open(filepath)

        text = tesseract.image_to_string(image=image, builder=builders.TextBuilder())
        return text.strip('\r\n')

    def take_screenshot_of_locator(self, locator):
        locator_rect = locator.get_rect()
        actual_rect = self.get_actual_rect(locator_rect)
        screenshot = self.get_screenshot_blob()
        image = self.create_image_from_screenshot(screenshot)
        return SlickMobileApp.crop_image(image, actual_rect[0], actual_rect[1], actual_rect[2], actual_rect[3])

    def save_screenshot_of_locator(self, locator, filename="tmp_image_for_compare", version="tmp", directory="/local-repos/mobile/images"):
        cropped_image = self.take_screenshot_of_locator(locator)
        file_location = SlickMobileApp.save_image(cropped_image, filename, version, directory)
        return file_location

    def take_tmp_screenshot_for_compare(self, locator, filename="tmp_image_for_compare", version="tmp", remove=True):
        import os
        filepath = None
        try:
            filepath = self.save_screenshot_of_locator(locator=locator, filename=filename, version=version)
            return self.load_mobile_image(filename, version=version)
        finally:
            if filepath is not None and remove:
                os.remove(filepath)

    def save_screenshot(self, screenshot_blob):
        from utils import get_epoch_time
        if self.screenshot_dir is None:
            print("Screenshot directory is: {}".format(self.screenshot_dir))
            return

        if self.unique_screenshots and self.screenshot_blob == screenshot_blob:
            return

        self.screenshot_blob = screenshot_blob
        image_filepath = "{}/{}.png".format(self.screenshot_dir, get_epoch_time())
        SlickMobileApp.image = SlickMobileApp.create_image_from_screenshot(self.screenshot_blob)
        SlickMobileApp.image.save(filename=image_filepath)

    def load_mobile_image(self, filename, version, directory="/local-repos/mobile/images"):
        """
        Load a png file from a specified directory.
        :param filename: String
        :param version: String
        :param directory: String
        :return: Image
        """

        if self.is_simulator() and "ios" in version:
            temp = version.split("_")
            version = "{}_SIM_{}".format(temp[0], temp[1])

        filepath = "{}/{}-{}.png".format(directory, filename, version.upper())

        return SlickMobileApp.load_image(filepath=filepath)

    def get_screenshot_blob(self):
        try:
            return self.screenshot_as_byte()
        except Exception as e:
            raise Exception("Failed to get screenshot blob: {}".format(e.message))

    @staticmethod
    def create_screenshot_dir(screenshot_dir):
        import os
        if not os.path.isdir(screenshot_dir):
            os.makedirs(screenshot_dir)

    @staticmethod
    def remove_screenshots(screenshot_dir, extension="png"):
        import os
        import glob
        image_pattern = "{}/*.{}".format(screenshot_dir, extension)
        for item in glob.glob(image_pattern):
            os.remove(item)

    @staticmethod
    def create_image_from_screenshot(screenshot):
        from wand.image import Image
        image = Image(blob=screenshot, format="PNG")
        return image

    @staticmethod
    def get_image_size(image):
        from wand.image import Image
        if not isinstance(image, Image):
            raise Exception("Image are not instances of wand.Image")

        return float(image.width), float(image.height)

    @staticmethod
    def compare_images(image1, image2, greater_than=.99, less_than=100, metric='ssim'):
        from wand.image import Image
        if not isinstance(image1, Image) or not isinstance(image2, Image):
            raise Exception("Images are not instances of wand.Image")

        image1.type = "grayscale"
        image2.type = "grayscale"

        if image1.page_height != image2.page_height or image1.page_width != image2.page_width:
            print("#### Height and width did not match ####")
            print("Image1 page_height = {}, page_width = {}".format(image1.page_height, image1.page_width))
            print("Image2 page_height = {}, page_width = {}".format(image2.page_height, image2.page_width))
            return False, "Image dimensions were not the same"

        if metric == "ssim":
            is_same, value = SlickMobileApp.compare_images_ssim(image1, image2, greater_than)

        elif metric == "root_mean_square" or metric == "mse":
            is_same, value = SlickMobileApp.compare_images_root_mean_squared(image1, image2, less_than)

        else:
            return False, "{} is not a valid metric.".format(metric)

        return is_same, value

    @staticmethod
    def compare_images_ssim(image1, image2, greater_than):
        from skimage.measure import compare_ssim as ssim
        import cv2
        import numpy

        img1_buffer = numpy.asarray(bytearray(image1.make_blob()), dtype=numpy.uint8)
        retval1 = cv2.imdecode(img1_buffer, cv2.IMREAD_UNCHANGED)

        img2_buffer = numpy.asarray(bytearray(image2.make_blob()), dtype=numpy.uint8)
        retval2 = cv2.imdecode(img2_buffer, cv2.IMREAD_UNCHANGED)


        value = ssim(retval1, retval2)

        print("##### {} - IMAGE SSIM VALUE #####".format(value))

        # 1 is exact
        # Range 1 to -1
        if value == 1:
            is_same = True
        elif value > greater_than:
            is_same = True
        else:
            is_same = False

        return is_same, value

    @staticmethod
    def compare_images_root_mean_squared(image1, image2, less_than):

        value = image1.compare(image2, metric="root_mean_square")[1]

        print("###### {} - IMAGE ROOT MEAN SQUARED VALUE #####".format(value))

        # 0 is exact
        # Range 0 to infinity + 1
        if value == 0:
            is_same = True
        elif value < less_than:
            is_same = True
        else:
            is_same = False

        return is_same, value

    @staticmethod
    def crop_blob(blob, start_x, start_y, width, height):
        """
        :param blob: byte[]
        :param start_x: int
        :param start_y: int
        :param width: int
        :param height: int
        :return:
        """
        from wand.image import Image
        return SlickMobileApp.crop_image(Image(blob=blob), start_x, start_y, width, height)

    @staticmethod
    def crop_image(image, start_x, start_y, width, height):
        """
        :param image: Image
        :param start_x: int
        :param start_y: int
        :param width: int
        :param height: int
        :return:
        """
        from wand.image import Image
        if not isinstance(image, Image):
            raise Exception("Image is not instance of wand.Image")
        img = image
        img.normalize()

        left = start_x
        top = start_y
        img.crop(left=left, top=top, width=width, height=height)
        return img

    @staticmethod
    def load_image(filepath):
        """
        Load a png image from the filepath specified.
        :param filepath: String
        :return: Image
        """
        import os
        from wand.image import Image

        if not os.path.exists(filepath):
            raise Exception("Could not find the image: {}".format(filepath))

        f = open(filepath)
        return Image(file=f, format="png")

    @staticmethod
    def save_image(image, filename, version, directory="/local-repos/mobile/images"):
        """
        Saving the image to a specified directory
        :param image: wand.image.Image
        :param filename: String
        :param version: String
        :param directory: String
        :return:
        """

        import os
        from wand.image import Image
        if not isinstance(image, Image):
            raise Exception("Image is not instance of wand.Image")

        image_dir = directory
        if not os.path.isdir(image_dir):
            os.mkdir(image_dir)

        filepath = "{}/{}-{}.png".format(image_dir, filename, version.upper())
        image.save(filename=filepath)
        return filepath

    @staticmethod
    def get_video_encoding_command(image_directory, filepath, interval=2, image_type="png", video_codec="libx264",
                                   video_width="280", video_height="520"):
        """
        Generate the command for creating a video with ffmpeg
        :param image_directory:
        :param filepath:
        :param interval:
        :param image_type:
        :param video_codec:
        :param video_width:
        :param video_height:
        :return:
        """
        import os
        image_dir = image_directory
        if not os.path.isdir(image_dir):
            raise Exception("Directory could not be found: {}".format(image_directory))

        return "ffmpeg -pattern_type glob -r 1/{} -i '{}/*.{}' -s {}x{} -c:v {} -pix_fmt yuv420p -y {}".format(interval,
                                                                                                               image_directory,
                                                                                                               image_type,
                                                                                                               video_width,
                                                                                                               video_height,
                                                                                                               video_codec,
                                                                                                               filepath)

    @staticmethod
    def create_video_from_images(image_directory, filepath, interval=2, image_type="png", video_codec="libx264",
                                 video_width="280", video_height="520"):
        """
        Create a video from a set of images
        :param image_directory:
        :param filepath:
        :param interval:
        :param image_type:
        :param video_codec:
        :param video_width:
        :param video_height:
        :return:
        """
        import os
        import subprocess

        video_dir = os.path.dirname(filepath)
        if not os.path.isdir(video_dir):
            os.makedirs(video_dir)

        # FFMPEG MUST BE INSTALLED
        command = SlickMobileApp.get_video_encoding_command(image_directory, filepath, interval, image_type, video_codec,
                                                       video_width, video_height)
        print("### Creating the video file: {} ###".format(command))
        output = subprocess.check_call(command, shell=True)
        if output == 0:
            print("Created the video at: {}".format(filepath))
        else:
            raise Exception("Failed to create the video.")

    def cut(self, locator):
        """
        Select all from a locator and cut
        :param locator:
        :return:
        """
        if self.is_android():
            start_x, start_y, end_x, end_y = locator.get_rect()
            y = start_y + 2

            locator.tap()
            self.swipe_by_coordinates([start_x + 2, y], [end_x - 2, y])
            self.driver.keyevent(keycode=277)
            self.driver.keyevent(keycode=111)

        else:
            self.btn_cut = SlickMobileLocator("Cut text button", Find.by_name("Cut"))
            self.btn_select_all = SlickMobileLocator("select all button", Find.by_name("Select All"))

            locator.tap()
            if not self.btn_select_all.exists():
                locator.tap()

            self.btn_select_all.tap()
            self.btn_cut.tap()

    def copy(self, locator):
        """
        Select all from a locator and copy
        :param locator:
        :return:
        """
        if self.is_android():
            start_x, start_y, end_x, end_y = locator.get_rect()
            y = start_y + 2

            locator.tap()
            self.swipe_by_coordinates([start_x + 2, y], [end_x - 2, y])
            self.driver.keyevent(keycode=278)
            self.driver.keyevent(keycode=111)

        else:
            self.btn_copy = SlickMobileLocator("copy button", Find.by_name("Copy"))
            self.btn_select_all = SlickMobileLocator("select all button", Find.by_name("Select All"))

            locator.tap()
            if not self.btn_select_all.exists():
                locator.tap()

            self.btn_select_all.tap()
            self.btn_copy.tap()

    def paste(self, locator):
        """
        Paste into a locator
        :param locator:
        :return:
        """
        if self.is_android():
            touch_action = TouchAction(self.driver)

            locator.tap()

            touch_action.press(el=locator.element)
            touch_action.perform()

            sleep(3)

            touch_action.release()
            touch_action.perform()

            self.driver.keyevent(keycode=279)
            self.driver.keyevent(keycode=111)

        else:
            self.btn_paste = SlickMobileLocator("paste button", Find.by_name("Paste"))
            self.btn_select_all = SlickMobileLocator("select all button", Find.by_name("Select All"))

            locator.tap()
            locator.element.clear()

            if not self.btn_paste.exists():
                locator.tap()

            self.btn_paste.tap()