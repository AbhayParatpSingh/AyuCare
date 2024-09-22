console.log('JS Loaded'); // For testing if the file loads



document.addEventListener('DOMContentLoaded', () => {
    // Function to toggle the dropdown menu
    function toggleUserMenu() {
        const dropdown = document.getElementById('user-menu');
        dropdown.classList.toggle('hidden');  // This adds/removes the 'hidden' class
        console.log('Dropdown toggled');
    }

    // Event listener for the button
    document.getElementById('user-menu-button').addEventListener('click', (event) => {
        event.stopPropagation();  // Prevent click event from bubbling up and closing the dropdown
        toggleUserMenu();
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', function(event) {
        const dropdown = document.getElementById('user-menu');
        const button = document.getElementById('user-menu-button');

        if (!dropdown.contains(event.target) && !button.contains(event.target)) {
            dropdown.classList.add('hidden');  // Ensure the dropdown is hidden
            console.log('Dropdown closed');
        }
    });

    // Close dropdown when a menu item is clicked
    const menuItems = document.querySelectorAll('[role="menuitem"]');
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            const dropdown = document.getElementById('user-menu');
            dropdown.classList.add('hidden');  // Ensure the dropdown is hidden
            console.log('Dropdown closed by menu item');
        });
    });
});
