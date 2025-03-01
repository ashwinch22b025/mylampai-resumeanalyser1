# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import getpass
import requests
from time import sleep
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# ------------------------------
# Existing LinkedIn Scraper Code (unchanged)
# ------------------------------

# Set your LinkedIn credentials as environment variables (recommended)
email = os.getenv("LINKEDIN_USER")  # or "your_email@example.com"
password = os.getenv("LINKEDIN_PASSWORD")  # or "your_password"
VERIFY_LOGIN_ID = "global-nav__primary-link"
REMEMBER_PROMPT = 'remember-me-prompt__form-primary'
NAME = 'text-heading-xlarge'

def __prompt_email_password():
    u = input("Email: ")
    p = getpass.getpass(prompt="Password: ")
    return (u, p)

def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'

def login(driver, email=None, password=None, cookie = None, timeout=10):
    if cookie is not None:
        return _login_with_cookie(driver, cookie)
  
    if not email or not password:
        email, password = __prompt_email_password()
  
    driver.get("https://www.linkedin.com/login")
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
  
    email_elem = driver.find_element(By.ID,"username")
    email_elem.send_keys(email)
  
    password_elem = driver.find_element(By.ID,"password")
    password_elem.send_keys(password)
    password_elem.submit()
  
    if driver.current_url == 'https://www.linkedin.com/checkpoint/lg/login-submit':
        remember = driver.find_element(By.ID,REMEMBER_PROMPT)
        if remember:
            remember.submit()
  
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME,VERIFY_LOGIN_ID)))
  
def _login_with_cookie(driver, cookie):
    driver.get("https://www.linkedin.com/login")
    driver.add_cookie({
      "name": "li_at",
      "value": cookie
    })

###############
@dataclass
class Contact:
    name: str = None
    occupation: str = None
    url: str = None

@dataclass
class Institution:
    institution_name: str = None
    linkedin_url: str = None
    website: str = None
    industry: str = None
    type: str = None
    headquarters: str = None
    company_size: int = None
    founded: int = None

@dataclass
class Experience(Institution):
    from_date: str = None
    to_date: str = None
    description: str = None
    position_title: str = None
    duration: str = None
    location: str = None

@dataclass
class Education(Institution):
    from_date: str = None
    to_date: str = None
    description: str = None
    degree: str = None

@dataclass
class Interest(Institution):
    title = None

@dataclass
class Accomplishment(Institution):
    category = None
    title = None

@dataclass
class Scraper:
    driver: Chrome = None
    WAIT_FOR_ELEMENT_TIMEOUT = 5
    TOP_CARD = "pv-top-card"

    @staticmethod
    def wait(duration):
        sleep(int(duration))

    def focus(self):
        self.driver.execute_script('alert("Focus window")')
        self.driver.switch_to.alert.accept()

    def mouse_click(self, elem):
        action = webdriver.ActionChains(self.driver)
        action.move_to_element(elem).perform()

    def wait_for_element_to_load(self, by=By.CLASS_NAME, name="pv-top-card", base=None):
        base = base or self.driver
        return WebDriverWait(base, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located((by, name))
        )

    def wait_for_all_elements_to_load(self, by=By.CLASS_NAME, name="pv-top-card", base=None):
        base = base or self.driver
        return WebDriverWait(base, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_all_elements_located((by, name))
        )

    def is_signed_in(self):
        try:
            WebDriverWait(self.driver, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, VERIFY_LOGIN_ID))
            )
            self.driver.find_element(By.CLASS_NAME, VERIFY_LOGIN_ID)
            return True
        except Exception as e:
            pass
        return False

    def scroll_to_half(self):
        self.driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_class_name_element_to_page_percent(self, class_name: str, page_percent: float):
        self.driver.execute_script(f'elem = document.getElementsByClassName("{class_name}")[0]; elem.scrollTo(0, elem.scrollHeight*{str(page_percent)});')

    def __find_element_by_class_name__(self, class_name):
        try:
            self.driver.find_element(By.CLASS_NAME, class_name)
            return True
        except:
            pass
        return False

    def __find_element_by_xpath__(self, tag_name):
        try:
            self.driver.find_element(By.XPATH, tag_name)
            return True
        except:
            pass
        return False

    def __find_enabled_element_by_xpath__(self, tag_name):
        try:
            elem = self.driver.find_element(By.XPATH, tag_name)
            return elem.is_enabled()
        except:
            pass
        return False

    @classmethod
    def __find_first_available_element__(cls, *args):
        for elem in args:
            if elem:
                return elem[0]

