
import json
from pyodide.ffi import create_proxy
from js import chrome, document, Blob, URL, Object

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
    # Remove any existing download link
    existing_link = document.getElementById("download-link")
    if existing_link:
        document.body.removeChild(existing_link)

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
            return
        
        json_data = json.dumps(selected_tabs_data, indent=4)
        
        blob = Blob.new([json_data], {"type": "application/json"})
        url = URL.createObjectURL(blob)
        
        download_link = document.createElement("a")
        download_link.href = url
        download_link.download = "selected_tabs.json"
        download_link.textContent = "Click here to download your JSON file"
        download_link.id = "download-link"
        
        document.body.appendChild(download_link)

    chrome.tabs.query({}, create_proxy(get_tabs_for_export))

chrome.tabs.query({}, create_proxy(display_tabs))
document.getElementById("export-btn").addEventListener("click", create_proxy(export_selected_tabs))
