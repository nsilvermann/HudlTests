from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Assumes every wepbage is at least reachable
# Doesn't account for authentication services being down


driver = webdriver.Chrome()

f = open("loginCredentials.txt", "r")
userEmail = f.readline().strip().split(" ")[1]
userPassword = f.readline().strip().split(" ")[1]
f.close()

if(userEmail == "replace_with_your_email" or userPassword == "replace_with_your_password"):
	print("Please enter your email/password in the loginCredentials.txt file.")


# The backIcon is <a> without href. Validated by checking url switches to hudl.com.
def testBackIcon(): 
	driver.get("https://www.hudl.com/login")
	backIcon = driver.find_element("xpath", "//*[contains(@class, 'backIcon')]").click()
	pageURL = driver.current_url

	if(pageURL == "https://www.hudl.com/"):
		print("Back Icon - Pass")
	else:
		print("Back Icon - Fail")


# Tests sign up link redirects
def testSignUp():
	driver.get("https://www.hudl.com/login")
	signUpLink = driver.find_element("xpath", "//*[contains(@class, 'signUpLink')]").click()
	pageURL = driver.current_url

	if(pageURL == "https://www.hudl.com/register/signup"):
		print("Sign Up Link - Pass")
	else:
		print("Sign Up Link - Fail")


# Tests Hudl logo redirect
def testHudlLogo():
	driver.get("https://www.hudl.com/login")
	hudlLogo = driver.find_element("xpath", "//*[contains(@class, 'hudlLogoContainer')]").click()
	pageURL = driver.current_url

	if(pageURL == "https://www.hudl.com/"):
		print("Hudl Logo - Pass")
	else:
		print("Hudl Logo - Fail")


# Tests need help link redirect
def testNeedHelp():
	driver.get("https://www.hudl.com/login")
	# data-qa-id= need-help-link
	helpLink = driver.find_element(By.LINK_TEXT, "Need help?").click()
	pageURL = driver.current_url

	if(pageURL == "https://www.hudl.com/login/help#"):
		print("Help Link - Pass")
	else:
		print("Help Link - Fail")


# Tests organization log in redirect
def testOrganizationLogIn():
	driver.get("https://www.hudl.com/login")
	OrganizationLoginInLink = driver.find_element(By.LINK_TEXT, "Log In with an Organization").click()
	pageURL = driver.current_url

	if(pageURL == "https://www.hudl.com/app/auth/login/organization"):
		print("Organization Link - Pass")
	else:
		print("Organization Link - Fail")


# Not critical to validate the functionality of the hudl.com login page
# def testRememberMe():
	# driver.get("https://www.hudl.com/login")


# Attempts to sign in with given email/password using button click
def testLoginButton(email, password, correctTitle, testName): 
	driver.get("https://www.hudl.com/login")
	emailInput = driver.find_element(By.ID, "email")
	emailInput.send_keys(email)

	passwordInput = driver.find_element(By.ID, "password")
	passwordInput.send_keys(password)

	logInButton = driver.find_element(By.ID, "logIn")
	logInButton.click()
	try:
		WebDriverWait(driver, 2).until(EC.title_contains(correctTitle))
	except:
		print(testName + " - Fail")

	if(driver.title == correctTitle):
		print(testName + " - Pass")


# Attempts to sign in with given email/password by enter key stroke
def testLoginEnter(email, password, correctTitle, testName): 
	driver.get("https://www.hudl.com/login")
	emailInput = driver.find_element(By.ID, "email")
	emailInput.send_keys(email)

	passwordInput = driver.find_element(By.ID, "password")
	passwordInput.send_keys(password)
	passwordInput.send_keys(Keys.ENTER)
	try:
		WebDriverWait(driver, 2).until(EC.title_contains(correctTitle))
	except:
		print(testName + " - Fail")

	if(driver.title == correctTitle):
		print(testName + " - Pass")



# All Combinations (b= blank, w= wrong c= correct)
	# - b email, b pass  fail
	# - b email, w pass  fail
	# - b email, c pass  fail
	# - w email, b pass  fail
	# - c email, b pass  fail
	# - w email, w pass  fail
	# - w email, c pass  fail
	# - c email, w pass  fail
	# - c email, c pass  pass

def testAllElements():
	testBackIcon()
	testSignUp()
	testHudlLogo()
	testNeedHelp()
	testOrganizationLogIn()
	# testRememberMe()

def testAllEnterLogins():
	testLoginEnter("", "", "Log In", "Bank Email/Blank password")
	testLoginEnter("", "fakepassword", "Log In", "Blank Email/Wrong password")
	testLoginEnter("", userPassword, "Log In", "Blank Email/Correct password")

	testLoginEnter("fakeemail@fake.com", "", "Log In", "Wrong Email/Blank password")
	testLoginEnter(userEmail, "", "Log In", "Correct Email/Blank password")

	testLoginEnter("fakeemail@fake.com", "fakepassword", "Log In", "Wrong Email/Wrong password")
	testLoginEnter("fakeemail@fake.com", userPassword, "Log In", "Wrong Email/Correct password")
	testLoginEnter(userEmail, "fakepassword", "Log In", "Correct Email/Wrong password")
	testLoginEnter(userEmail, userPassword, "Home - Hudl", "Correct Email/Correct password")

def testAllButtonLogins():
	testLoginButton("", "", "Log In", "Bank Email/Blank password")
	testLoginButton("", "fakepassword", "Log In", "Blank Email/Wrong password")
	testLoginButton("", userPassword, "Log In", "Blank Email/Correct password")

	testLoginButton("fakeemail@fake.com", "", "Log In", "Wrong Email/Blank password")
	testLoginButton(userEmail, "", "Log In", "Correct Email/Blank password")

	testLoginButton("fakeemail@fake.com", "fakepassword", "Log In", "Wrong Email/Wrong password")
	testLoginButton("fakeemail@fake.com", userPassword, "Log In", "Wrong Email/Correct password")
	testLoginButton(userEmail, "fakepassword", "Log In", "Correct Email/Wrong password")
	testLoginButton(userEmail, userPassword, "Home - Hudl", "Correct Email/Correct password")

testAllElements()
testAllEnterLogins()
testAllButtonLogins()

driver.quit()