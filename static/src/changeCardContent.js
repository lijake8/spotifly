function generateTiles(items, mainContent, tileTemplate) {
  mainContent.innerHTML = "";
  items.forEach(function (item) {
    var tileClone = tileTemplate.cloneNode(true);
    tileClone.querySelector("h3").textContent = item.title;
    tileClone.querySelector("p").textContent = item.description;
    mainContent.appendChild(tileClone);
  })
}

var button1 = document.getElementById("button1");
var button2 = document.getElementById("button2");
var mainContent = document.getElementById("mainContent");
var tileTemplate = document.getElementById("tile-template").content;

button1.addEventListener("click", function () {
  generateTiles(items1, mainContent, tileTemplate);
});

button2.addEventListener("click", function () {
  generateTiles(items2, mainContent, tileTemplate);
});
