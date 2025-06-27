
from playwright.sync_api import sync_playwright, expect, Error as PlaywrightError
from playwright_stealth.stealth import Stealth # Corrected import for Stealth class
import time

# User-provided content to humanize
content_to_humanize = """This is a sample text that needs to be humanized. It is being used to test the Walter Writes AI bot. The purpose of this test is to ensure the bot can log in, navigate, input text, select options, and retrieve the processed output, while also attempting to bypass potential Cloudflare protections."""

# Login details
email = "aaaliyanzmoreau255@gmail.com"
password = "Create1#"

def main():
    # Wrap sync_playwright() with Stealth().use_sync()
    with Stealth().use_sync(sync_playwright()) as p:
        browser = None
        try:
            print("Launching Chromium browser (headless) with Playwright Stealth...")
            browser_launch_args = [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
            ]
            browser = p.chromium.launch(headless=True, args=browser_launch_args)
            page = browser.new_page()
            print("Browser and page initialized.")

            # Stealth is applied via the context manager, so no explicit stealth_sync(page) needed here.
            # print("Applying stealth settings...") # No longer needed explicitly
            # stealth_sync(page) # No longer needed explicitly
            # print("Stealth settings applied.") # No longer needed explicitly

            # 1. Navigate to the login page
            login_url = "https://app.walterwrites.ai/en/login?callbackUrl=https%3A%2F%2Fapp.walterwrites.ai"
            print(f"Navigating to login page: {login_url}")
            # Increased timeout for page.goto to allow Cloudflare challenge more time
            page.goto(login_url, timeout=90000, wait_until="domcontentloaded")
            print(f"Initial navigation complete. Current URL: {page.url}")

            # Reduced explicit wait, relying more on stealth and Playwright's auto-waits
            # print("Waiting for 15 seconds to allow Cloudflare challenge to resolve...")
            # page.wait_for_timeout(15000) # Wait 15 seconds
            # print(f"Current URL after 15s delay: {page.url}")


            # Debug: Save screenshot and print page content
            screenshot_path = "login_page_debug.png"
            page.screenshot(path=screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
            print(f"Page content first 1000 chars after delay:\n{page.content()[:1000]}")

            # Fill email
            print(f"Filling email: {email}")
            # Reverting to get_by_placeholder, as Cloudflare is bypassed. Increased timeout.
            email_locator = page.get_by_placeholder("Email")
            email_locator.wait_for(state="visible", timeout=60000) # Increased timeout
            print("Typing email...")
            email_locator.type(email, delay=50) # Simulate typing

            # Fill password - using get_by_placeholder as well.
            print("Typing password...")
            password_locator = page.get_by_placeholder("Password")
            password_locator.wait_for(state="visible", timeout=30000) # Standard timeout for password
            password_locator.type(password, delay=50) # Simulate typing
            print("Password typed. Attempting to submit by pressing Enter.")
            password_locator.press("Enter")

            # Debug: Screenshot after login attempt
            page.wait_for_timeout(2000) # Brief pause for page to potentially react after Enter
            print(f"URL after Enter press: {page.url}")
            after_login_attempt_screenshot_path = "after_login_attempt.png"
            page.screenshot(path=after_login_attempt_screenshot_path)
            print(f"Screenshot after login attempt saved to {after_login_attempt_screenshot_path}")
            print(f"Page content after login attempt (first 1000 chars):\n{page.content()[:1000]}")

            # Check for login error messages
            # Common patterns for error messages. These are guesses.
            possible_error_selectors = [
                "[role='alert']",
                "div[class*='error']",
                "p[class*='error']",
                "div[data-testid*='error']",
                "span[class*='error']"
            ]
            error_message_found = False
            for i, selector in enumerate(possible_error_selectors):
                try:
                    # Wait briefly for the error message to potentially appear
                    error_locator = page.locator(selector).first # Take the first if multiple
                    error_locator.wait_for(state="visible", timeout=5000) # 5s timeout for error message
                    error_text = error_locator.inner_text()
                    if error_text:
                        print(f"Potential login error message found (selector {i+1}): {error_text.strip()}")
                        error_message_found = True
                        break # Stop if one error message is found
                except PlaywrightError: # TimeoutError is a PlaywrightError subtype
                    # This selector didn't find a visible error, try next
                    print(f"No error message found with selector {i+1}: {selector}")
                    pass

            if not error_message_found:
                print("No common login error messages detected visually or by common selectors.")

            # Wait for navigation to the dashboard
            dashboard_url_pattern = "https://app.walterwrites.ai/en/dashboard"
            print(f"Waiting for navigation to dashboard URL pattern: {dashboard_url_pattern}")
            page.wait_for_url(dashboard_url_pattern, timeout=30000)
            print("Successfully navigated to dashboard.")

            # 2. Navigate to the humanizer page
            print("Navigating to Humanizer page...")
            # The old Selenium script used: //a[@href='/en/humanizer']
            # A more Playwright-idiomatic way if the text is unique and stable:
            # page.get_by_role("link", name="Humanize AI Content").click()
            # Or using the href attribute directly:
            page.locator("a[href='/en/humanizer']").click()

            humanizer_url_pattern = "https://app.walterwrites.ai/en/humanizer"
            print(f"Waiting for navigation to Humanizer URL pattern: {humanizer_url_pattern}")
            page.wait_for_url(humanizer_url_pattern, timeout=20000)
            print("Successfully navigated to Humanizer page.")

            # 3. Paste the content
            print("Pasting content into the editor...")
            # The old Selenium script used: div.ql-editor (CSS_SELECTOR)
            # This should be equivalent in Playwright
            input_editor_locator = page.locator("div.ql-editor")
            input_editor_locator.wait_for(state="visible", timeout=20000) # Ensure editor is ready
            input_editor_locator.fill(content_to_humanize)
            print("Content pasted.")

            # 4. Select dropdown for Readability as Masters
            # Selenium XPath: //label[contains(text(), 'Readability')]/following-sibling::div//select
            print("Selecting Readability: Masters...")
            readability_dropdown_locator = page.locator("//label[contains(text(), 'Readability')]/following-sibling::div//select")
            readability_dropdown_locator.select_option(label="Masters")
            print("Readability selected.")

            # 5. Select dropdown for Purpose as Report
            # Selenium XPath: //label[contains(text(), 'Purpose')]/following-sibling::div//select
            print("Selecting Purpose: Report...")
            purpose_dropdown_locator = page.locator("//label[contains(text(), 'Purpose')]/following-sibling::div//select")
            purpose_dropdown_locator.select_option(label="Report")
            print("Purpose selected.")

            # 6. Click the Detection Bypass Level as Enhanced
            # Selenium XPath: //button[contains(text(), 'Enhanced')]
            print("Clicking Detection Bypass Level: Enhanced...")
            # Using get_by_role if "Enhanced" is the accessible name of a button
            # If not, a more specific locator might be needed.
            page.get_by_role("button", name="Enhanced", exact=True).click()
            print("Enhanced bypass level clicked.")

            # 7. Click the button Humanize & Scan
            # Selenium XPath: //button[contains(text(), 'Humanize & Scan')]
            print("Clicking 'Humanize & Scan' button...")
            page.get_by_role("button", name="Humanize & Scan", exact=True).click()
            print("'Humanize & Scan' button clicked.")

            # 8. Wait until the text has been humanized in the div id="editorQuillContainer"
            print("Waiting for humanized output container to be visible...")
            humanized_output_container_locator = page.locator("#editorQuillContainer")
            humanized_output_container_locator.wait_for(state="visible", timeout=60000)
            print("Humanized output container is visible.")

            # Give it a few more seconds for content to fully load/change, as in original script
            print("Waiting for a short delay for content to settle...")
            page.wait_for_timeout(5000)

            # 9. Click the copy button
            # This selector is very generic and might fail or click the wrong thing.
            # CSS Selector from original: ".absolute.inset-0.flex.size-full.grow.items-center.justify-center.transition-opacity.duration-300.opacity-100"
            # It's better to find a more specific selector if possible. For now, translating directly.
            # If this is problematic, this step might need to be skipped or refined after testing.
            copy_button_css_selector = ".absolute.inset-0.flex.size-full.grow.items-center.justify-center.transition-opacity.duration-300.opacity-100"
            print(f"Attempting to click copy button with CSS selector: {copy_button_css_selector}")
            try:
                copy_button_locator = page.locator(copy_button_css_selector)
                # Check if the button is unique and visible before clicking
                if copy_button_locator.count() == 1 and copy_button_locator.is_visible():
                    copy_button_locator.click()
                    print("Copy button clicked.")
                elif copy_button_locator.count() > 1:
                    print(f"Warning: Multiple elements found for copy button selector. Clicking the first one.")
                    copy_button_locator.first.click()
                    print("Copy button (first match) clicked.")
                else:
                    print("Warning: Copy button not found or not visible with the generic selector. Skipping click.")

            except Exception as copy_e:
                print(f"Warning: Could not click copy button (selector might be too generic or element changed): {copy_e}")

            # 10. Output the humanized content
            print("Extracting humanized content...")
            # We'll try to get the text directly from the humanized output container.
            humanized_content = humanized_output_container_locator.inner_text()
            print("--- Humanized Content Start ---")
            print(humanized_content)
            print("--- Humanized Content End ---")


        except PlaywrightError as e:
            print(f"A Playwright Error occurred: {e}")
            if "missing dependencies" in str(e).lower():
                 print("This error often indicates missing OS-level libraries for the browser.")
                 print("Common ones for Debian/Ubuntu include: libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libxss1 libasound2 libxtst6")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            import traceback
            traceback.print_exc()
        finally:
            if browser:
                print("Closing browser...")
                browser.close()
                print("Browser closed.")

if __name__ == "__main__":
    main()
