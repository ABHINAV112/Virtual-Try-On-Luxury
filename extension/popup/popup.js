const onClickTab = (argument) => {
  console.log(argument);
  let eleShow = null;
  let eleHide = null;
  if (argument == "tryCloth") {
    eleShow = document.getElementById("try-cloth");
    eleHide = document.getElementById("profile");
  } else {
    eleShow = document.getElementById("profile");
    eleHide = document.getElementById("try-cloth");
  }
  eleHide.classList.add("hide");
  eleShow.classList.remove("hide");
};

const tryClothButton = document.getElementById("try-cloth-button");
tryClothButton.addEventListener("click", () => {
  onClickTab("tryCloth");
});
const profileButton = document.getElementById("profile-button");
profileButton.addEventListener("click", () => {
  onClickTab("person");
});

// let changeColor = document.getElementById("changeColor");

// chrome.storage.sync.get("color", ({ color }) => {
//   changeColor.style.backgroundColor = color;
// });

// // When the button is clicked, inject setPageBackgroundColor into current page
// changeColor.addEventListener("click", async () => {
//   let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

//   chrome.scripting.executeScript({
//     target: { tabId: tab.id },
//     function: setPageBackgroundColor,
//   });
// });

// // The body of this function will be executed as a content script inside the
// // current page
// function setPageBackgroundColor() {
//   chrome.storage.sync.get("color", ({ color }) => {
//     document.body.style.backgroundColor = color;
//   });
// }
