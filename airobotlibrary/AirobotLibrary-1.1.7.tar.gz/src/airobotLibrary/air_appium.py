from AppiumLibrary import AppiumLibrary
from airtest.core.settings import Settings as ST
import allure


if not hasattr(ST, 'REMOTE_URL'): ST.REMOTE_URL = None

class AirAppium(AppiumLibrary):
    def __init__(self, timeout=5):
        super(AirAppium, self).__init__(timeout=timeout)

    @allure.step
    def open_application(self, remote_url=ST.REMOTE_URL, alias=None, **kwargs):
        return super(AirAppium, self).open_application(remote_url=remote_url, alias=alias, **kwargs)

    @allure.step
    def close_application(self):
        return super(AirAppium, self).close_application()

    @allure.step
    def close_all_applications(self):
        return super(AirAppium, self).close_all_applications()

    @allure.step
    def switch_application(self, index_or_alias):
        return super(AirAppium, self).switch_application(index_or_alias=index_or_alias)

    @allure.step
    def switch_to_context(self, context_name):
        return super(AirAppium, self).switch_to_context(context_name=context_name)

    @allure.step
    def go_back(self):
        return super(AirAppium, self).go_back()

    @allure.step
    def press_keycode(self, keycode, metastate=None):
        return super(AirAppium, self).press_keycode(keycode=keycode, metastate=metastate)

    @allure.step
    def scroll(self, start_locator, end_locator):
        return super(AirAppium, self).scroll(start_locator=start_locator, end_locator=end_locator)
    
    @allure.step
    def scroll_down(self, locator):
        return super(AirAppium, self).scroll_down(locator=locator)

    @allure.step
    def scroll_up(self, locator):
        return super(AirAppium, self).scroll_up(locator=locator)

    @allure.step
    def click_a_point(self, x=0, y=0, duration=100):
        return super(AirAppium, self).click_a_point(x=x, y=y, duration=duration)

    @allure.step
    def click_element(self, locator):
        return super(AirAppium, self).click_element(locator=locator)

    @allure.step
    def click_button(self, index_or_name):
        return super(AirAppium, self).click_button(index_or_name=index_or_name)

    @allure.step
    def click_text(self, text, exact_match=False):
        return super(AirAppium, self).click_text(text=text, exact_match=exact_match)

    @allure.step
    def long_press(self, locator, duration=1000):
        return super(AirAppium, self).long_press(locator=locator, duration=duration)

    @allure.step
    def long_press_keycode(self, keycode, metastate=None):
        return super(AirAppium, self).long_press_keycode(keycode=keycode, metastate=metastate)

    @allure.step
    def input_text(self, locator, text):
        return super(AirAppium, self).input_text(locator=locator, text=text)

    @allure.step
    def input_password(self, locator, text):
        return super(AirAppium, self).input_password(locator=locator, text=text)

    @allure.step
    def input_value(self, locator, text):
        return super(AirAppium, self).input_value(locator=locator, text=text)

    @allure.step
    def install_app(self, app_path, app_package):
        return super(AirAppium, self).install_app(app_path=app_path, app_package=app_package)

    @allure.step
    def shake(self):
        return super(AirAppium, self).shake()

    @allure.step
    def swipe(self, start_x, start_y, offset_x, offset_y, duration=1000):
        return super(AirAppium, self).swipe(start_x=start_x, start_y=start_y, offset_x=offset_x, offset_y=offset_y, duration=duration)

    @allure.step
    def tap(self, locator, x_offset=None, y_offset=None, count=1):
        return super(AirAppium, self).tap(locator=locator, x_offset=x_offset, y_offset=y_offset, count=count)

    @allure.step
    def touch_id(self, match=True):
        return super(AirAppium, self).touch_id(match=match)

    @allure.step
    def pinch(self, locator, percent="200%", steps=1):
        return super(AirAppium, self).pinch(locator=locator, percent=percent, steps=steps)

    @allure.step
    def page_should_contain_text(self, text, loglevel='INFO'):
        return super(AirAppium, self).page_should_contain_text(text=text, loglevel=loglevel)

    @allure.step
    def page_should_contain_element(self, locator, loglevel='INFO'):
        return super(AirAppium, self).page_should_contain_element(locator=locator, loglevel=loglevel)

    @allure.step
    def page_should_not_contain_element(self, locator, loglevel='INFO'):
        return super(AirAppium, self).page_should_not_contain_element(locator=locator, loglevel=loglevel)
    
    @allure.step
    def page_should_not_contain_text(self, text, loglevel='INFO'):
        return super(AirAppium, self).page_should_not_contain_text(text=text, loglevel=loglevel)

    def capture_page_screenshot(self, filename=None):
        file = super(AirAppium, self).capture_page_screenshot(filename=filename)
        with open(file, 'rb') as fp:
            allure.attach(fp.read(), '截图{}'.format(filename or ''), allure.attachment_type.PNG)
        return file

    def _get_log_dir(self):
        return ST.LOG_DIR

    def _run_on_failure(self):
        if self._run_on_failure_keyword is None:
            return
        if self._running_on_failure_routine:
            return
        self._running_on_failure_routine = True
        try:
            self.capture_page_screenshot()
        except Exception as err:
            self._run_on_failure_error(err)
        finally:
            self._running_on_failure_routine = False

    def _click_element_by_name(self, name):
        driver = self._current_application()
        try:
            element = driver.find_element_by_name(name)
        except Exception as e:
            raise e

        try:
            element.click()
        except Exception as e:
            raise Exception('Cannot click the element with name "%s"' % name)

    def _find_element_by_class_name(self, class_name, index_or_name):
        elements = self._find_elements_by_class_name(class_name)

        if self._is_index(index_or_name):
            try:
                index = int(index_or_name.split('=')[-1])
                element = elements[index]
            except (IndexError, TypeError):
                raise Exception('Cannot find the element with index "%s"' % index_or_name)
        else:
            found = False
            for element in elements:
                self._info("'%s'." % element.text)
                if element.text == index_or_name:
                    found = True
                    break
            if not found:
                raise Exception('Cannot find the element with name "%s"' % index_or_name)

        return element

    def _click_element_by_class_name(self, class_name, index_or_name):
        element = self._find_element_by_class_name(class_name, index_or_name)
        self._info("Clicking element '%s'." % element.text)
        try:
            element.click()
        except Exception as e:
            raise Exception('Cannot click the %s element "%s"' % (class_name, index_or_name))

    def _element_input_text_by_class_name(self, class_name, index_or_name, text):
        try:
            element = self._find_element_by_class_name(class_name, index_or_name)
        except Exception as e:
            raise e

        self._info("input text in element as '%s'." % element.text)
        try:
            element.send_keys(text)
        except Exception as e:
            raise Exception('Cannot input text "%s" for the %s element "%s"' % (text, class_name, index_or_name))
