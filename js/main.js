// Main JavaScript file for Nose Cleaner

// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });

        // Close mobile menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    }

    // Update current year
    const currentYear = new Date().getFullYear();
    const yearElements = document.querySelectorAll('[id^="current-year"]');
    yearElements.forEach(element => {
        element.textContent = currentYear;
    });

    // Newsletter form handling
    const newsletterForm = document.getElementById('newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            
            if (email) {
                // Simple email validation
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (emailRegex.test(email)) {
                    // Show success message
                    showNotification('Thank you for subscribing! You\'ll receive our latest updates soon.', 'success');
                    this.reset();
                } else {
                    showNotification('Please enter a valid email address.', 'error');
                }
            }
        });
    }

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add fade-in animation to elements when they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.product-card, .article-card, .nav-card');
    animatedElements.forEach(el => observer.observe(el));

    // Cost calculator functionality
    initializeCostCalculator();
});

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
    `;

    // Add to page
    document.body.appendChild(notification);

    // Close button functionality
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.remove();
    });

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Cost calculator for nasal irrigators
function initializeCostCalculator() {
    const calculatorContainer = document.querySelector('.cost-calculator');
    if (!calculatorContainer) return;

    const calculateButton = calculatorContainer.querySelector('.calculate-btn');
    const resultDiv = calculatorContainer.querySelector('.calculation-result');

    if (calculateButton && resultDiv) {
        calculateButton.addEventListener('click', function() {
            const deviceCost = parseFloat(calculatorContainer.querySelector('#device-cost').value) || 0;
            const saltPodCost = parseFloat(calculatorContainer.querySelector('#salt-pod-cost').value) || 0;
            const usesPerDay = parseFloat(calculatorContainer.querySelector('#uses-per-day').value) || 0;
            const saltPodsPerUse = parseFloat(calculatorContainer.querySelector('#salt-pods-per-use').value) || 1;

            if (deviceCost > 0 && saltPodCost > 0 && usesPerDay > 0) {
                const dailyCost = (saltPodCost * saltPodsPerUse * usesPerDay);
                const monthlyCost = dailyCost * 30;
                const yearlyCost = dailyCost * 365;
                const costPerUse = saltPodCost * saltPodsPerUse;

                resultDiv.innerHTML = `
                    <h4>Cost Breakdown:</h4>
                    <div class="cost-breakdown">
                        <div class="cost-item">
                            <span>Cost per use:</span>
                            <span>$${costPerUse.toFixed(2)}</span>
                        </div>
                        <div class="cost-item">
                            <span>Daily cost:</span>
                            <span>$${dailyCost.toFixed(2)}</span>
                        </div>
                        <div class="cost-item">
                            <span>Monthly cost:</span>
                            <span>$${monthlyCost.toFixed(2)}</span>
                        </div>
                        <div class="cost-item">
                            <span>Yearly cost:</span>
                            <span>$${yearlyCost.toFixed(2)}</span>
                        </div>
                    </div>
                `;
                resultDiv.style.display = 'block';
            } else {
                resultDiv.innerHTML = '<p>Please fill in all required fields.</p>';
                resultDiv.style.display = 'block';
            }
        });
    }
}

// Product comparison functionality
function initializeProductComparison() {
    const comparisonTable = document.querySelector('.comparison-table');
    if (!comparisonTable) return;

    // Add click handlers for comparison checkboxes
    const checkboxes = comparisonTable.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            updateComparisonDisplay();
        });
    });
}

function updateComparisonDisplay() {
    const selectedProducts = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
        .map(cb => cb.value);
    
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        const productName = card.querySelector('h3').textContent.toLowerCase();
        const isSelected = selectedProducts.some(selected => 
            productName.includes(selected.toLowerCase())
        );
        
        if (selectedProducts.length > 0) {
            card.style.display = isSelected ? 'block' : 'none';
        } else {
            card.style.display = 'block';
        }
    });
}

// Search functionality
function initializeSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchResults = document.querySelector('.search-results');
    
    if (searchInput && searchResults) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            
            if (query.length < 2) {
                searchResults.style.display = 'none';
                return;
            }
            
            // Simple search through product cards
            const productCards = document.querySelectorAll('.product-card, .article-card');
            const matches = Array.from(productCards).filter(card => {
                const text = card.textContent.toLowerCase();
                return text.includes(query);
            });
            
            if (matches.length > 0) {
                searchResults.innerHTML = matches.map(card => {
                    const title = card.querySelector('h3').textContent;
                    const link = card.querySelector('a')?.href || '#';
                    return `<a href="${link}" class="search-result-item">${title}</a>`;
                }).join('');
                searchResults.style.display = 'block';
            } else {
                searchResults.innerHTML = '<p>No results found.</p>';
                searchResults.style.display = 'block';
            }
        });
    }
}

// Initialize all functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeProductComparison();
    initializeSearch();
});

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .notification-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0;
        line-height: 1;
    }
    
    .cost-breakdown {
        display: grid;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    
    .cost-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .cost-item:last-child {
        border-bottom: none;
        font-weight: bold;
        background: #f3f4f6;
        padding: 0.75rem;
        border-radius: 4px;
    }
    
    .search-results {
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        z-index: 1000;
        max-height: 300px;
        overflow-y: auto;
    }
    
    .search-result-item {
        display: block;
        padding: 0.75rem 1rem;
        color: #374151;
        text-decoration: none;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .search-result-item:hover {
        background: #f9fafb;
    }
    
    .search-result-item:last-child {
        border-bottom: none;
    }
`;
document.head.appendChild(style);
