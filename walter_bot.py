
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

# User-provided content to humanize
content_to_humanize = """This is a sample text that needs to be humanized. It is being used to test the Walter Writes AI bot. The purpose of this test is to ensure the bot can log in, navigate, input text, select options, and retrieve the processed output, while also attempting to bypass potential Cloudflare protections."""

# Login details
email = "aaaliyanzmoreau255@gmail.com"
password = "Create1#"

# Initialize WebDriver using standard Selenium for diagnostic purposes
options = ChromeOptions()
options.binary_location = "/usr/bin/chromium-browser"  # Path to the snap wrapper
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

chromedriver_path = "/usr/bin/chromedriver"  # Path to the very old system chromedriver
service = Service(executable_path=chromedriver_path, service_args=['--verbose', '--log-path=./chromedriver_std.log'])

print(f"Attempting to start standard Selenium WebDriver with:")
print(f"  Browser Binary: {options.binary_location}")
print(f"  ChromeDriver: {chromedriver_path}")

driver = None
try:
    driver = webdriver.Chrome(service=service, options=options)
    print("Standard Selenium WebDriver initialized successfully.")
    # 1. Navigate to the login page
    driver.get("https://app.walterwrites.ai/en/login?callbackUrl=https%3A%2F%2Fapp.walterwrites.ai")

    # Wait for the email input field to be present
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder=\'Email\']"))
    )
    email_field.send_keys(email)

    # Wait for the password input field to be present
    password_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder=\'Password\']"))
    )
    password_field.send_keys(password)

    # Click the Sign in button
    sign_in_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), \'Sign in\')]"))
    )
    sign_in_button.click()

    # 2. Navigate to the humanizer page (after successful login, this should redirect or be accessible)
    # It's better to wait for a specific element on the dashboard or humanizer page to confirm login
    # For now, let's assume a direct navigation is possible after login, or the callback URL handles it.
    WebDriverWait(driver, 30).until(
        EC.url_to_be("https://app.walterwrites.ai/en/dashboard") # Assuming dashboard is the first page after login
    )
    
    # Click the element with the Humanize AI Content which points to the url https://app.walterwrites.ai/en/humanizer
    # This selector might need adjustment based on the actual HTML structure after login
    humanize_ai_content_link = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[@href=\'/en/humanizer\']"))
    )
    humanize_ai_content_link.click()

    # Wait for the humanizer page to load
    WebDriverWait(driver, 20).until(
        EC.url_to_be("https://app.walterwrites.ai/en/humanizer")
    )

    # 3. Paste the content
    # The user mentioned div id="editorQuillContainer" for humanized text, assuming input area is also related
    # This selector might need adjustment based on the actual HTML structure
    input_editor = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.ql-editor")) # Common class for Quill editor input area
    )
    input_editor.send_keys(content_to_humanize)

    # 4. Select dropdown for Readability as Masters
    # Assuming the dropdown has a <select> tag and options
    readability_dropdown = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//label[contains(text(), \'Readability\')]/following-sibling::div//select")) # Adjust if not a direct select
    )
    Select(readability_dropdown).select_by_visible_text("Masters")

    # 5. Select dropdown for Purpose as Report
    purpose_dropdown = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//label[contains(text(), \'Purpose\')]/following-sibling::div//select")) # Adjust if not a direct select
    )
    Select(purpose_dropdown).select_by_visible_text("Report")

    # 6. Click the Detection Bypass Level as Enhanced
    enhanced_bypass_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), \'Enhanced\')]"))
    )
    enhanced_bypass_button.click()

    # 7. Click the button Humanize & Scan
    humanize_scan_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), \'Humanize & Scan\')]"))
    )
    humanize_scan_button.click()

    # 8. Wait until the text has been humanized in the div id="editorQuillContainer"
    # This is a crucial step and might require a more robust check (e.g., text change, loading spinner disappearance)
    # For now, a simple wait for the element to be visible and then a short sleep
    humanized_output_container = WebDriverWait(driver, 60).until(
        EC.visibility_of_element_located((By.ID, "editorQuillContainer"))
    )
    time.sleep(5) # Give it a few more seconds for content to fully load/change

    # 9. Click the class="absolute inset-0 flex size-full grow items-center justify-center transition-opacity duration-300 opacity-100" to copy the content.
    # This class name is very generic and might not be unique. It's better to find a more specific selector if possible.
    # Assuming this is a copy button that appears after humanization
    copy_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".absolute.inset-0.flex.size-full.grow.items-center.justify-center.transition-opacity.duration-300.opacity-100"))
    )
    copy_button.click()

    # 10. Output the humanized content to the client (assuming it's now in clipboard or can be retrieved from the div)
    # If the copy button copies to clipboard, we can't directly access it via Selenium.
    # We'll try to get the text directly from the humanized output container.
    humanized_content = humanized_output_container.text
    print("Humanized Content:")
    print(humanized_content)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()



