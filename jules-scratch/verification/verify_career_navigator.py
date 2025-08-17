import os
from playwright.sync_api import sync_playwright, expect

def run_verification():
    """
    This script verifies the AI Career Navigator frontend by:
    1. Navigating to the local index.html file.
    2. Entering a job title ("Software Developer").
    3. Clicking the analyze button.
    4. Waiting for the results to be displayed.
    5. Taking a screenshot of the final state.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Construct the absolute path to the index.html file
        # This makes the script runnable from anywhere
        html_file_path = os.path.abspath('ai-career-navigator/frontend/index.html')

        # Go to the local HTML file
        page.goto(f'file://{html_file_path}')

        # 1. Fill in the job title
        job_input = page.get_by_placeholder("e.g., Financial Analyst")
        expect(job_input).to_be_visible()
        job_input.fill("Software Developer")

        # 2. Click the analyze button
        analyze_button = page.get_by_role("button", name="Analyze My Role")
        analyze_button.click()

        # 3. Wait for the results to appear and assert correctness
        # We wait for the H2 with the role title to appear in the results container.
        # We use .first to ensure we are only targeting the first h2 element, avoiding strict mode violation.
        results_header = page.locator("#results-container h2").first
        expect(results_header).to_have_text("Software Developer", timeout=10000) # Increased timeout for API call

        # Check if the impact level is visible
        impact_level = page.locator(".impact-level.high")
        expect(impact_level).to_be_visible()
        expect(impact_level).to_have_text("High Transformation")

        # 4. Take a screenshot for visual verification
        screenshot_path = 'jules-scratch/verification/verification.png'
        page.screenshot(path=screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        browser.close()

if __name__ == "__main__":
    run_verification()
