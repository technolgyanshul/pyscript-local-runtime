
import json
import asyncio
from pyodide.ffi import create_proxy
from pyodide.http import pyfetch
from js import chrome, document

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
    api_key = document.getElementById("gemini-api-key").value
    if not api_key:
        document.getElementById("docs-output").value = "Please enter your Gemini API key."
        return

    document.getElementById("docs-output").value = "Generating descriptions using URL context..."

    json_schema = {
        "type": "OBJECT",
        "properties": {
            "summary": {"type": "STRING"}
        },
        "required": ["summary"]
    }
    
    generation_config = {
        "response_mime_type": "application/json",
        "response_schema": json_schema
    }

    def get_tabs_for_docs(tabs):
        async def fetch_descriptions():
            descriptions = []
            for tab in tabs:
                try:
                    prompt = "Provide a one-sentence summary of the provided web page."
                    
                    # Corrected tool name to `googleSearchRetrieval` for the v1 API
                    tools = [{
                        "googleSearchRetrieval": {
                            "uris": [tab.url]
                        }
                    }]

                    model = "gemini-2.5-flash"
                    response = await pyfetch(
                        url=f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}",
                        method="POST",
                        headers={"Content-Type": "application/json"},
                        body=json.dumps({
                            "contents": [{"parts": [{"text": prompt}]}],
                            "tools": tools,
                            "generationConfig": generation_config
                        })
                    )

                    data = await response.json()
                    
                    if response.status != 200 or 'error' in data:
                        error_message = data.get('error', {}).get('message', f'HTTP {response.status}')
                        descriptions.append(f"{tab.title}: Error - {error_message}")
                        continue

                    generated_content = data['candidates'][0]['content']['parts'][0]['text']
                    response_json = json.loads(generated_content)
                    summary = response_json.get("summary", "No summary found in response.")
                    descriptions.append(f"{tab.title}: {summary.strip()}")

                except Exception as err:
                    descriptions.append(f"{tab.title}: Error processing request - {str(err)}")
            
            document.getElementById("docs-output").value = "\n\n".join(descriptions)

        asyncio.ensure_future(fetch_descriptions())

    chrome.tabs.query({}, create_proxy(get_tabs_for_docs))


chrome.tabs.query({}, create_proxy(display_tabs))
document.getElementById("export-btn").addEventListener("click", create_proxy(export_selected_tabs))
document.getElementById("generate-docs-btn").addEventListener("click", create_proxy(generate_docs))
