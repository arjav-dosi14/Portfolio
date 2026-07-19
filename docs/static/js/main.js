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

    // --- Intersection Observer for Scroll Reveal ---
    // Recursively finds semantic content blocks to animate inside a section
    function getLeafAnimatables(element) {
        let leaves = [];
        Array.from(element.children).forEach(child => {
            if (['STYLE', 'SCRIPT', 'NOSCRIPT', 'SVG'].includes(child.tagName)) return;
            
            // Check if it's a semantic block element
            if (['H1','H2','H3','H4','H5','H6','P','IMG','A','BUTTON','FORM','UL','LI'].includes(child.tagName)) {
                leaves.push(child);
            } 
            // Check if it's a card, badge, pill or distinct visual block
            else if (
                child.classList.contains('bg-white') || 
                child.classList.contains('bg-gray-50') || 
                child.classList.contains('bg-gray-100') ||
                child.classList.contains('bg-gray-900') ||
                child.classList.contains('bg-brand-alt') || 
                child.classList.contains('shadow-lg') || 
                child.classList.contains('shadow-sm') || 
                child.classList.contains('shadow-premium') ||
                child.classList.contains('border') ||
                child.tagName === 'SPAN'
            ) {
                leaves.push(child);
            } 
            else {
                // It's a structural container, go deeper
                leaves = leaves.concat(getLeafAnimatables(child));
            }
        });
        return leaves;
    }

    const sectionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const section = entry.target;
            const animatables = getLeafAnimatables(section);
            
            if (entry.isIntersecting) {
                // Entering viewport: stagger in
                animatables.forEach((el, index) => {
                    if (el.classList.contains('scroll-child-init')) {
                        setTimeout(() => {
                            el.classList.add('scroll-child-visible');
                        }, index * 100); // 100ms stagger delay
                    }
                });
            } else {
                // Leaving viewport: reset to hidden state
                animatables.forEach(el => {
                    if (el.classList.contains('scroll-child-init')) {
                        el.classList.remove('scroll-child-visible');
                    }
                });
            }
        });
    }, {
        threshold: 0.1, // Trigger slightly after it enters
        rootMargin: "0px 0px -10% 0px"
    });

    // Initialize all sections
    document.querySelectorAll('section').forEach(section => {
        const animatables = getLeafAnimatables(section);
        animatables.forEach(el => {
            el.classList.add('scroll-child-init');
        });
        sectionObserver.observe(section);
    });

    // --- Contact Form AJAX Handler ---
    const contactForm = document.querySelector('#contact form');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.innerHTML;
            
            // Loading state
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg> Sending...';
            submitBtn.classList.add('opacity-80', 'cursor-not-allowed');

            try {
                const formData = new FormData(contactForm);
                const response = await fetch(contactForm.action || '/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Accept': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (response.ok && data.status === 'success') {
                    showToast(data.message, 'success');
                    contactForm.reset();
                } else {
                    showToast(data.message || 'Something went wrong.', 'error');
                }
            } catch (error) {
                showToast('Unable to send your message. Please try again later.', 'error');
            } finally {
                // Restore button state
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnText;
                submitBtn.classList.remove('opacity-80', 'cursor-not-allowed');
            }
        });
    }

    // Modern Toast Notification Function
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `fixed bottom-6 right-6 px-6 py-4 rounded-xl shadow-2xl flex items-center gap-3 transform transition-all duration-500 translate-y-full opacity-0 z-[9999] ${
            type === 'success' ? 'bg-gray-900 text-white' : 'bg-red-50 text-red-900 border border-red-200'
        }`;
        
        // Icon
        const icon = type === 'success' 
            ? '<svg class="w-5 h-5 text-green-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>'
            : '<svg class="w-5 h-5 text-red-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>';
            
        toast.innerHTML = `${icon} <span class="text-[14px] font-medium tracking-wide">${message}</span>`;
        document.body.appendChild(toast);
        
        // Trigger animation in
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                toast.classList.remove('translate-y-full', 'opacity-0');
            });
        });
        
        // Remove after 4 seconds
        setTimeout(() => {
            toast.classList.add('translate-y-full', 'opacity-0');
            setTimeout(() => {
                toast.remove();
            }, 500);
        }, 4000);
    }

    // --- 3D Tilt Effect for Project Cards ---
    const projectCards = document.querySelectorAll('#projects .grid > div');
    
    // Only apply on devices with hover capability and if user prefers motion
    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches && 
        !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        
        projectCards.forEach(card => {
            const img = card.querySelector('img');
            let bounds;
            let isHovering = false;
            
            // Optimize painting
            card.style.willChange = 'transform, box-shadow';
            if (img) img.style.willChange = 'transform';
            
            card.addEventListener('mouseenter', () => {
                bounds = card.getBoundingClientRect();
                isHovering = true;
            });
            
            card.addEventListener('mousemove', (e) => {
                if (!isHovering) return;
                
                // Calculate mouse position relative to card center
                const mouseX = e.clientX - bounds.left;
                const mouseY = e.clientY - bounds.top;
                const centerX = bounds.width / 2;
                const centerY = bounds.height / 2;
                
                // Calculate rotation (-4 to 4 degrees)
                const rotateX = ((mouseY - centerY) / centerY) * -4; 
                const rotateY = ((mouseX - centerX) / centerX) * 4;
                
                requestAnimationFrame(() => {
                    // Smooth tracking transition
                    card.style.transition = 'transform 200ms ease-out, box-shadow 200ms ease-out';
                    card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
                    card.style.boxShadow = '0 25px 35px -5px rgba(0, 0, 0, 0.08), 0 15px 15px -5px rgba(0, 0, 0, 0.04)';
                    
                    if (img) {
                        img.style.transition = 'transform 200ms ease-out';
                        img.style.transform = 'scale3d(1.03, 1.03, 1.03)';
                    }
                });
            });
            
            card.addEventListener('mouseleave', () => {
                isHovering = false;
                
                requestAnimationFrame(() => {
                    // Smooth return transition
                    card.style.transition = 'transform 300ms ease-out, box-shadow 300ms ease-out';
                    card.style.transform = '';
                    card.style.boxShadow = '';
                    
                    if (img) {
                        img.style.transition = 'transform 300ms ease-out';
                        img.style.transform = '';
                    }
                    
                    // Clear inline transitions after animation completes to restore CSS control
                    setTimeout(() => {
                        if (!isHovering) {
                            card.style.transition = '';
                            if (img) img.style.transition = '';
                        }
                    }, 300);
                });
            });
            
            // Re-calculate bounds on scroll if hovering to prevent jitter
            window.addEventListener('scroll', () => {
                if (isHovering) {
                    bounds = card.getBoundingClientRect();
                }
            }, { passive: true });
        });
    }

    // --- Magnetic Primary Buttons ---
    const magneticButtons = document.querySelectorAll(`
        #home a,
        nav a[href$=".pdf"],
        #projects a,
        #contact button[type="submit"]
    `);

    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches && 
        !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        
        let mouseX = window.innerWidth / 2;
        let mouseY = window.innerHeight / 2;
        let isMoving = false;
        
        const updateMagneticButtons = () => {
            magneticButtons.forEach(btn => {
                const rect = btn.getBoundingClientRect();
                const btnCenterX = rect.left + rect.width / 2;
                const btnCenterY = rect.top + rect.height / 2;
                
                // Define the 80px magnetic trigger zone around the button
                if (mouseX > rect.left - 80 && mouseX < rect.right + 80 &&
                    mouseY > rect.top - 80 && mouseY < rect.bottom + 80) {
                    
                    const distX = mouseX - btnCenterX;
                    const distY = mouseY - btnCenterY;
                    
                    // Max distance from center to the trigger edge
                    const maxDistX = rect.width / 2 + 80;
                    const maxDistY = rect.height / 2 + 80;
                    
                    // Calculate translation (max 4px)
                    const moveX = (distX / maxDistX) * 4;
                    const moveY = (distY / maxDistY) * 4;
                    
                    btn.style.transition = 'transform 150ms ease-out';
                    btn.style.transform = `translate(${moveX}px, ${moveY}px)`;
                } else {
                    if (btn.style.transform !== '') {
                        // Smooth return when leaving the magnetic field
                        btn.style.transition = 'transform 300ms ease-out';
                        btn.style.transform = '';
                        
                        // Clean up inline transition after it finishes so original CSS transitions work
                        setTimeout(() => {
                            if (btn.style.transform === '') {
                                btn.style.transition = '';
                            }
                        }, 300);
                    }
                }
            });
            isMoving = false;
        };
        
        document.addEventListener('mousemove', (e) => {
            mouseX = e.clientX;
            mouseY = e.clientY;
            
            if (!isMoving) {
                isMoving = true;
                requestAnimationFrame(updateMagneticButtons);
            }
        }, { passive: true });
        
        window.addEventListener('scroll', () => {
            if (!isMoving) {
                isMoving = true;
                requestAnimationFrame(updateMagneticButtons);
            }
        }, { passive: true });
    }

    // --- Premium Skill Tooltips ---
    const tooltipData = {
        'Core Python': {
            projects: ['ShopSphere', 'Laptix', 'Portfolio'],
            purpose: 'Backend logic and server-side scripting.'
        },
        'Core / Adv Java': {
            projects: ['Hospital Management System'],
            purpose: 'Object-oriented enterprise application logic.'
        },
        'C / C++': {
            projects: [],
            purpose: 'Performance-critical data structures and algorithms.'
        },
        'HTML & MySQL': {
            projects: ['ShopSphere', 'Hospital Management System', 'Portfolio'],
            purpose: 'Web structuring and relational database management.'
        },
        'OOP': {
            projects: ['ShopSphere', 'Laptix', 'Hospital Management System'],
            purpose: 'Designing maintainable, modular software architectures.'
        },
        'NumPy & Pandas': {
            projects: [],
            purpose: 'Data analysis and numerical computations.'
        },
        'File & Exception Handling': {
            projects: ['ShopSphere', 'Laptix'],
            purpose: 'Robust data I/O and graceful error recovery.'
        },
        'JDBC Connectivity': {
            projects: ['Hospital Management System'],
            purpose: 'Connecting Java backends to MySQL databases.'
        },
        'JSP Servlets': {
            projects: ['Hospital Management System'],
            purpose: 'Server-side Java request handling and rendering.'
        },
        'DSA & App Dev': {
            projects: [],
            purpose: 'Optimized algorithms and modern application design.'
        },
        'DBMS & AI': {
            projects: [],
            purpose: 'Database optimization and intelligent feature integration.'
        }
    };

    const skillItems = document.querySelectorAll('#skills ul li');

    if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
        let activeTooltip = null;
        
        skillItems.forEach(item => {
            // Visual indicator that it's hoverable
            item.classList.add('cursor-default', 'transition-colors', 'duration-300', 'hover:text-blue-600');
            
            item.addEventListener('mouseenter', (e) => {
                const skillName = item.textContent.trim();
                const data = tooltipData[skillName];
                
                if (!data) return;
                
                const tooltip = document.createElement('div');
                tooltip.className = 'fixed z-[10000] bg-gray-900/95 backdrop-blur-md border border-gray-800 text-white p-5 rounded-2xl shadow-2xl max-w-[240px] pointer-events-none transform transition-all duration-300 opacity-0 scale-95 origin-bottom';
                
                let html = `<h4 class="font-bold text-[15px] text-blue-400 mb-3 flex items-center gap-2">
                                <svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                                ${skillName}
                            </h4>`;
                
                if (data.projects.length > 0) {
                    html += `<div class="mb-3">
                                <p class="text-[11px] uppercase tracking-widest text-gray-400 font-semibold mb-2">Used In</p>
                                <ul class="text-[13px] text-gray-200 space-y-1.5 ml-1 border-l-2 border-gray-700 pl-3">`;
                    data.projects.forEach(p => {
                        html += `<li>${p}</li>`;
                    });
                    html += `   </ul>
                             </div>`;
                }
                
                html += `<div class="pt-3 border-t border-gray-800/50">
                            <p class="text-[13px] text-gray-300 leading-relaxed">${data.purpose}</p>
                         </div>`;
                
                tooltip.innerHTML = html;
                document.body.appendChild(tooltip);
                activeTooltip = tooltip;
                
                const positionTooltip = (e) => {
                    if (!activeTooltip) return;
                    const offset = 20;
                    let x = e.clientX;
                    let y = e.clientY - offset;
                    
                    tooltip.style.left = '0';
                    tooltip.style.top = '0';
                    
                    const rect = tooltip.getBoundingClientRect();
                    
                    // Center above cursor, keep within viewport bounds
                    x = Math.max(16, Math.min(x - rect.width / 2, window.innerWidth - rect.width - 16));
                    y = y - rect.height;
                    
                    // Flip to bottom if out of viewport
                    if (y < 16) {
                        y = e.clientY + offset;
                        tooltip.classList.replace('origin-bottom', 'origin-top');
                    }
                    
                    tooltip.style.transform = `translate(${x}px, ${y}px) scale(1)`;
                };
                
                positionTooltip(e);
                
                requestAnimationFrame(() => {
                    tooltip.style.opacity = '1';
                });
                
                const moveHandler = (e) => positionTooltip(e);
                item.addEventListener('mousemove', moveHandler);
                
                item.addEventListener('mouseleave', () => {
                    item.removeEventListener('mousemove', moveHandler);
                    if (tooltip) {
                        tooltip.style.opacity = '0';
                        tooltip.style.transform = tooltip.style.transform.replace('scale(1)', 'scale(0.95)');
                        setTimeout(() => {
                            if (tooltip.parentNode) tooltip.remove();
                        }, 300);
                    }
                    activeTooltip = null;
                }, { once: true });
            });
        });
    }
});
