# AI Tab Scribe

A Chrome extension that uses the Gemini API to automatically generate one-sentence summaries for your open browser tabs. It also allows you to export tab information as a JSON file.

## Features

*   **Export Tabs to JSON:** Select and export the details (title, URL) of your open tabs into a clean JSON format.
*   **AI-Powered Descriptions:** Automatically generate a one-sentence summary for each open tab using Google's Gemini Pro model.

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
3.  In the "Generate Website Descriptions" section, paste your Gemini API key into the input field.
4.  Click the "Generate Descriptions" button.
5.  The extension will call the Gemini API for each of your open tabs and display the generated one-sentence summary in the text area below.

## Technologies Used

*   **Python**
*   **PyScript** (to run Python in the browser)
*   **Google Gemini API**
