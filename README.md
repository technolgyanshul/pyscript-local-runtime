# AI Tab Scribe

A Chrome extension that uses the Gemini API to automatically generate one-sentence summaries for your open browser tabs. It also allows you to export tab information as a JSON file.

## Features

*   **Export Tabs to JSON:** Select and export the details (title, URL) of your open tabs into a clean JSON format.
*   **AI-Powered Descriptions:** Automatically generate a one-sentence summary for each open tab using Google's Gemini Pro model.
*   **Smart API Key Management:** Securely stores your Gemini API key in local storage, so you only need to enter it once.
*   **Theme Aware:** Includes a theme switcher with light, dark, and system theme options.

## How to Use

### 1. Load the Extension

1.  Open Chrome and navigate to `chrome://extensions`.
2.  Enable "Developer mode" using the toggle in the top-right corner.
3.  Click the "Load unpacked" button.
4.  Select the directory where you've saved these project files.

### 2. Export Tabs

1.  Click on the AI Tab Scribe extension icon in your Chrome toolbar.
2.  The popup will display a list of all your open tabs, which are all selected by default.
3.  Deselect any tabs you don't want to export.
4.  Click the "Export Selected Tabs" button.
5.  The tab information will be displayed as a JSON object in the text area below. You can copy this for your own use.

### 3. Generate AI Descriptions

1.  **Get a Gemini API Key:** You will need a Gemini API key to use this feature. You can obtain a free key from [Google AI Studio](https://makersuite.google.com/).
2.  Click on the AI Tab Scribe extension icon in your Chrome toolbar.
3.  The first time you use the feature, paste your Gemini API key into the input field.
4.  Click the "Generate Descriptions" button.
5.  The extension will call the Gemini API for each of your open tabs and display the generated one-sentence summary in the text area below.

## Limitations

This extension operates within the strict security boundaries of the Chrome extension environment. For security reasons, the popup cannot directly read the content of your open tabs.

*   **Predictive, Not Extractive Summaries:** The AI generates a *predicted* summary based only on the **title and URL** of a webpage, not its actual content. It is making an educated guess about the page's content, similar to a human reading a headline.

## Future Scope

To provide true, high-quality summaries, the extension would need to be enhanced to read the actual text content of each webpage. This can be achieved through the following process:

*   **DOM Access via Content Scripts:** The next version could implement a content script, which is a secure mechanism for an extension to interact with a webpage. This would involve:
    1.  Requesting additional permissions in the `manifest.json` file to run scripts on web pages.
    2.  Injecting the content script into each selected tab.
    3.  The script would then read the page's text content (from the Document Object Model, or DOM).
    4.  This extracted text would be sent to the Gemini API to generate a summary based on the full content, resulting in a much more accurate and informative description.

## Technologies Used

*   **Python**
*   **PyScript** (to run Python in the browser)
*   **Google Gemini API**
