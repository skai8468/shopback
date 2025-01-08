document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('buylinkButton').addEventListener('click', function() {
        window.location.href = "/buy";
    });

    document.getElementById('stamplinkButton').addEventListener('click', function() {
        window.location.href = "/stampcard";
    });
});

document.getElementById("add-store-bar").addEventListener("click", () => {
    const storeName = prompt("Enter the store name:");
    const storeLogo = prompt("Enter the store logo URL:");
    if (!storeName || !storeLogo) return;

    const storeGrid = document.querySelector(".store-grid");

    // Create a new store bar
    const storeBar = document.createElement("div");
    storeBar.className = "store-bar";

    // Store logo
    const logo = document.createElement("img");
    logo.src = storeLogo;
    logo.alt = `${storeName} Logo`;
    logo.className = "store-logo";

    // Stampcards container
    const stampCardsContainer = document.createElement("div");
    stampCardsContainer.className = "stampcards";

    // Add default stamps
    for (let i = 0; i < 3; i++) {
        const stamp = document.createElement("img");
        stamp.src = "https://andlarry.com/wp-content/uploads/2022/11/SB-AndL-Thumbnail-1.jpg";
        stamp.alt = "ShopBack Stamp";
        stampCardsContainer.appendChild(stamp);
    }

    // Append logo and stampcards to store bar
    storeBar.appendChild(logo);
    storeBar.appendChild(stampCardsContainer);

    // Append store bar to the grid
    storeGrid.appendChild(storeBar);
});
