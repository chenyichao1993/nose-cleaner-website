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
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value.trim();
            
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
            } else {
                showNotification('Please enter your email address.', 'error');
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
            const usesPerDay = parseFloat(calculatorContainer.querySelector('#uses-per-day').value) || 0;
            const saltPodsPerUse = parseFloat(calculatorContainer.querySelector('#salt-pods-per-use').value) || 1;

            if (usesPerDay > 0) {
                // Fixed costs per salt pod
                const navagePodCost = 0.50; // $0.50 per Naväge salt pod
                const neilmedPodCost = 0.15; // $0.15 per NeilMed saline packet
                
                // Calculate costs
                const navageCostPerUse = navagePodCost * saltPodsPerUse;
                const neilmedCostPerUse = neilmedPodCost * saltPodsPerUse;
                
                const navageDailyCost = navageCostPerUse * usesPerDay;
                const neilmedDailyCost = neilmedCostPerUse * usesPerDay;
                
                const navageMonthlyCost = navageDailyCost * 30;
                const neilmedMonthlyCost = neilmedDailyCost * 30;
                
                const navageYearlyCost = navageDailyCost * 365;
                const neilmedYearlyCost = neilmedDailyCost * 365;
                
                const yearlySavings = navageYearlyCost - neilmedYearlyCost;
                const recommendedProduct = yearlySavings > 0 ? 'NeilMed' : 'Naväge';
                const savingsAmount = Math.abs(yearlySavings);

                resultDiv.innerHTML = `
                    <div class="cost-comparison">
                        <h4>Annual Cost Comparison</h4>
                        <div class="comparison-cards">
                            <div class="cost-card navage-card">
                                <h5>Naväge</h5>
                                <div class="cost-breakdown">
                                    <div class="cost-item">
                                        <span>Per use:</span>
                                        <span>$${navageCostPerUse.toFixed(2)}</span>
                                    </div>
                                    <div class="cost-item">
                                        <span>Monthly:</span>
                                        <span>$${navageMonthlyCost.toFixed(2)}</span>
                                    </div>
                                    <div class="cost-item total">
                                        <span>Yearly:</span>
                                        <span>$${navageYearlyCost.toFixed(2)}</span>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="cost-card neilmed-card">
                                <h5>NeilMed</h5>
                                <div class="cost-breakdown">
                                    <div class="cost-item">
                                        <span>Per use:</span>
                                        <span>$${neilmedCostPerUse.toFixed(2)}</span>
                                    </div>
                                    <div class="cost-item">
                                        <span>Monthly:</span>
                                        <span>$${neilmedMonthlyCost.toFixed(2)}</span>
                                    </div>
                                    <div class="cost-item total">
                                        <span>Yearly:</span>
                                        <span>$${neilmedYearlyCost.toFixed(2)}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="recommendation">
                            <h5>💡 Recommendation</h5>
                            <p><strong>${recommendedProduct}</strong> would save you <strong>$${savingsAmount.toFixed(2)}</strong> per year with your usage pattern.</p>
                        </div>
                    </div>
                `;
                resultDiv.style.display = 'block';
            } else {
                resultDiv.innerHTML = '<p class="error-message">Please enter a valid number of uses per day.</p>';
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
    
    .cost-comparison {
        margin-top: 2rem;
        padding: 1.5rem;
        background: #f8fafc;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }
    
    .comparison-cards {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .cost-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 2px solid transparent;
    }
    
    .navage-card {
        border-color: #3b82f6;
    }
    
    .neilmed-card {
        border-color: #10b981;
    }
    
    .cost-card h5 {
        margin: 0 0 1rem 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .navage-card h5 {
        color: #3b82f6;
    }
    
    .neilmed-card h5 {
        color: #10b981;
    }
    
    .cost-breakdown {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    
    .cost-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .cost-item.total {
        border-bottom: none;
        font-weight: bold;
        background: #f8fafc;
        padding: 0.75rem;
        border-radius: 6px;
        margin-top: 0.5rem;
    }
    
    .recommendation {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        margin-top: 1.5rem;
    }
    
    .recommendation h5 {
        margin: 0 0 0.5rem 0;
        font-size: 1.1rem;
    }
    
    .recommendation p {
        margin: 0;
        font-size: 1rem;
    }
    
    .error-message {
        color: #ef4444;
        text-align: center;
        padding: 1rem;
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 8px;
    }
    
    @media (max-width: 768px) {
        .comparison-cards {
            grid-template-columns: 1fr;
            gap: 1rem;
        }
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
