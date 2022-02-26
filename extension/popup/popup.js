let error = false;
let imageSrcs;
let imageIndex = 0;

const imageCarouselImg = document.getElementById("image-carousel-img");
chrome.storage.local.get(["key"], function (result) {
  if (result.key) {
    document.getElementById("display-pic").src = result.key;
    document.getElementById("pic-error").classList.add("hide");
  } else {
    error = "No photo uploaded";
  }
});

const onClickTab = (argument) => {
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
  eleHide.classList.remove("flex");

  eleShow.classList.remove("hide");
  eleShow.classList.add("flex");

  const apiResultDiv = document.getElementById("api-result");
  apiResultDiv.classList.remove("flex");
  apiResultDiv.classList.add("hide");
};

const tryClothButton = document.getElementById("try-cloth-button");
tryClothButton.addEventListener("click", () => {
  onClickTab("tryCloth");
});
const profileButton = document.getElementById("profile-button");
profileButton.addEventListener("click", () => {
  onClickTab("person");
});

const fileUpload = document.getElementById("file-upload");
fileUpload.addEventListener("change", (e) => {
  var image = fileUpload.files[0];
  var oFReader = new FileReader();
  oFReader.readAsDataURL(image);

  oFReader.onload = function (oFREvent) {
    document.getElementById("display-pic").src = oFREvent.target.result;
    chrome.storage.local.set({ key: oFREvent.target.result });
  };
});

const changeImage = (num) => {
  imageIndex += num;
  if (imageIndex < 0) {
    imageIndex = 0;
  }
  if (imageIndex >= imageSrcs.length) {
    imageIndex = imageSrcs.length - 1;
  }
  console.log(imageSrcs[imageIndex]);
  imageCarouselImg.src = imageSrcs[imageIndex];
};

document.getElementById("increment-image").addEventListener("click", () => {
  changeImage(1);
});
document.getElementById("decrement-image").addEventListener("click", () => {
  changeImage(-1);
});

chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
  chrome.tabs.sendMessage(tabs[0].id, { action: "get-images" }, function (res) {
    if (res) {
      imageSrcs = res.images;
      document.getElementById("loading").classList.add("hide");
      document.getElementById("image-carousel").classList.remove("hide");
      imageCarouselImg.src = imageSrcs[imageIndex];
    }
  });
});

const makeApiCall = async () => {
  const url = "https://avatars.dicebear.com/api/human/12321.svg";
  const res = await fetch(url);
  const blob = await res.blob();
  const imageObjectURL = URL.createObjectURL(blob);
  return imageObjectURL;
};

const tryOnButton = document.getElementById("try-on");
tryOnButton.addEventListener("click", async () => {
  const eleHide = document.getElementById("try-cloth");
  eleHide.classList.remove("flex");
  eleHide.classList.add("hide");

  const apiResultDiv = document.getElementById("api-result");
  apiResultDiv.classList.add("flex");
  apiResultDiv.classList.remove("hide");
  const imageBlobUrl = await makeApiCall();
  document.getElementById("loader").classList.add("hide");
  document.getElementById("result-img").src = imageBlobUrl;
});
