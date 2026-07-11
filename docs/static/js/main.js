document.addEventListener('DOMContentLoaded', () => {
    // Interactive Avatar
    const avatar = document.getElementById('interactive-avatar');
    const isTouchDevice = (('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0));

    if (avatar && !isTouchDevice) {
        let mouseX = 0, mouseY = 0;
        let targetX = 0, targetY = 0;
        
        document.addEventListener('mousemove', (e) => {
            mouseX = (e.clientX / window.innerWidth) * 2 - 1;
            mouseY = (e.clientY / window.innerHeight) * 2 - 1;
        });

        document.addEventListener('mouseleave', () => {
            mouseX = 0; mouseY = 0;
        });

        function animateAvatar() {
            targetX += (mouseX - targetX) * 0.1;
            targetY += (mouseY - targetY) * 0.1;
            avatar.style.transform = `rotateX(${targetY * -6}deg) rotateY(${targetX * 8}deg)`;
            requestAnimationFrame(animateAvatar);
        }
        animateAvatar();
    }

    // GSAP Scroll Animations
    gsap.registerPlugin(ScrollTrigger);
    
    const commonScrollTrigger = (triggerElement) => ({
        trigger: triggerElement,
        start: "top 85%",
        toggleActions: "play reverse play reverse"
    });

    gsap.from("#home > div > div", { y: 40, opacity: 0, duration: 0.6, ease: "power2.out", stagger: 0.2, scrollTrigger: commonScrollTrigger("#home") });
    gsap.from("#about > div", { x: -40, opacity: 0, duration: 0.6, ease: "power2.out", stagger: 0.2, scrollTrigger: commonScrollTrigger("#about") });
    gsap.from("#skills .grid > div", { y: 40, opacity: 0, duration: 0.6, ease: "power2.out", stagger: 0.1, scrollTrigger: commonScrollTrigger("#skills") });
    gsap.from("#projects .grid > div", { y: 40, opacity: 0, duration: 0.6, ease: "power2.out", stagger: 0.2, scrollTrigger: commonScrollTrigger("#projects") });
    gsap.from("#experience .border-l > div", { y: 40, opacity: 0, duration: 0.6, ease: "power2.out", stagger: 0.15, scrollTrigger: commonScrollTrigger("#experience") });
    gsap.from("#education .border-l > div", { y: 40, opacity: 0, duration: 0.6, ease: "power2.out", stagger: 0.15, scrollTrigger: commonScrollTrigger("#education") });
    gsap.from("#contact > div", { y: 40, opacity: 0, duration: 0.6, ease: "power2.out", stagger: 0.2, scrollTrigger: commonScrollTrigger("#contact") });

    // Navbar shadow effect & Scroll Progress Bar
    const navbar = document.getElementById('navbar');
    const scrollProgress = document.getElementById('scroll-progress');
    
    window.addEventListener('scroll', () => {
        // Navbar shadow & opaque background
        if (window.scrollY > 50) {
            navbar.classList.remove('bg-transparent', 'border-transparent');
            navbar.classList.add('bg-white/90', 'backdrop-blur-md', 'border-black/[0.04]', 'shadow-sm');
        } else {
            navbar.classList.add('bg-transparent', 'border-transparent');
            navbar.classList.remove('bg-white/90', 'backdrop-blur-md', 'border-black/[0.04]', 'shadow-sm');
        }
        
        // Scroll Progress
        if (scrollProgress) {
            const scrollTop = window.scrollY;
            const docHeight = document.body.scrollHeight - window.innerHeight;
            const scrollPercent = (scrollTop / docHeight) * 100;
            scrollProgress.style.width = scrollPercent + '%';
        }
    });

    // Scroll Spy for Navigation Links
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');

    const scrollSpyObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, {
        threshold: 0.3,
        rootMargin: "-20% 0px -60% 0px"
    });

    sections.forEach(section => {
        scrollSpyObserver.observe(section);
    });

    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIconOpen = document.getElementById('menu-icon-open');
    const menuIconClose = document.getElementById('menu-icon-close');
    const mobileLinks = document.querySelectorAll('.mobile-link');
    
    function toggleMobileMenu() {
        const isExpanded = mobileMenuButton.getAttribute('aria-expanded') === 'true';
        mobileMenuButton.setAttribute('aria-expanded', !isExpanded);
        
        if (!isExpanded) {
            // Open menu
            mobileMenu.classList.remove('-translate-y-full');
            menuIconOpen.classList.add('hidden');
            menuIconClose.classList.remove('hidden');
            document.body.classList.add('overflow-hidden'); // Prevent scrolling
        } else {
            // Close menu
            mobileMenu.classList.add('-translate-y-full');
            menuIconOpen.classList.remove('hidden');
            menuIconClose.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
        }
    }

    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', toggleMobileMenu);
    }

    // Close mobile menu when a link is clicked
    mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (mobileMenuButton.getAttribute('aria-expanded') === 'true') {
                toggleMobileMenu();
            }
        });
    });
});
