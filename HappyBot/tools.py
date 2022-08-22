from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import chromedriver_binary

project_message = \
    """
```
Check out the CIS Club!
Here is the google form to sign up ⬇️
``` 
- https://forms.gle/3CtiQcdLPLE5PNNAA
```
Right here is the discord ⬇️
``` 
- https://discord.gg/rbUa47a2
```
We are excited to start many projects one of which is building
discord bots, so 
Lets build bots! send a message or send your email to the bot
by using the command: 
::email <github_email> 
to be added to the project  👍
we are hoping to get server set up, 
until then happy bot might be down every
so often 🤖
Github for Discord Bot(s) project ⬇️  
```
https://github.com/sebcampos/CSM_CIS_Discord_bots
"""


welcome_message_content = \
"""
"*I am happy bot, \n*
*send me the command `::punny` and ill tell you a joke...*"
"""


def scrape_puns():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get("https://parade.com/1024249/marynliles/funny-puns/")  # url for puns
    puns_list = [p_tag.text for p_tag in driver.find_elements(By.XPATH, "//article//p") if
                 p_tag.text and p_tag.text[0].isnumeric()]
    driver.close()
    driver.quit()
    cleaned_list = [re.sub(r"^[0-9]{1,3}\. ", "", i) for i in puns_list]
    return cleaned_list


def add_email_to_db(user, message, bot):
    message = message.replace("::email", "")
    email = re.search("([a-zA-Z0-9]+@.+)", message)  # not the best email validator
    if not email:
        return False
    email = email.groups()[0].strip()
    data = \
        {
            "username": [str(user)],
            "email": [email]
        }
    bot.add_to_database("emails", data)
    return True
