/* ===== ANIMATIONS AU SCROLL ===== */

class ScrollAnimations {
    constructor() {
        this.animatedElements = [];
        this.observer = null;
        this.init();
    }

    init() {
        this.setupIntersectionObserver();
        this.addScrollAnimations();
        this.addHoverEffects();
    }

    setupIntersectionObserver() {
        // Configuration de l'observateur d'intersection
        const options = {
            root: null,
            rootMargin: '0px',
            threshold: 0.1
        };

        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateElement(entry.target);
                }
            });
        }, options);
    }

    addScrollAnimations() {
        // Sélectionner tous les éléments à animer
        const elements = document.querySelectorAll('.scroll-animate, .uniform-card, .promotion-card, .structure-card, .plat-card');
        
        elements.forEach((element, index) => {
            // Ajouter la classe scroll-animate si elle n'existe pas
            if (!element.classList.contains('scroll-animate')) {
                element.classList.add('scroll-animate');
            }
            
            // Ajouter un délai progressif pour les cartes
            if (element.classList.contains('uniform-card') || 
                element.classList.contains('promotion-card') || 
                element.classList.contains('structure-card') || 
                element.classList.contains('plat-card')) {
                element.style.animationDelay = `${index * 0.1}s`;
            }
            
            // Observer l'élément
            this.observer.observe(element);
        });
    }

    animateElement(element) {
        // Ajouter la classe d'animation
        element.classList.add('animate-in');
        
        // Ajouter des animations spécifiques selon le type d'élément
        if (element.classList.contains('uniform-card')) {
            this.animateCard(element);
        } else if (element.classList.contains('promotion-card')) {
            this.animatePromotionCard(element);
        } else if (element.classList.contains('structure-card')) {
            this.animateStructureCard(element);
        } else if (element.classList.contains('plat-card')) {
            this.animatePlatCard(element);
        }
    }

    animateCard(element) {
        // Animation d'entrée pour les cartes uniformes
        element.style.animation = 'fadeInUp 0.8s ease-out forwards';
        
        // Ajouter des effets de hover
        element.addEventListener('mouseenter', () => {
            element.style.transform = 'translateY(-8px) scale(1.02)';
            element.style.boxShadow = '0 12px 30px rgba(0, 0, 0, 0.2)';
        });
        
        element.addEventListener('mouseleave', () => {
            element.style.transform = 'translateY(0) scale(1)';
            element.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
        });
    }

    animatePromotionCard(element) {
        // Animation spécifique pour les cartes de promotion
        element.style.animation = 'fadeInUp 0.8s ease-out forwards';
        
        // Animation du badge de promotion
        const badge = element.querySelector('.promotion-badge');
        if (badge) {
            badge.style.animation = 'pulse 2s infinite';
        }
        
        // Animation de l'image au hover
        const image = element.querySelector('.promotion-image');
        if (image) {
            element.addEventListener('mouseenter', () => {
                image.style.transform = 'scale(1.1)';
            });
            
            element.addEventListener('mouseleave', () => {
                image.style.transform = 'scale(1)';
            });
        }
    }

    animateStructureCard(element) {
        // Animation spécifique pour les cartes de structure
        element.style.animation = 'fadeInUp 0.8s ease-out forwards';
        
        // Animation de la note
        const rating = element.querySelector('.rating-display');
        if (rating) {
            rating.style.animation = 'fadeInUp 0.8s ease-out 0.2s both';
        }
    }

    animatePlatCard(element) {
        // Animation spécifique pour les cartes de plat
        element.style.animation = 'fadeInUp 0.8s ease-out forwards';
        
        // Animation du badge de catégorie
        const categoryBadge = element.querySelector('.img-badge');
        if (categoryBadge) {
            categoryBadge.style.animation = 'fadeInUp 0.6s ease-out 0.3s both';
        }
    }

    addHoverEffects() {
        // Ajouter des effets de hover pour tous les boutons
        const buttons = document.querySelectorAll('.btn, .uniform-btn');
        buttons.forEach(button => {
            button.addEventListener('mouseenter', () => {
                button.style.transform = 'translateY(-2px)';
                button.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.15)';
            });
            
            button.addEventListener('mouseleave', () => {
                button.style.transform = 'translateY(0)';
                button.style.boxShadow = '';
            });
        });
    }

    // Méthode pour réinitialiser les animations
    resetAnimations() {
        const elements = document.querySelectorAll('.scroll-animate');
        elements.forEach(element => {
            element.classList.remove('animate-in');
            element.style.animation = '';
        });
    }

    // Méthode pour forcer l'animation d'un élément
    forceAnimate(element) {
        if (element) {
            this.animateElement(element);
        }
    }
}

// Initialisation des animations au scroll
document.addEventListener('DOMContentLoaded', () => {
    // Créer l'instance des animations
    window.scrollAnimations = new ScrollAnimations();
    
    // Ajouter des animations pour les éléments qui se chargent dynamiquement
    if (typeof MutationObserver !== 'undefined') {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    mutation.addedNodes.forEach((node) => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            const cards = node.querySelectorAll('.uniform-card, .promotion-card, .structure-card, .plat-card');
                            cards.forEach(card => {
                                if (!card.classList.contains('scroll-animate')) {
                                    card.classList.add('scroll-animate');
                                    window.scrollAnimations.observer.observe(card);
                                }
                            });
                        }
                    });
                }
            });
        });
        
        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }
});

// Fonction utilitaire pour ajouter des animations manuellement
function addScrollAnimation(element, delay = 0) {
    if (window.scrollAnimations && element) {
        element.style.animationDelay = `${delay}s`;
        element.classList.add('scroll-animate');
        window.scrollAnimations.observer.observe(element);
    }
}

// Fonction pour animer une liste de cartes avec délai progressif
function animateCardList(container, cardSelector = '.uniform-card, .promotion-card, .structure-card, .plat-card') {
    if (window.scrollAnimations && container) {
        const cards = container.querySelectorAll(cardSelector);
        cards.forEach((card, index) => {
            addScrollAnimation(card, index * 0.1);
        });
    }
}

// Export pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ScrollAnimations;
}
