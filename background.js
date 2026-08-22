chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "scanLink",
    title: "Scan link with SafeClick",
    contexts: ["link", "selection"]
  });
});
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "scanLink") {
    fetch('http://127.0.0.1:5000/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: info.linkUrl })
    })
    .then(response => response.json())
    .then(data => {
      chrome.scripting.executeScript({
        target: {tabId: tab.id},
        func: (score, flags) => {
            alert(`SafeClick Score: ${score}/100\nFlags: ${flags}`);
        },
        args: [data.risk_score, data.reasons.map(r => r.text).join(" | ")]
      });
    })
    .catch(err => console.log("Engine offline", err));
  }
});