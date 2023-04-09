const app = {}
app.methods = {}

app.methods.setContextMenuItems = (fieldsets) => {
  chrome.contextMenus.create({
    id: "ChatGPT",
    title: "ChatGPT",
    contexts: ['selection'],
  });
};

chrome.runtime.onInstalled.addListener(() => 
  chrome.storage.sync.get(null, (storage) => app.methods.setContextMenuItems(storage.fieldsets))
);

chrome.contextMenus.onClicked.addListener(
  (info) => {console.log("Clicked");
  chrome.browserAction.setTitle({
    title:'This is the tooltip text upon mouse hover.'
});}
);