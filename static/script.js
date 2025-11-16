
const productId = "{{product.id}}";
const bidButton = document.getElementById("bidButton");
const bidBar = document.getElementById("bidBar");
const stKey = "bid_" + productId;
const lastBidTyped = localStorage.getItem(stKey);


if(lastBidTyped){
  bidBar.value = lastBidTyped;
}
bidButton.addEventListener("click", () => {
  localStorage.setItem(stKey, bidBar.value);
});