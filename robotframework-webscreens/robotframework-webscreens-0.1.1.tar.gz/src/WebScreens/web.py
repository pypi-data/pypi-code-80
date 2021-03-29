from .version import VERSION
from selenium import webdriver
from robot.libraries.BuiltIn import BuiltIn
from robot.api.deco import keyword
from robot.api import logger

class WebScreens():

    """
    WebScreens library helps in simulating different web screen resolutions by using selenium internally

    Available Resolutions:

        |  = Resolution Tye =  |    = Values =  |
        |  Desktop             |  2560*1440, 1920*1200, 1680*1050, 1600*1200, 1400*900, 1366*768, 1280*800, 1280*768, 1152*864, 1024*768, 800*600  |
        |  Tablet              |  768*1024, 1024*1366, 800*1280, 600*960  |
        |  Mobile              |  360*598, 412*684, 414*736, 375*667, 320*568, 320*480  |
    
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self):
        self.webdriver = None
        self.DESKTOP_RESOLUTIONS = ["2560*1440", "1920*1200", "1680*1050", "1600*1200", "1400*900",
         "1366*768", "1280*800", "1280*768", "1152*864", "1024*768", "800*600"]
        self.TABLET_RESOLUTIONS = ["768*1024", "1024*1366", "800*1280", "600*960"]
        self.SMARTPHONE_RESOLUTIONS = ["360*598", "412*684", "414*736", "375*667", "320*568", "320*480"]
    
    @keyword("Simulate Screen Resolutions")
    def simulate_screen_resolutions(self, app_url=None, resolution_type="Desktop", screenshot=True, revert=True):
        """
        Adjust webbrowser to set of resolutions, navigate to url and capture page screenshot.

        |  = Attributes =   |   = Description =  |
        |  app_url          |   Application url under test. Default is current page and user can pass respective URL  |
        |  resolution_type  |   Pre defined resolutions assigned to variable. They are ``Mobile``, ``Desktop`` and ``Tablet``  |
        |  screenshot       |   Capture screenshot after navigating to page. Default value is ``True``  |
        |  revert           |   Revert screen resolution to original resolution. Default value is ``True``  |

        Usage Example:

        |  = Keyword =  |  = Paramter =  |
        |  Simulate Screen Resolutions  |  resolution_type=Mobile  |
        |  Simulate Screen Resolutions  |  app_url=https://github.com/  |  resolution_type=Desktop  |  

        """
        # get selenium instance
        seleniumlib = BuiltIn().get_library_instance('SeleniumLibrary')

        # remember window size
        prev_width, prev_height = seleniumlib.get_window_size()
        
        if resolution_type.lower() == "desktop":
            resolution_list = self.DESKTOP_RESOLUTIONS
        elif resolution_type.lower() == "tablet":
            resolution_list = self.TABLET_RESOLUTIONS
        elif resolution_type.lower() == "mobile":
            resolution_list = self.SMARTPHONE_RESOLUTIONS
        else:
            BuiltIn().fail("Resolution: %s not found"%(resolution_type))
        
        # loop through resolutions list
        for items in resolution_list:
            BuiltIn().log("Simulating Resolution: %s" %(items) )
            try:
                width, height = items.split("*")
                # re-size for required
                seleniumlib.set_window_size(width, height)
                
                # reload page
                if app_url is None:
                    seleniumlib.reload_page()
                else:
                    url = app_url
                    seleniumlib.go_to(url)
                
                # capture full page screenshot - supports firefox only
                if screenshot:
                    seleniumlib.capture_element_screenshot("tag:body")
            
            except Exception as e:
                BuiltIn().log(e)
            
            finally:
                if revert:
                    seleniumlib.set_window_size(prev_width, prev_height)
                    seleniumlib.reload_page()

    @keyword("Simulate Screen Resolution")
    def simulate_screen_resolution(self, width, height, app_url=None, screenshot=True, revert=True):
        """
        Adjust webbrowser to given resolution (width * height), navigate to url and capture page screenshot.

        |  = Attributes =   |   = Description =  |
        |  width            |   Browser width  |
        |  height           |   Browser height  |
        |  app_url          |   Application url under test. Default is current page and user can pass respective URL  |
        |  screenshot       |   Capture screenshot after navigating to page. Default value is ``True``  |
        |  revert           |   Revert screen resolution to original resolution. Default value is ``True``  |


        Usage Example:

        |  = Keyword =  |  = Paramter =  |
        |  Simulate Screen Resolution  |  800  |  760  |
        |  Simulate Screen Resolution  |  800  |  760  |  app_url=https://github.com/  |  screenshot=False  |  

        """
        # get selenium instance
        seleniumlib = BuiltIn().get_library_instance('SeleniumLibrary')

        # remember window size
        prev_width, prev_height = seleniumlib.get_window_size()
        try:
            # re-size for required
            seleniumlib.set_window_size(width, height)
            
            # reload page
            if app_url is None:
                seleniumlib.reload_page()
            else:
                url = app_url
                seleniumlib.go_to(url)
            
            # capture full page screenshot
            if screenshot:
                seleniumlib.capture_element_screenshot("tag:body")
        
        except Exception as e:
            BuiltIn().log(e)
        
        finally:
            if revert:
                seleniumlib.set_window_size(prev_width, prev_height)
                seleniumlib.reload_page()