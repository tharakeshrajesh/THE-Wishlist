const form = document.getElementById("wishlistForm")

document.getElementById("viewWishlistButton").addEventListener("click", () => {
    window.location.href = '/wishlist';
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    let name = form.elements.name.value;
    const item = form.elements.wishlistitem.value;

    !name ? name = "anonymous" : name

    await fetch('/req', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name, item })
    });

    form.reset();
});
