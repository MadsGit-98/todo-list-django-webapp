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

AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true
});

feather.replace();