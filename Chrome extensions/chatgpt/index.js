// const app = {}
// app.methods = {}

// app.methods.setContextMenuItems = (fieldsets) => {
//   chrome.contextMenus.create({
//     id: "ChatGPT",
//     title: "ChatGPT",
//     contexts: ['selection'],
//   });
// };

// chrome.runtime.onInstalled.addListener(() => 
//   chrome.storage.sync.get(null, (storage) => app.methods.setContextMenuItems(storage.fieldsets))
// );

// chrome.contextMenus.onClicked.addListener(
//   (info) => {alert("Clicked");
//   chrome.browserAction.setTitle({
//     title:'This is the tooltip text upon mouse hover.'
// });}
// );

// chrome.runtime.onInstalled.addListener(() => {
//   chrome.contextMenus.create({
//     id: "ChatGPT",
//     title: "My Chrome Extension",
//     contexts: ["all"],
//     onclick: () => {
//       alert("Hello, World!");
//     }
//   });
// });


// chrome.contextMenus.onClicked.addListener(
//   (info) => {alert("Clicked");}
// );

import { OPENAI_API_KEY } from "./env.js";

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    title: "CE",
    contexts: ["all"],
    id: "my-context-menu"
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  // if (info.menuItemId === "my-context-menu") {
  //   chrome.notifications.create('notify1', {
  //     type: "basic",
  //     title: "CE",
  //     message: "Hello, World!",
  //     iconUrl: chrome.runtime.getURL("icon.png")
  //   }, function() { console.log('created!'); });
  // }

  function getChatGPTResponse() {
    console.log(info.selectionText)
    if (info.selectionText === undefined || info.selectionText === "Undefined" || info.selectionText === "") {
      console.log("dd")
    }
    else {
      const response = fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${OPENAI_API_KEY}`
        },
        body: JSON.stringify({
          "model": "gpt-3.5-turbo",
          "messages": [
            {
              "role": "user", 
              "content": `${info.selectionText}\n\n\nAnswer very briefly, if it is true or false, just say true or false. If the question contains options, just tell me if a or b or c or d. Bottom line, see to it that the answer is in one sentence and word count does not exceed 30 in the worst case.`
            }
          ]
        })
      })
      .then((response) => response.json())
      .then((data) => {
        const opts = {
          type: 'basic',
          iconUrl: chrome.runtime.getURL("icon.png"),
          title: 'notification title',
          message: data.choices[0].message.content
        }
        chrome.notifications.create('NOTFICATION_ID', opts)
      })
      .catch((error) => console.error(error));
    }
  }

  getChatGPTResponse();

});
