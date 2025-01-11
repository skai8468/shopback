let join = document.getElementById("join-btn");

//function joinnow() {
  //window.open('https://www.nike.com/sg/?cp=20906733152_search_%7Csg%7CCore+Brand+-+Core+Brand+-+General+-+EN_EN%7CMICROSOFT%7Cnike&&msclkid=4148a1e85cec1b36e1b9c69615f440eb&utm_source=bing&utm_medium=cpc&utm_campaign=Core%20Brand%20-%20Core%20Brand%20-%20General%20-%20EN_EN&utm_term=nike&utm_content=General%20-%20Core&gclid=4148a1e85cec1b36e1b9c69615f440eb&gclsrc=3p.ds', '_blank');
//}

function toggleLike(button) {
  if (button.classList.contains("liked")) {
      // If already liked, remove the "liked" state
      button.classList.remove("liked");
      button.style.backgroundColor = ""; // Reset background color
      button.style.color = ""; // Reset text color
  } else {
      // If not liked, add the "liked" state
      button.classList.add("liked");
      button.style.backgroundColor = "blue"; // Set background color to blue
      button.style.color = "white"; // Set text color to white
  }
}

function addFriend(button) {
  button.textContent = "Added";
  button.style.backgroundColor = "green";
  button.style.cursor = "not-allowed";
  button.disabled = true; // Disable the button after adding
}