
import json
from pyodide.ffi import create_proxy
from js import chrome, document, Blob, URL, Object

def get_tabs_data(tabs):
    tabs_data = []
    for tab in tabs:
        tabs_data.append({
            "title": tab.title,
            "url": tab.url,
            "id": tab.id,
            "active": tab.active,
            "windowId": tab.windowId
        })
    
    json_data = json.dumps(tabs_data, indent=4)
    
    # Create a Blob from the JSON data
    blob = Blob.new([json_data], {"type": "application/json"})
    
    # Create a URL for the Blob
    url = URL.createObjectURL(blob)
    
    # Create a download link
    download_link = document.createElement("a")
    download_link.href = url
    download_link.download = "tabs.json"
    download_link.textContent = "Download JSON"
    
    # Add the link to the document
    document.body.appendChild(download_link)
    download_link.click()
    document.body.removeChild(download_link)


def export_tabs(e):
    chrome.tabs.query({}, create_proxy(get_tabs_data))

document.getElementById("export-btn").addEventListener("click", create_proxy(export_tabs))
