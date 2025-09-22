VANTA.GLOBE({
    el: "#vanta-bg",
    mouseControls: true,
    touchControls: true,
    gyroControls: false,
    minHeight: 200.00,
    minWidth: 200.00,
    scale: 1.00,
    scaleMobile: 1.00,
    color: 0x00ffff,
    backgroundColor: 0x0,
    size: 0.8
});

// Toggle new list form
document.getElementById('new-list-btn').addEventListener('click', function() {
    const form = document.getElementById('new-list-form');
    form.classList.toggle('hidden');
});

// Also handle the main create list button if no list is selected
if (document.getElementById('new-list-btn-main')) {
    document.getElementById('new-list-btn-main').addEventListener('click', function() {
        const form = document.getElementById('new-list-form');
        form.classList.toggle('hidden');
        // Scroll to the form if it's now visible
        if (!form.classList.contains('hidden')) {
            form.scrollIntoView({ behavior: 'smooth' });
        }
    });
}

AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true
});
feather.replace();