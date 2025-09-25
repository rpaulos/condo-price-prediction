class ScrollAnimations {
    constructor() {
        this.observers = [];
        this.init();
    }

    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupAnimations());
        } else {
            this.setupAnimations();
        }
    }

    setupAnimations() {
        this.createObserver();
        
        this.addAnimationClasses();
        
        this.setupHeroAnimations();
        this.setupFeatureAnimations();
        // this.setupPreviewAnimations();
        this.setupDeveloperAnimations();
    }

    createObserver() {
        const options = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    
                    if (entry.target.hasAttribute('data-stagger')) {
                        this.handleStaggeredAnimation(entry.target);
                    }
                }
            });
        }, options);
    }

    addAnimationClasses() {
        const heroTitle = document.querySelector('.hero-title');
        const heroSubtitle = document.querySelector('.hero-subtitle');
        const heroDescription = document.querySelector('.hero-description');
        const heroBuilding = document.querySelector('.hero-building');
        const logoIcon = document.querySelector('.logo-icon');

        if (heroTitle) {
            heroTitle.classList.add('fade-up');
            heroTitle.setAttribute('data-delay', '0.2');
        }
        if (heroSubtitle) {
            heroSubtitle.classList.add('fade-up');
            heroSubtitle.setAttribute('data-delay', '0.4');
        }
        if (heroDescription) {
            heroDescription.classList.add('fade-up');
            heroDescription.setAttribute('data-delay', '0.6');
        }
        if (heroBuilding) {
            heroBuilding.classList.add('slide-up');
            heroBuilding.setAttribute('data-delay', '0.8');
        }
        if (logoIcon) {
            logoIcon.classList.add('bounce-in');
            logoIcon.setAttribute('data-delay', '1.0');
        }

        const featuresTitle = document.querySelector('.features-section .section-title');
        const featuresDescription = document.querySelector('.features-section .section-description');
        const featureCards = document.querySelectorAll('.feature-card');

        if (featuresTitle) {
            featuresTitle.classList.add('fade-up');
            this.observer.observe(featuresTitle);
        }
        if (featuresDescription) {
            featuresDescription.classList.add('fade-up');
            featuresDescription.setAttribute('data-delay', '0.2');
            this.observer.observe(featuresDescription);
        }

        featureCards.forEach((card, index) => {
            card.classList.add('slide-up');
            card.setAttribute('data-delay', `${0.3 + (index * 0.2)}`);
            this.observer.observe(card);
        });

        const previewTitle = document.querySelector('.preview-section .section-title');
        const previewDescription = document.querySelector('.preview-section .section-description');
        const previewCards = document.querySelectorAll('.preview-card');

        console.log('Preview elements found:', {
            title: !!previewTitle,
            description: !!previewDescription,
            cards: previewCards.length
        });

        if (previewTitle) {
            previewTitle.classList.add('fade-up');
            this.observer.observe(previewTitle);
        }
        if (previewDescription) {
            previewDescription.classList.add('fade-up');
            previewDescription.setAttribute('data-delay', '0.2');
            this.observer.observe(previewDescription);
        }

        // previewCards.forEach((card, index) => {
        //     if (index === 0) {
        //         card.classList.add('slide-left');
        //     } else if (index === 1) {
        //         card.classList.add('scale-up');
        //     } else {
        //         card.classList.add('slide-right');
        //     }
        //     card.setAttribute('data-delay', `${0.3 + (index * 0.2)}`);
        //     this.observer.observe(card);
        // });

        const developersTitle = document.querySelector('.developers-section .section-title');
        const developersDescription = document.querySelector('.developers-section-description');
        const developerCards = document.querySelectorAll('.developer-card');

        if (developersTitle) {
            developersTitle.classList.add('fade-up');
            this.observer.observe(developersTitle);
        }
        if (developersDescription) {
            developersDescription.classList.add('fade-up');
            developersDescription.setAttribute('data-delay', '0.2');
            this.observer.observe(developersDescription);
        }

        developerCards.forEach((card, index) => {
            card.classList.add('slide-up');
            card.setAttribute('data-delay', `${0.3 + (index * 0.15)}`);
            this.observer.observe(card);
        });

        const footer = document.querySelector('.footer');
        if (footer) {
            footer.classList.add('fade-up');
            this.observer.observe(footer);
        }
    }

    setupHeroAnimations() {
        setTimeout(() => {
            const heroElements = document.querySelectorAll('.hero-section [class*="fade"], .hero-section [class*="slide"], .hero-section [class*="bounce"]');
            heroElements.forEach(element => {
                element.classList.add('animate-in');
            });
        }, 500);
    }

    setupFeatureAnimations() {
        const featureCards = document.querySelectorAll('.feature-card');
        featureCards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-10px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(-5px) scale(1)';
            });
        });
    }

    // setupPreviewAnimations() {
    //     // Add subtle parallax effect only after the initial scroll animation
    //     const previewCards = document.querySelectorAll('.preview-card');
    //     let initialAnimationComplete = false;
        
    //     // Wait for initial animations to complete
    //     setTimeout(() => {
    //         initialAnimationComplete = true;
    //     }, 2000);
        
    //     window.addEventListener('scroll', () => {
    //         if (!initialAnimationComplete) return;
            
    //         const scrolled = window.pageYOffset;
    //         const previewSection = document.querySelector('.preview-section');
            
    //         if (previewSection) {
    //             const rect = previewSection.getBoundingClientRect();
    //             const isVisible = rect.top < window.innerHeight && rect.bottom > 0;
                
    //             if (isVisible) {
    //                 previewCards.forEach((card, index) => {
    //                     const parallaxSpeed = 0.02; // Much gentler parallax
    //                     const movement = scrolled * parallaxSpeed * (index - 1);
                        
    //                     // Only apply parallax if the card has already animated in
    //                     if (card.classList.contains('animate-in')) {
    //                         card.style.transform = `translateY(${movement}px)`;
    //                     }
    //                 });
    //             }
    //         }
    //     });
    // }

    setupDeveloperAnimations() {
        const developerCards = document.querySelectorAll('.developer-card');
        
        developerCards.forEach((card, index) => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-8px) scale(1.02)';
                card.style.boxShadow = '0 20px 40px rgba(66, 121, 246, 0.3)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(-5px) scale(1)';
                card.style.boxShadow = '';
            });
        });
    }

    handleStaggeredAnimation(parent) {
        const children = parent.querySelectorAll('[data-stagger-child]');
        children.forEach((child, index) => {
            setTimeout(() => {
                child.classList.add('animate-in');
            }, index * 100);
        });
    }
}

new ScrollAnimations();

document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-links a, .footer-nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            if (href.startsWith('#')) {
                e.preventDefault();
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    const offsetTop = targetElement.offsetTop - 100;
                    
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
});

window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    const navBackground = document.querySelector('.nav-background');
    
    if (window.scrollY > 50) {
        navBackground.style.backgroundColor = 'rgba(252, 254, 255, 0.95)';
        navBackground.style.backdropFilter = 'blur(10px)';
        navBackground.style.borderBottom = '1px solid rgba(66, 121, 246, 0.1)';
    } else {
        navBackground.style.backgroundColor = '#fcfeff';
        navBackground.style.backdropFilter = 'none';
        navBackground.style.borderBottom = 'none';
    }
});