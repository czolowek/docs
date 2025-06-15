// Cyberpunk 2077 Database JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all cyberpunk effects
    initMatrixBackground();
    initTypingEffect();
    initGlitchEffects();
    initCounterAnimation();
    initFormEnhancements();
    initHoverEffects();
});

// Matrix-style background effect
function initMatrixBackground() {
    const canvas = document.createElement('canvas');
    canvas.id = 'matrix-bg';
    canvas.style.position = 'fixed';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.zIndex = '-2';
    canvas.style.pointerEvents = 'none';
    canvas.style.opacity = '0.05';
    
    document.body.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = [];
    
    for (let i = 0; i < columns; i++) {
        drops[i] = 1;
    }
    
    function draw() {
        ctx.fillStyle = 'rgba(10, 10, 10, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#00ff88';
        ctx.font = fontSize + 'px monospace';
        
        for (let i = 0; i < drops.length; i++) {
            const text = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    
    setInterval(draw, 100);
}

// Typing effect for titles
function initTypingEffect() {
    const elements = document.querySelectorAll('[data-typing]');
    
    elements.forEach(element => {
        const text = element.textContent;
        element.textContent = '';
        element.style.borderRight = '2px solid #00ff88';
        
        let i = 0;
        const timer = setInterval(() => {
            element.textContent += text.charAt(i);
            i++;
            
            if (i > text.length) {
                clearInterval(timer);
                setTimeout(() => {
                    element.style.borderRight = 'none';
                }, 500);
            }
        }, 100);
    });
}

// Random glitch effects
function initGlitchEffects() {
    const glitchElements = document.querySelectorAll('.glitch-text');
    
    glitchElements.forEach(element => {
        setInterval(() => {
            if (Math.random() > 0.95) {
                element.style.textShadow = `
                    ${Math.random() * 5}px 0 #ff073a,
                    ${Math.random() * -5}px 0 #00ff88,
                    ${Math.random() * 5}px 0 #39ff14
                `;
                
                setTimeout(() => {
                    element.style.textShadow = '0 0 10px rgba(0, 255, 136, 0.5)';
                }, 100);
            }
        }, 2000);
    });
}

// Animated counters for statistics
function initCounterAnimation() {
    const counters = document.querySelectorAll('.stat-number');
    
    const animateCounter = (element) => {
        const target = parseInt(element.textContent);
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            element.textContent = Math.floor(current);
            
            if (current >= target) {
                element.textContent = target;
                clearInterval(timer);
            }
        }, 16);
    };
    
    // Intersection Observer for triggering animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    });
    
    counters.forEach(counter => {
        observer.observe(counter);
    });
}

// Enhanced form interactions
function initFormEnhancements() {
    // Auto-complete suggestions with cyber styling
    const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"]');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.boxShadow = '0 0 15px rgba(0, 255, 136, 0.4)';
            this.style.borderColor = '#00ff88';
        });
        
        input.addEventListener('blur', function() {
            this.style.boxShadow = '';
            this.style.borderColor = '#333333';
        });
        
        // Cyber typing sound effect (visual feedback)
        input.addEventListener('input', function() {
            this.style.color = '#00ff88';
            setTimeout(() => {
                this.style.color = '#ffffff';
            }, 200);
        });
    });
    
    // Enhanced search functionality
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            
            // Visual feedback for search
            this.style.borderColor = '#39ff14';
            this.style.boxShadow = '0 0 20px rgba(57, 255, 20, 0.3)';
            
            searchTimeout = setTimeout(() => {
                this.style.borderColor = '#00ff88';
                this.style.boxShadow = '0 0 15px rgba(0, 255, 136, 0.4)';
            }, 1000);
        });
    }
}

// Interactive hover effects
function initHoverEffects() {
    // Card hover effects
    const cards = document.querySelectorAll('.card, .person-card, .stat-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
            this.style.boxShadow = '0 10px 30px rgba(0, 255, 136, 0.3)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
            this.style.boxShadow = '';
        });
    });
    
    // Button scan line effect
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            const scanLine = document.createElement('div');
            scanLine.style.position = 'absolute';
            scanLine.style.top = '0';
            scanLine.style.left = '-100%';
            scanLine.style.width = '100%';
            scanLine.style.height = '100%';
            scanLine.style.background = 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent)';
            scanLine.style.transition = 'left 0.5s ease';
            scanLine.style.pointerEvents = 'none';
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(scanLine);
            
            setTimeout(() => {
                scanLine.style.left = '100%';
            }, 10);
            
            setTimeout(() => {
                if (scanLine.parentNode) {
                    scanLine.parentNode.removeChild(scanLine);
                }
            }, 510);
        });
    });
}

// Search functionality enhancements
function enhanceSearch() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('input[name="q"]');
    const searchType = document.querySelector('select[name="type"]');
    
    if (searchForm && searchInput) {
        // Real-time search suggestions
        let suggestionTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(suggestionTimeout);
            
            if (this.value.length > 2) {
                suggestionTimeout = setTimeout(() => {
                    // Visual feedback for active searching
                    this.style.borderColor = '#39ff14';
                    this.parentElement.style.position = 'relative';
                    
                    // Add scanning animation
                    const scanner = document.createElement('div');
                    scanner.className = 'search-scanner';
                    scanner.style.cssText = `
                        position: absolute;
                        top: 0;
                        left: 0;
                        right: 0;
                        height: 2px;
                        background: linear-gradient(90deg, transparent, #00ff88, transparent);
                        animation: scanner-move 1s ease-in-out infinite;
                    `;
                    
                    this.parentElement.appendChild(scanner);
                    
                    setTimeout(() => {
                        if (scanner.parentNode) {
                            scanner.parentNode.removeChild(scanner);
                        }
                        this.style.borderColor = '#00ff88';
                    }, 1000);
                }, 300);
            }
        });
    }
}

// Initialize enhanced search
document.addEventListener('DOMContentLoaded', enhanceSearch);

// Add CSS animations dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes scanner-move {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(300%); }
    }
    
    .search-scanner {
        z-index: 10;
    }
    
    .cyber-pulse {
        animation: cyber-pulse 2s ease-in-out infinite;
    }
    
    @keyframes cyber-pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
`;
document.head.appendChild(style);

// Terminal-style console logging
console.log(`
╔══════════════════════════════════════════════════════════════╗
║                    CYBERPUNK DATABASE 2077                   ║
║                        SYSTEM ONLINE                         ║
╠══════════════════════════════════════════════════════════════╣
║ Status: OPERATIONAL                                          ║
║ Security Level: MAXIMUM                                      ║
║ Access Granted: AUTHENTICATED USER                           ║
╚══════════════════════════════════════════════════════════════╝
`);
