function openSharePopup(event) {
    event.preventDefault(); // Prevent default link behavior

    // Get the popup element
    const popup = document.getElementById('share-popup');
    const overlay = document.querySelector('.overlay');  // Look for existing overlay

    // Check if the popup is already visible
    if (popup.style.display === 'block') {
        // If visible, hide the popup and remove the overlay
        popup.style.display = 'none';
        if (overlay) {
            document.body.removeChild(overlay);
        }
    } else {
        // If not visible, create an overlay and show the popup
        const overlay = document.createElement('div');
        overlay.classList.add('overlay');
        document.body.appendChild(overlay);

        // Show the popup
        popup.style.display = 'block';

        // Close the popup when clicking outside the popup (on overlay)
        overlay.addEventListener('click', function() {
            popup.style.display = 'none';
            document.body.removeChild(overlay);  // Remove the overlay
        });

        // Prevent closing the popup when clicking inside the popup itself
        popup.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    }
}
