import { OPENAI_API_KEY } from "./env.js";

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    title: "TrueOrFalse",
    contexts: ["all"],
    id: "TrueOrFalse"
  });
});

chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    title: "MCQ",
    contexts: ["all"],
    id: "MCQ"
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {

  function getChatGPTResponse(extras) {
    if (info.selectionText === undefined || info.selectionText === "Undefined" || info.selectionText === "") {
      console.log("pass")
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
              "content": `${info.selectionText}${extras}`
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
  
  if (info.menuItemId === "TrueOrFalse") {
    getChatGPTResponse("\n\n\nAnswer very briefly, just say true or false.")
  }
  if (info.menuItemId === "MCQ") {
    getChatGPTResponse("\n\n\nAnswer very briefly, just one pick item. Don't give any explanation or justification.")
  }

});