###############
class Person(Scraper):

    __TOP_CARD = "main"
    __WAIT_FOR_ELEMENT_TIMEOUT = 5

    def __init__(
        self,
        linkedin_url=None,
        name=None,
        about=None,
        experiences=None,
        educations=None,
        interests=None,
        accomplishments=None,
        company=None,
        job_title=None,
        contacts=None,
        driver=None,
        get=True,
        scrape=True,
        close_on_complete=True,
        time_to_wait_after_login=0,
    ):
        self.linkedin_url = linkedin_url
        self.name = name
        self.about = about or []
        self.experiences = experiences or []
        self.educations = educations or []
        self.interests = interests or []
        self.accomplishments = accomplishments or []
        self.also_viewed_urls = []
        self.contacts = contacts or []

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(os.path.dirname(__file__), "drivers/chromedriver")
                else:
                    driver_path = os.getenv("CHROMEDRIVER")
                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        if get:
            driver.get(linkedin_url)

        self.driver = driver

        if scrape:
            self.scrape(close_on_complete)

    def add_about(self, about):
        self.about.append(about)

    def add_experience(self, experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    def add_interest(self, interest):
        self.interests.append(interest)

    def add_accomplishment(self, accomplishment):
        self.accomplishments.append(accomplishment)

    def add_location(self, location):
        self.location = location

    def add_contact(self, contact):
        self.contacts.append(contact)

    def scrape(self, close_on_complete=True):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete)
        else:
            print("you are not logged in!")

    def _click_see_more_by_class_name(self, class_name):
        try:
            _ = WebDriverWait(self.driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            div = self.driver.find_element(By.CLASS_NAME, class_name)
            div.find_element(By.TAG_NAME, "button").click()
        except Exception as e:
            pass

    def is_open_to_work(self):
        try:
            return "#OPEN_TO_WORK" in self.driver.find_element(By.CLASS_NAME, "pv-top-card-profile-picture").find_element(By.TAG_NAME, "img").get_attribute("title")
        except:
            return False

    def get_experiences(self):
        url = os.path.join(self.linkedin_url, "details/experience")
        self.driver.get(url)
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        self.scroll_to_half()
        self.scroll_to_bottom()
        main_list = self.wait_for_element_to_load(name="pvs-list__container", base=main)
        for position in main_list.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item"):
            position = position.find_element(By.CSS_SELECTOR, "div[data-view-name='profile-component-entity']")
            company_logo_elem, position_details = position.find_elements(By.XPATH, "*")

            # company elem
            company_linkedin_url = company_logo_elem.find_element(By.XPATH, "*").get_attribute("href")
            if not company_linkedin_url:
                continue

            # position details
            position_details_list = position_details.find_elements(By.XPATH, "*")
            position_summary_details = position_details_list[0] if len(position_details_list) > 0 else None
            position_summary_text = position_details_list[1] if len(position_details_list) > 1 else None
            outer_positions = position_summary_details.find_element(By.XPATH, "*").find_elements(By.XPATH, "*")

            if len(outer_positions) == 4:
                position_title = outer_positions[0].find_element(By.TAG_NAME, "span").text
                company = outer_positions[1].find_element(By.TAG_NAME, "span").text
                work_times = outer_positions[2].find_element(By.TAG_NAME, "span").text
                location = outer_positions[3].find_element(By.TAG_NAME, "span").text
            elif len(outer_positions) == 3:
                if "·" in outer_positions[2].text:
                    position_title = outer_positions[0].find_element(By.TAG_NAME, "span").text
                    company = outer_positions[1].find_element(By.TAG_NAME, "span").text
                    work_times = outer_positions[2].find_element(By.TAG_NAME, "span").text
                    location = ""
                else:
                    position_title = ""
                    company = outer_positions[0].find_element(By.TAG_NAME, "span").text
                    work_times = outer_positions[1].find_element(By.TAG_NAME, "span").text
                    location = outer_positions[2].find_element(By.TAG_NAME, "span").text
            else:
                position_title = ""
                company = outer_positions[0].find_element(By.TAG_NAME, "span").text
                work_times = ""
                location = ""

            times = work_times.split("·")[0].strip() if work_times else ""
            duration = work_times.split("·")[1].strip() if len(work_times.split("·")) > 1 else None

            from_date = " ".join(times.split(" ")[:2]) if times else ""
            to_date = " ".join(times.split(" ")[3:]) if times else ""
            if position_summary_text and any(element.get_attribute("pvs-list__container") for element in position_summary_text.find_elements(By.TAG_NAME, "*")):
                inner_positions = (position_summary_text.find_element(By.CLASS_NAME, "pvs-list__container")
                                  .find_element(By.XPATH, "*").find_element(By.XPATH, "*").find_element(By.XPATH, "*")
                                  .find_elements(By.CLASS_NAME, "pvs-list__paged-list-item"))
            else:
                inner_positions = []
            if len(inner_positions) > 1:
                descriptions = inner_positions
                for description in descriptions:
                    res = description.find_element(By.TAG_NAME, "a").find_elements(By.XPATH, "*")
                    position_title_elem = res[0] if len(res) > 0 else None
                    work_times_elem = res[1] if len(res) > 1 else None
                    location_elem = res[2] if len(res) > 2 else None

                    location = location_elem.find_element(By.XPATH, "*").text if location_elem else None
                    position_title = position_title_elem.find_element(By.XPATH, "*").find_element(By.TAG_NAME, "*").text if position_title_elem else ""
                    work_times = work_times_elem.find_element(By.XPATH, "*").text if work_times_elem else ""
                    times = work_times.split("·")[0].strip() if work_times else ""
                    duration = work_times.split("·")[1].strip() if len(work_times.split("·")) > 1 else None
                    from_date = " ".join(times.split(" ")[:2]) if times else ""
                    to_date = " ".join(times.split(" ")[3:]) if times else ""

                    experience = Experience(
                        position_title=position_title,
                        from_date=from_date,
                        to_date=to_date,
                        duration=duration,
                        location=location,
                        description=description,
                        institution_name=company,
                        linkedin_url=company_linkedin_url
                    )
                    self.add_experience(experience)
            else:
                description = position_summary_text.text if position_summary_text else ""

                experience = Experience(
                    position_title=position_title,
                    from_date=from_date,
                    to_date=to_date,
                    duration=duration,
                    location=location,
                    description=description,
                    institution_name=company,
                    linkedin_url=company_linkedin_url
                )
                self.add_experience(experience)

    def get_educations(self):
        url = os.path.join(self.linkedin_url, "details/education")
        self.driver.get(url)
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        self.scroll_to_half()
        self.scroll_to_bottom()
        main_list = self.wait_for_element_to_load(name="pvs-list__container", base=main)
        for position in main_list.find_elements(By.CLASS_NAME, "pvs-list__paged-list-item"):
            position = position.find_element(By.XPATH, "//div[@data-view-name='profile-component-entity']")
            institution_logo_elem, position_details = position.find_elements(By.XPATH, "*")

            # company elem
            institution_linkedin_url = institution_logo_elem.find_element(By.XPATH, "*").get_attribute("href")

            # position details
            position_details_list = position_details.find_elements(By.XPATH, "*")
            position_summary_details = position_details_list[0] if len(position_details_list) > 0 else None
            position_summary_text = position_details_list[1] if len(position_details_list) > 1 else None
            outer_positions = position_summary_details.find_element(By.XPATH, "*").find_elements(By.XPATH, "*")

            institution_name = outer_positions[0].find_element(By.TAG_NAME, "span").text
            if len(outer_positions) > 1:
                degree = outer_positions[1].find_element(By.TAG_NAME, "span").text
            else:
                degree = None

            if len(outer_positions) > 2:
                times = outer_positions[2].find_element(By.TAG_NAME, "span").text

                if times != "":
                    from_date = times.split(" ")[times.split(" ").index("-")-1] if len(times.split(" "))>3 else times.split(" ")[0]
                    to_date = times.split(" ")[-1]
            else:
                from_date = None
                to_date = None

            description = position_summary_text.text if position_summary_text else ""

            education = Education(
                from_date=from_date,
                to_date=to_date,
                description=description,
                degree=degree,
                institution_name=institution_name,
                linkedin_url=institution_linkedin_url
            )
            self.add_education(education)

    def get_name_and_location(self):
        top_panel = self.driver.find_element(By.XPATH, "//*[@class='mt2 relative']")
        self.name = top_panel.find_element(By.TAG_NAME, "h1").text
        self.location = top_panel.find_element(By.XPATH, "//*[@class='text-body-small inline t-black--light break-words']").text

    def get_about(self):
        try:
            about = self.driver.find_element(By.ID, "about").find_element(By.XPATH, "..").find_element(By.CLASS_NAME, "display-flex").text
        except NoSuchElementException:
            about = None
        self.about = about

    def scrape_logged_in(self, close_on_complete=True):
        driver = self.driver
        duration = None

        root = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located((By.TAG_NAME, self.__TOP_CARD))
        )
        self.focus()
        self.wait(5)

        # get name and location
        self.get_name_and_location()

        self.open_to_work = self.is_open_to_work()

        # get about
        self.get_about()
        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));")
        driver.execute_script("window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));")

        # get experience
        self.get_experiences()

        # get education
        self.get_educations()

        driver.get(self.linkedin_url)

        # get interest
        try:
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@class='pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view']",
                    )
                )
            )
            interestContainer = driver.find_element(By.XPATH, "//*[@class='pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view']")
            for interestElement in interestContainer.find_elements(By.XPATH, "//*[@class='pv-interest-entity pv-profile-section__card-item ember-view']"):
                interest = Interest(
                    interestElement.find_element(By.TAG_NAME, "h3").text.strip()
                )
                self.add_interest(interest)
        except:
            pass

        # get accomplishment
        try:
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "//*[@class='pv-profile-section pv-accomplishments-section artdeco-container-card artdeco-card ember-view']",
                    )
                )
            )
            acc = driver.find_element(By.XPATH, "//*[@class='pv-profile-section pv-accomplishments-section artdeco-container-card artdeco-card ember-view']")
            for block in acc.find_elements(By.XPATH, "//div[@class='pv-accomplishments-block__content break-words']"):
                category = block.find_element(By.TAG_NAME, "h3")
                for title in block.find_element(By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li"):
                    accomplishment = Accomplishment(category.text, title.text)
                    self.add_accomplishment(accomplishment)
        except:
            pass

        # get connections
        try:
            driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mn-connections"))
            )
            connections = driver.find_element(By.CLASS_NAME, "mn-connections")
            if connections is not None:
                for conn in connections.find_elements(By.CLASS_NAME, "mn-connection-card"):
                    anchor = conn.find_element(By.CLASS_NAME, "mn-connection-card__link")
                    url = anchor.get_attribute("href")
                    name = conn.find_element(By.CLASS_NAME, "mn-connection-card__details").find_element(By.CLASS_NAME, "mn-connection-card__name").text.strip()
                    occupation = conn.find_element(By.CLASS_NAME, "mn-connection-card__details").find_element(By.CLASS_NAME, "mn-connection-card__occupation").text.strip()
                    contact = Contact(name=name, occupation=occupation, url=url)
                    self.add_contact(contact)
        except:
            connections = None

        if close_on_complete:
            driver.quit()

    @property
    def company(self):
        if self.experiences:
            return (
                self.experiences[0].institution_name
                if self.experiences[0].institution_name
                else None
            )
        else:
            return None

    @property
    def job_title(self):
        if self.experiences:
            return (
                self.experiences[0].position_title
                if self.experiences[0].position_title
                else None
            )
        else:
            return None

    def __repr__(self):
        return "<Person {name}\n\nAbout\n{about}\n\nExperience\n{exp}\n\nEducation\n{edu}\n\nInterest\n{int}\n\nAccomplishments\n{acc}\n\nContacts\n{conn}>".format(
            name=self.name,
            about=self.about,
            exp=self.experiences,
            edu=self.educations,
            int=self.interests,
            acc=self.accomplishments,
            conn=self.contacts,
        )

# ------------------------------
# FastAPI Setup
# ------------------------------

app = FastAPI()

class ScrapeRequest(BaseModel):
    linkedin_url: str

class ScrapeResponse(BaseModel):
    scraped_data: str

@app.post("/scrape", response_model=ScrapeResponse)
def scrape_profile(req: ScrapeRequest):
    # Set the path to your ChromeDriver executable.
    chromedriver_path = r"E:\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # Use a raw string
    # Create a Service instance with the path to chromedriver.
    service = Service(chromedriver_path)
    # Initialize the webdriver with the Service object.
    driver = webdriver.Chrome(service=service)
    try:
        # Log into LinkedIn.
        login(driver, email, password)
        # Replace with the LinkedIn profile URL from the request.
        linkedin_profile_url = req.linkedin_url
        # Create a Person object for the profile.
        person = Person(linkedin_profile_url, driver=driver)
        # Prepare a response. Here we return the __repr__ of the Person object.
        result = str(person)
        return ScrapeResponse(scraped_data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            driver.quit()
        except Exception:
            pass

# ------------------------------
# Main execution (for running with Python directly)
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
