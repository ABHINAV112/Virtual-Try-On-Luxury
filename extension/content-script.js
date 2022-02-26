chrome.runtime.onMessage.addListener(function (
  { action },
  sender,
  sendResponse
) {
  if (action == "get-images") {
    const collection = document.getElementsByTagName("img");
    const collectionSrcs = [];
    for (let i = 0; i < collection.length; i++) {
      collectionSrcs.push(collection[i].src);
    }
    sendResponse({ images: collectionSrcs });
    return true;
  }
});
