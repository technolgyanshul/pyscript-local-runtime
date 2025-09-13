
import json
import asyncio
from pyodide.ffi import create_proxy
from pyodide.http import pyfetch
from js import chrome, document

def display_tabs(tabs):
    tab_list_div = document.getElementById("tab-list")
    
    # Clear any existing tabs in the list
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
    
    selected_tab_ids = []
    for checkbox in checkboxes:
        if checkbox.checked:
            selected_tab_ids.append(int(checkbox.value))
    
    def get_tabs_for_export(tabs):
        for tab in tabs:
            if tab.id in selected_tab_ids:
                selected_tabs_data.append({
                    "title": tab.title,
                    "url": tab.url,
                    "id": tab.id,
                    "active": tab.active,
                    "windowId": tab.windowId
                })
        
        if not selected_tabs_data:
            document.getElementById("json-output").value = ""
            return
        
        json_data = json.dumps(selected_tabs_data, indent=4)
        document.getElementById("json-output").value = json_data

    chrome.tabs.query({}, create_proxy(get_tabs_for_export))

async def generate_docs(e):
    api_key = document.getElementById("gemini-api-key").value
    if not api_key:
        document.getElementById("docs-output").value = "Please enter your Gemini API key."
        return

    document.getElementById("docs-output").value = "Generating descriptions..."

    def get_tabs_for_docs(tabs):
        async def fetch_descriptions():
            descriptions = []
            for tab in tabs:
                try:
                    prompt = f"What is the main purpose of the website at this URL: {tab.url}? Provide a one-sentence summary."
                    # Corrected the API endpoint and model
                    model = "gemini-1.5-flash-latest"
                    response = await pyfetch(
                        url=f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}",
                        method="POST",
                        headers={"Content-Type": "application/json"},
                        body=json.dumps({
                            "contents": [{
                                "parts": [{
                                    "text": prompt
                                }]
                            }]
                        })
                    )
                    data = await response.json()
                    # Check for errors in the response
                    if 'error' in data:
                        error_message = data['error'].get('message', 'Unknown error')
                        descriptions.append(f"{tab.title}: Error - {error_message}")
                        continue
                    
                    generated_text = data['candidates'][0]['content']['parts'][0]['text']
                    descriptions.append(f"{tab.title}: {generated_text.strip()}")
                except Exception as e:
                    descriptions.append(f"{tab.title}: Error generating description - {e}")
            
            document.getElementById("docs-output").value = "\n\n".join(descriptions)

        asyncio.ensure_future(fetch_descriptions())

    chrome.tabs.query({}, create_proxy(get_tabs_for_docs))


chrome.tabs.query({}, create_proxy(display_tabs))
document.getElementById("export-btn").addEventListener("click", create_proxy(export_selected_tabs))
document.getElementById("generate-docs-btn").addEventListener("click", create_proxy(generate_docs))
