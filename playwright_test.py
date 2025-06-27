from playwright.sync_api import sync_playwright, Error as PlaywrightError
import time

def run_playwright_test():
    print("Attempting to run Playwright test...")
    with sync_playwright() as p:
        browser = None
        try:
            print("Launching Chromium browser (headless)...")
            # Explicitly set headless=True, though it's often default
            # Adding common sandbox args that might be needed, similar to Selenium
            browser_launch_args = [
                '--no-sandbox',  # Often required in sandboxed/CI environments
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage', # Overcome limited resource problems
                '--disable-gpu', # Can help in headless environments
            ]
            browser = p.chromium.launch(headless=True, args=browser_launch_args)
            print("Browser launched successfully.")

            page = browser.new_page()
            print("New page created.")

            target_url = "http://example.com"
            print(f"Navigating to {target_url}...")
            page.goto(target_url, timeout=30000) # 30s timeout
            print(f"Navigation to {target_url} successful.")

            title = page.title()
            print(f"Page title: {title}")

            if "Example Domain" not in title:
                print(f"Error: Unexpected page title: {title}")
            else:
                print("Playwright test appears successful!")

        except PlaywrightError as e:
            print(f"A Playwright Error occurred: {e}")
            # Attempt to capture more details if possible
            if e.message and "Host system is missing dependencies" in e.message:
                print("This error often indicates missing OS-level libraries for the browser.")
                print("Common ones for Debian/Ubuntu include: libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libgbm1 libxss1 libasound2 libxtst6")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            if browser:
                print("Closing browser...")
                browser.close()
                print("Browser closed.")

if __name__ == "__main__":
    run_playwright_test()
