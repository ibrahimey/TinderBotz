from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import re
from tinderbotz.helpers.xpaths import content
from datetime import datetime

class GeomatchHelper:

    delay = 5

    HOME_URL = "https://www.tinder.com/app/recs"

    def __init__(self, browser):
        self.browser = browser
        if "/app/recs" not in self.browser.current_url:
            self._get_home_page()

    def like(self)->bool:
        try:
            # need to find better way
            #if 'profile' in self.browser.current_url:
            #    xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[4]/button'

                # wait for element to appear
            #    WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
            #        (By.XPATH, xpath)))

                # locate like button
            #    like_button = self.browser.find_element(By.XPATH, xpath)

            #    like_button.click()

            #else:
            #    xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]'

            #    WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
            #        (By.XPATH, xpath)))

             #   card = self.browser.find_element(By.XPATH, xpath)

            #    action = ActionChains(self.browser)
           #    action.drag_and_drop_by_offset(card, 200, 0).perform()

            action = ActionChains(self.browser)
            action.send_keys(Keys.ARROW_RIGHT).perform()
            #time.sleep(1)
            return True

        except (TimeoutException, ElementClickInterceptedException):
            self._get_home_page()

        return False

    def dislike(self):
        try:
            #if 'profile' in self.browser.current_url:
            #    xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[2]/button'
                # wait for element to appear
            #    WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
            #        (By.XPATH, xpath)))

            #    dislike_button = self.browser.find_element(By.XPATH, xpath)

            #    dislike_button.click()
            #else:

            #    xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]'

            #    WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
            #        (By.XPATH, xpath)))

            #    card = self.browser.find_element(By.XPATH, xpath)

            #    action = ActionChains(self.browser)
            #    action.drag_and_drop_by_offset(card, -200, 0).perform()
            
            action = ActionChains(self.browser)
            action.send_keys(Keys.ARROW_LEFT).perform()

            #time.sleep(1)
        except (TimeoutException, ElementClickInterceptedException):
            self._get_home_page()

    def superlike(self):
        try:
            if 'profile' in self.browser.current_url:
                xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[2]/div/div/div[3]/div/div/div/button'

                # wait for element to appear
                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

                superlike_button = self.browser.find_element(By.XPATH, xpath)

                superlike_button.click()

            else:
                xpath = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]'

                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                    (By.XPATH, xpath)))

                card = self.browser.find_element(By.XPATH, xpath)

                action = ActionChains(self.browser)
                action.drag_and_drop_by_offset(card, 0, -200).perform()

            time.sleep(1)

        except (TimeoutException, ElementClickInterceptedException):
            self._get_home_page()

    def _open_profile(self, second_try=False):
        if self._is_profile_opened(): return;
        try:
            #xpath = '//button'
            #WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
            #    (By.XPATH, xpath)))
            #buttons = self.browser.find_elements(By.XPATH, xpath)

            #for button in buttons:
            #    # some buttons might not have a span as subelement
            #    try:
            #        text_span = button.find_element(By.XPATH, './/span').text
            #        if 'open profile' in text_span.lower():
            #            button.click()
            #            break
            #    except:
            #        continue

            # New Implementation
            action = ActionChains(self.browser)
            action.send_keys(Keys.ARROW_UP).perform()

            #time.sleep(1)

        except (ElementClickInterceptedException, TimeoutException):
            if not second_try:
                print("Trying again to locate the profile info button in a few seconds")
                time.sleep(2)
                self._open_profile(second_try=True)
            else:
                self.browser.refresh()
        except:
            self.browser.get(self.HOME_URL)
            if not second_try:
                self._open_profile(second_try=True)

    def get_name(self):
        if not self._is_profile_opened():
            self._open_profile()

        try:
            # xpath = '//main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/h1/span[1]'
            # '//main/div/div/div/div/div[2]/button/div/div/div/div/div[1]/div/div/span'
            # wait for element to appear
            # WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))

            #element = self.browser.find_element(By.XPATH, xpath)
            # element = self.browser.find_elements(By.CSS_SELECTOR, "span[itemprop='name']")[-1]
            time.sleep(0.1) # TODO: instead of sleep try this wait for element thingy
            element = self.browser.find_element(By.CSS_SELECTOR, "span[class='Pend(8px)']")
            name = element.text

            return name
        except NoSuchElementException:
            # TODO: This part probably does not work or maybe it should also have try except
            element = self.browser.find_elements(By.CSS_SELECTOR, "span[itemprop='name']")[-1]
            name = element.text

            return name
        except Exception as e:
            pass

    def get_age(self):
        if not self._is_profile_opened():
            self._open_profile()

        age = None

        try:
            # xpath = '//main/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div/h1/span[2]'
            # time.sleep(0.2)
            # wait for element to appear
            # WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))

            # element = self.browser.find_element(By.XPATH, xpath)
            
            element = self.browser.find_element(By.CSS_SELECTOR, "span[class='Whs(nw) Typs(display-2-strong)']")
            try:
                age = int(element.text)
            except ValueError:
                age = None

        except Exception as e:
            pass

        return age

    def is_verified(self):
        if not self._is_profile_opened():
            self._open_profile()

        xpath_badge = f'{content}/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[2]'
        try:
            self.browser.find_element(By.XPATH, xpath_badge)
            return True

        except:
            return False

    _WORK_SVG_PATH = "M16.995 4.37A2.37 2.37 0 0 0 14.625 2h-5.25a2.37 2.37 0 0 0-2.37 2.37v1.635h-5.5C.677 6.005 0 6.677 0 7.505v11.99c0 .828.677 1.5 1.505 1.5h20.99a1.5 1.5 0 0 0 1.5-1.5V7.505a1.5 1.5 0 0 0-1.5-1.5h-5.5zm-7.62-.375A.375.375 0 0 0 9 4.37v1.635h6V4.37a.375.375 0 0 0-.375-.375zM21.625 8c.207 0 .375.168.375.375v10.25a.375.375 0 0 1-.375.375H18.99V8zM2 8.375C2 8.168 2.168 8 2.375 8H5.01v11H2.375A.375.375 0 0 1 2 18.625zM7.005 19h9.99V8h-9.99z"
    _STUDYING_SVG_PATH = "M11.171 4.182a1.975 1.975 0 0 1 1.658 0l10.578 4.883c.79.365.79 1.505 0 1.87L20 12.507v4.903a2 2 0 0 1-1.02 1.744l-.607.341a13 13 0 0 1-12.746 0l-.608-.341A2 2 0 0 1 4 17.41v-4.902l-1-.462V14a1 1 0 1 1-2 0v-2.877l-.407-.188c-.79-.365-.79-1.505 0-1.87zm1.658 11.636 4.848-2.238H18v3.83l-.607.342a11 11 0 0 1-10.786 0L6 17.41v-3.83h.323l4.848 2.238a1.977 1.977 0 0 0 1.658 0M20.593 10 12 6.033 3.406 10 12 13.967z"
    _HOME_SVG_PATH = "M2.25 10.005H3v10.5a1.5 1.5 0 0 0 1.5 1.5h15a1.5 1.5 0 0 0 1.5-1.5v-10.5h.75c.72 0 1.027-.918.45-1.35L12.9 1.68a1.5 1.5 0 0 0-1.8 0L1.8 8.655c-.577.432-.27 1.35.45 1.35M12 3.499 5.985 8.01h12.03zM4.995 20.01V10.005H19V20.01h-3.002v-5.69c0-.716-.581-1.297-1.298-1.297H9.3c-.717 0-1.297.58-1.297 1.297v5.69zm9.008 0H10l-.002-4.992h4.005z"
    _LOCATION_SVG_PATH_2 = "M11.445 12.5a2.945 2.945 0 0 1-2.721-1.855 3.04 3.04 0 0 1 .641-3.269 2.905 2.905 0 0 1 3.213-.645 3.003 3.003 0 0 1 1.813 2.776c-.006 1.653-1.322 2.991-2.946 2.993zm0-5.544c-1.378 0-2.496 1.139-2.498 2.542 0 1.404 1.115 2.544 2.495 2.546a2.52 2.52 0 0 0 2.502-2.535 2.527 2.527 0 0 0-2.499-2.545v-.008z"
    _LOCATION_SVG_PATH = "M12.301 23.755c.746-.659 9.449-8.339 9.449-14.337C21.75 4.138 17.463 0 11.998 0 6.534 0 2.25 4.138 2.25 9.418c0 2.675 1.602 5.91 4.769 9.616a45.204 45.204 0 0 0 4.737 4.759l.246.207.26-.21zm-.305-2.424c.94-.889 2.376-2.32 3.77-4.011 1.084-1.315 2.105-2.741 2.847-4.152.753-1.433 1.142-2.705 1.142-3.75 0-4.113-3.328-7.423-7.757-7.423-4.428 0-7.753 3.309-7.753 7.423 0 1.941 1.208 4.713 4.29 8.319a42.901 42.901 0 0 0 3.461 3.594"
    _GENDER_SVG_PATH = "M12 21.994h.034c1.918.033 3.76-.191 5.157-.631 1.492-.47 1.964-1.013 2.056-1.23.004-.026.016-.156-.076-.444-.123-.382-.383-.884-.806-1.472-.846-1.175-2.142-2.411-3.473-3.341l-1.05-.735a1 1 0 0 1-.083-1.574l.968-.84c.684-.594 1.462-1.935 1.462-5.2C16.19 4.042 14.285 2.096 12 2c-2.285.096-4.19 2.042-4.19 4.525 0 3.266.78 4.607 1.463 5.2l.968.84a1 1 0 0 1-.083 1.575l-1.05.735c-1.33.93-2.626 2.166-3.473 3.34-.423.589-.683 1.091-.806 1.473-.092.288-.08.418-.076.444.092.217.564.76 2.056 1.23 1.397.44 3.24.664 5.157.631zm9.118-1.154c-.85 2.205-4.981 3.224-9.118 3.154-4.137.07-8.268-.949-9.118-3.154-.647-1.678 1.179-4.311 3.49-6.35a18.08 18.08 0 0 1 1.59-1.254 5.075 5.075 0 0 1-1.21-1.594c-.596-1.196-.941-2.85-.941-5.116C5.81 2.982 8.566.097 12 0c3.434.097 6.19 2.982 6.19 6.526 0 2.266-.346 3.92-.943 5.116a5.073 5.073 0 0 1-1.209 1.595c.54.377 1.077.8 1.59 1.253 2.311 2.039 4.137 4.672 3.49 6.35"
    _HEIGHT_SVG_PATH = "M16.95 0a1 1 0 0 1 .707.293l6.05 6.05a1 1 0 0 1 0 1.414l-15.95 15.95a1 1 0 0 1-1.414 0l-6.05-6.05a1 1 0 0 1 0-1.414L16.243.293A1 1 0 0 1 16.95 0M2.414 16.95l4.636 4.636 1.116-1.116-2.318-2.318a1 1 0 1 1 1.414-1.414l2.318 2.317 1.308-1.308-1.15-1.15a1 1 0 1 1 1.414-1.415l1.15 1.151 1.309-1.308-2.318-2.318a1 1 0 0 1 1.414-1.414l2.318 2.318 1.308-1.308-1.151-1.152a1 1 0 0 1 1.414-1.414l1.151 1.151 1.308-1.308-2.317-2.318a1 1 0 0 1 1.414-1.414l2.318 2.318 1.116-1.116-4.636-4.636z"
    _SEXUALITY_SVG_PATH = "M10.077 18.153a8.076 8.076 0 1 0 0-16.153 8.076 8.076 0 0 0 0 16.153m0 2c5.565 0 10.076-4.511 10.076-10.076C20.153 4.51 15.642 0 10.077 0 4.51 0 0 4.511 0 10.077c0 5.565 4.511 10.076 10.077 10.076"


    def get_row_data(self):

        if not self._is_profile_opened():
            self._open_profile()

        rowdata = {}

        xpath = '//div[@class="Row"]'
        rows = self.browser.find_elements(By.XPATH, xpath)

        for row in rows:
            svg = row.find_element(By.XPATH, ".//*[starts-with(@d, 'M')]").get_attribute('d')
            value = row.find_element(By.XPATH, ".//div[2]").text
            if svg == self._WORK_SVG_PATH:
                rowdata['work'] = value
            if svg == self._STUDYING_SVG_PATH:
                rowdata['study'] = value
            if svg == self._HOME_SVG_PATH:
                rowdata['home'] = value.split(' ')[-1]
            if svg == self._GENDER_SVG_PATH:
                rowdata['gender'] = value
            if svg == self._HEIGHT_SVG_PATH:
                rowdata['height'] = value
            if svg == self._SEXUALITY_SVG_PATH:
                rowdata['sexuality'] = value
            if svg == self._LOCATION_SVG_PATH or svg == self._LOCATION_SVG_PATH_2:
                distance = value.split(' ')[0]
                try:
                    distance = int(distance)
                except TypeError:
                    # Means the text has a value of 'Less than 1 km away'
                    distance = 1
                except ValueError:
                    distance = None

                rowdata['distance'] = distance

        return rowdata

    def get_bio_and_passions(self):
        if not self._is_profile_opened():
            self._open_profile()

        bio = None
        looking_for = None

        infoItemsDict = {
            "lifestyle": {},
            "basics": {}
        }

        # Can also add pronouns idj if there are any more sections
        infoItemsList = {
            "passions": [],
            "languages i know": [],
            "relationship type": []
        }

        anthem = None

        # Bio
        try:
            bio = self.browser.find_element(By.CSS_SELECTOR, 'section[class*="Px(16px) Py(12px) Us(t)"] > div').text
            # bio = self.browser.find_element(By.XPATH, '//main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/section[1]/div').text

        except Exception as e:
            pass

        # Looking for
        try:
            looking_for_el = self.browser.find_element(By.CSS_SELECTOR, 'div[class="Px(16px) My(12px)"]>div[class="D(b)"]')
            looking_for = looking_for_el.find_element(By.CSS_SELECTOR, 'div[class="Typs(subheading-1) CenterAlign"]').text

        except Exception as e:
            pass

        # Basics, Lifestyle and Passions
        try:
            sections = self.browser.find_elements(By.CSS_SELECTOR, "div[class='Px(16px) Py(12px)']")

            for section in sections:
                headline = section.find_element(By.TAG_NAME, "h2").text.lower()
                
                if headline in infoItemsDict.keys():
                    infoElements = section.find_elements(By.CSS_SELECTOR, "div[class^='Bdrs(100px)']")
                    for infoElement in infoElements:
                        # TODO: handle when there is +1 more
                        key = infoElement.find_element(By.TAG_NAME, "span").get_attribute("textContent").lower()
                        if key:
                            infoItemsDict[headline][key]= infoElement.text
                        else:
                            infoItemsDict[headline][infoElement.text] = infoElement.text
                elif headline in infoItemsList.keys():
                    infoElements = section.find_elements(By.CSS_SELECTOR, "div[class^='Bdrs(100px)']")
                    for infoElement in infoElements:
                        infoItemsList[headline].append(infoElement.text)
                elif headline == 'my anthem':
                    song = section.find_element(By.XPATH, "//main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/section[2]/div/div/div[1]/div[1]").text
                    artist = section.find_element(By.XPATH, "//main/div[1]/div/div/div/div[1]/div[1]/div/div[2]/section[2]/div/div/div[1]/div[2]/span']").text
                    anthem = {
                        "song": song,
                        "artist": artist
                    }
                else:
                    print("Unknown Sect Headline:", headline)

        except Exception as e:
            pass

        try:
            sections = self.browser.find_elements(By.CSS_SELECTOR, "section[class='Px(16px) Py(12px)']")

            for section in sections:
                headline = section.find_element(By.TAG_NAME, "h2").text.lower()

                if headline in infoItemsDict.keys():
                    infoElements = section.find_elements(By.CSS_SELECTOR, "li[class^='Bdrs(100px)']")
                    for infoElement in infoElements:
                        # TODO: handle when there is +1 more
                        key = infoElement.find_element(By.TAG_NAME, "span").get_attribute("textContent").lower()
                        if key:
                            infoItemsDict[headline][key] = infoElement.text
                        else:
                            infoItemsDict[headline][infoElement.text] = infoElement.text
                elif headline in infoItemsList.keys():
                    infoElements = section.find_elements(By.CSS_SELECTOR, "li[class^='Bdrs(100px)']")
                    for infoElement in infoElements:
                        infoItemsList[headline].append(infoElement.text)
                elif headline == 'my anthem':
                    song = section.find_element(By.CSS_SELECTOR, "div[class*='Mb(4px) Ell']").text
                    artist = section.find_element(By.CSS_SELECTOR, "span[class*='Mstart(4px)']").text
                    anthem = {
                        "song": song,
                        "artist": artist
                    }
                else:
                    print("Unknown Sect Headline:", headline)

        except Exception as e:
            pass

        infoItems = infoItemsList | infoItemsDict

        return bio, infoItems["passions"], infoItems["lifestyle"], infoItems["basics"], infoItems["languages i know"], infoItems["relationship type"], anthem, looking_for

    def get_image_urls_new(self):
        if not self._is_profile_opened():
            self._open_profile()

        image_urls = []
        len_pics = len(self.browser.find_elements(By.XPATH, "//main/div[1]/div/div/div/div[1]/div[1]/div/div[1]/span/div/div[1]/div"))


        for i in range(1, len_pics + 1):
            # Get the url of image
            try:
                xpath = f"//main/div[1]/div/div/div/div[1]/div[1]/div/div[1]/span/div/div[1]/div[{i}]/div/div"
                WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
                element = self.browser.find_element(By.XPATH, xpath)

                image_url = element.value_of_css_property('background-image').split('\"')[1]
                image_urls.append(image_url)
            except NoSuchElementException:
                print('Could not find image, skipping')
            except Exception as e:
                print(e)

            action = ActionChains(self.browser)
            action.send_keys(Keys.SPACE).perform()
            time.sleep(0.1)

        return image_urls


    def get_image_urls(self, quickload=True):
        if not self._is_profile_opened():
            self._open_profile()

        image_urls = []

        # only get url of first few images, and not click all bullets to get all image
        elements = self.browser.find_elements(By.XPATH, "//div[@aria-label='Profile slider']")
        for element in elements:
            image_url = element.value_of_css_property('background-image').split('\"')[1]
            if image_url not in image_urls:
                image_urls.append(image_url)

        # return image urls without opening all images
        if quickload:
            return image_urls

        try:
            # There are no bullets when there is only 1 image
            classname = 'bullet'

            # wait for element to appear
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located(
                (By.CLASS_NAME, classname)))

            image_btns = self.browser.find_elements_by_class_name(classname)

            for btn in image_btns:
                btn.click()
                time.sleep(1)

                elements = self.browser.find_elements(By.XPATH, "//div[@aria-label='Profile slider']")
                for element in elements:
                    image_url = element.value_of_css_property('background-image').split('\"')[1]
                    if image_url not in image_urls:
                        image_urls.append(image_url)

        except StaleElementReferenceException:
            pass

        except TimeoutException:
            # there is only 1 image, so no bullets to iterate through
            try:
                element = self.browser.find_element(By.XPATH, "//div[@aria-label='Profile slider']")
                image_url = element.value_of_css_property('background-image').split('\"')[1]
                if image_url not in image_urls:
                    image_urls.append(image_url)

            except Exception as e:
                print("unhandled Exception when trying to store their only image")
                print(e)

        except Exception as e:
            print("unhandled exception getImageUrls in geomatch_helper")
            print(e)

        return image_urls

    @staticmethod
    def de_emojify(text):
        """Remove emojis from a string
        Args:
            text (string): string with emojis or not
        Returns:
            string: recompile string without emojis
        """
        regrex_pattern = re.compile(
            pattern="["
                    u"\U0001F600-\U0001F64F"  # emoticons
                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    "]+",
            flags=re.UNICODE,
        )
        return regrex_pattern.sub(r'', text)

    def get_insta(self, text):
        """Take the bio and read line by line to match if the description
        contain an instagram user.
        Args:
            text (string): string with emojis or not
        Returns:
            ig (string): return valid instagram user.
        """
        if not text:
            return None
        valid_pattern = [
            "@",
            "ig-",
            "ig",
            "ig:",
            "ing",
            "ing:",
            "instag",
            "instag:",
            "insta:",
            "insta",
            "inst",
            "inst:",
            "instagram",
            "instagram:",
        ]
        description = text.rstrip().lower().strip()
        description = description.split()
        for x in range(len(description)):
            ig = self.de_emojify(description[x])
            if '@' in ig:
                return ig.replace('@', '')
            elif ig in valid_pattern:
                try:
                    if ':' in description[x + 1]:
                        return description[x + 2]
                    else:
                        return description[x + 1]
                except:
                    return None
            else:
                try:
                    ig = ig.split(':', 1)
                    if ig[0] in valid_pattern:
                        return ig[-1]
                except:
                    return None
        return None

    def _get_home_page(self):
        self.browser.get(self.HOME_URL)
        time.sleep(5)

    def _is_profile_opened(self):
        if '/profile' in self.browser.current_url:
            return True
        else:
            return False
