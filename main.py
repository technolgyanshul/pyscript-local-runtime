
import json
import asyncio
from pyodide.ffi import create_proxy, to_js
from pyodide.http import pyfetch
from js import chrome, document, Promise

# --- Chrome Storage Helper Functions ---
async def get_storage_data(key):
    def resolver(resolve, reject):
        chrome.storage.local.get(key, create_proxy(lambda data: resolve(data.to_py() if hasattr(data, 'to_py') else {})))
    
    promise = Promise.new(create_proxy(resolver))
    return await promise

async def set_storage_data(data):
    def resolver(resolve, reject):
        chrome.storage.local.set(to_js(data), create_proxy(resolve))
    
    promise = Promise.new(create_proxy(resolver))
    await promise

async def remove_storage_data(key):
    def resolver(resolve, reject):
        chrome.storage.local.remove(key, create_proxy(resolve))

    promise = Promise.new(create_proxy(resolver))
    await promise

# --- UI Management ---
def setup_ui():
    async def get_initial_key():
        data = await get_storage_data('gemini_api_key')
        api_key = data.get('gemini_api_key')
        if api_key:
            document.getElementById("gemini-api-key").value = api_key
            document.getElementById("api-key-container").style.display = "none"
            document.getElementById("change-api-key-btn").style.display = "block"
        else:
            document.getElementById("api-key-container").style.display = "block"
            document.getElementById("change-api-key-btn").style.display = "none"

    asyncio.ensure_future(get_initial_key())

def show_api_key_input():
    document.getElementById("api-key-container").style.display = "block"
    document.getElementById("change-api-key-btn").style.display = "none"

# --- Main Functions ---
def display_tabs(tabs):
    tab_list_div = document.getElementById("tab-list")
    tab_list_div.innerHTML = ""
    for tab in tabs:
        checkbox = document.createElement("input")
        checkbox.type = "checkbox"
        checkbox.id = f"tab-{tab.id}"
        checkbox.value = tab.id
        checkbox.checked = True
        label = document.createElement("label")
        label.setAttribute("for", f"tab-{tab.id}")
        label.textContent = tab.title
        container = document.createElement("div")
        container.appendChild(checkbox)
        container.appendChild(label)
        tab_list_div.appendChild(container)

def export_selected_tabs(e):
    selected_tabs_data = []
    checkboxes = document.querySelectorAll("#tab-list input[type='checkbox']")
    selected_tab_ids = [int(cb.value) for cb in checkboxes if cb.checked]

    def get_tabs_for_export(tabs):
        for tab in tabs:
            if tab.id in selected_tab_ids:
                selected_tabs_data.append({
                    "title": tab.title,
                    "url": tab.url
                })
        document.getElementById("json-output").value = json.dumps(selected_tabs_data, indent=4)

    chrome.tabs.query({}, create_proxy(get_tabs_for_export))

async def generate_docs(e):
    api_key_input = document.getElementById("gemini-api-key")
    api_key = api_key_input.value
    output_area = document.getElementById("docs-output")

    if not api_key:
        output_area.value = "Please enter your Gemini API key."
        return

    output_area.value = "Starting..."
    
    json_schema = {"type": "OBJECT", "properties": {"summary": {"type": "STRING"}}, "required": ["summary"]}
    generation_config = {"response_mime_type": "application/json", "response_schema": json_schema}

    async def get_tabs_and_fetch_descriptions(tabs):
        checkboxes = document.querySelectorAll("#tab-list input[type='checkbox']")
        selected_tab_ids = {int(cb.value) for cb in checkboxes if cb.checked}
        selected_tabs = [tab for tab in tabs if tab.id in selected_tab_ids]

        if not selected_tabs:
            output_area.value = "No tabs selected."
            return

        descriptions = {}
        initial_text = [f"{tab.title}: Queued..." for tab in selected_tabs]
        output_area.value = "\n\n".join(initial_text)
        
        successful_api_call = False

        for tab in selected_tabs:
            # Update UI to show current tab is processing
            descriptions[tab.id] = "Generating..."
            current_text = [f"{t.title}: {descriptions.get(t.id, 'Queued...')}" for t in selected_tabs]
            output_area.value = "\n\n".join(current_text)

            try:
                prompt = f"Based on the following title and URL, write a short, one-sentence predicted summary of the webpage.\nTitle: {tab.title}\nURL: {tab.url}"
                model = "gemini-1.5-flash-latest"
                
                response = await pyfetch(
                    url=f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
                    method="POST",
                    headers={"Content-Type": "application/json"},
                    body=json.dumps({
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": generation_config
                    })
                )
                data = await response.json()

                if response.status != 200 or 'candidates' not in data:
                    error_message = data.get('error', {}).get('message', f'HTTP {response.status} - No valid response.')
                    descriptions[tab.id] = f"Error: {error_message}"
                    if response.status in [401, 403]:
                        await remove_storage_data('gemini_api_key')
                        show_api_key_input()
                        output_area.value = f"API Key failed. Please enter a new key.\nError: {error_message}"
                        return
                else:
                    successful_api_call = True
                    generated_content = data['candidates'][0]['content']['parts'][0]['text']
                    response_json = json.loads(generated_content)
                    summary = response_json.get("summary", "No summary found.")
                    descriptions[tab.id] = summary.strip()

            except Exception as err:
                descriptions[tab.id] = f"Error: {str(err)}"
            
            # Update UI with the result for the current tab
            final_text = [f"{t.title}: {descriptions.get(t.id, 'Error')}" for t in selected_tabs]
            output_area.value = "\n\n".join(final_text)

        if successful_api_call:
            await set_storage_data({'gemini_api_key': api_key})
            document.getElementById("api-key-container").style.display = "none"
            document.getElementById("change-api-key-btn").style.display = "block"

    # Use a proxied async callback
    chrome.tabs.query({"currentWindow": True}, create_proxy(get_tabs_and_fetch_descriptions))

# --- Event Listeners ---
chrome.tabs.query({}, create_proxy(display_tabs))
document.getElementById("export-btn").addEventListener("click", create_proxy(export_selected_tabs))
document.getElementById("generate-docs-btn").addEventListener("click", create_proxy(generate_docs))
document.getElementById("change-api-key-btn").addEventListener("click", create_proxy(lambda e: show_api_key_input()))

# --- Initial Setup ---
setup_ui()
