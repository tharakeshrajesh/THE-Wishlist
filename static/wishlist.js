const itemsContainer = document.getElementById("wishlistItems");

document.getElementById("backButton").onclick = () => {
    window.location.href = '/';
}

async function loadItems() {
    const response = await fetch('/req');
    const items = await response.json();
    
    itemsContainer.innerHTML = '';
    items.forEach(item => {
        const element = document.createElement("p");
        element.textContent = `${item.name} wants ${item.item}!`;
        itemsContainer.appendChild(element);
    });
}

loadItems();