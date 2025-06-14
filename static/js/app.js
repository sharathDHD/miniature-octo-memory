// Main JavaScript for Fan Fiction Novel Generator

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Add loading state to form submissions
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            var submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
                
                // Re-enable after 30 seconds as fallback
                setTimeout(function() {
                    submitBtn.classList.remove('loading');
                    submitBtn.disabled = false;
                }, 30000);
            }
        });
    });

    // Smooth scrolling for anchor links
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add animation to cards on scroll
    var observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    var cards = document.querySelectorAll('.card');
    cards.forEach(function(card) {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(card);
    });

    // Character counter for textareas
    var textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        var maxLength = textarea.getAttribute('maxlength');
        if (maxLength) {
            var counter = document.createElement('div');
            counter.className = 'form-text text-end';
            counter.innerHTML = '<span class="current">0</span>/<span class="max">' + maxLength + '</span> characters';
            textarea.parentNode.appendChild(counter);

            textarea.addEventListener('input', function() {
                var current = this.value.length;
                counter.querySelector('.current').textContent = current;
                
                if (current > maxLength * 0.9) {
                    counter.classList.add('text-warning');
                } else {
                    counter.classList.remove('text-warning');
                }
            });
        }
    });

    // Enhanced search functionality (if search input exists)
    var searchInput = document.querySelector('#search-input');
    if (searchInput) {
        var searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(function() {
                performSearch(searchInput.value);
            }, 300);
        });
    }

    // Copy to clipboard functionality
    var copyButtons = document.querySelectorAll('[data-copy]');
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var textToCopy = this.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(function() {
                showToast('Copied to clipboard!', 'success');
            }).catch(function() {
                showToast('Failed to copy to clipboard', 'error');
            });
        });
    });

    // Theme toggle (if implemented)
    var themeToggle = document.querySelector('#theme-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-theme');
            localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
        });

        // Load saved theme
        var savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            document.body.classList.add('dark-theme');
        }
    }
});

// Utility functions
function showToast(message, type = 'info') {
    var toast = document.createElement('div');
    toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    toast.style.top = '20px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    toast.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(function() {
        toast.remove();
    }, 5000);
}

function performSearch(query) {
    // This would be implemented based on your search requirements
    console.log('Searching for:', query);
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

// API helper functions
async function fetchStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching stats:', error);
        return null;
    }
}

// Export functions for use in other scripts
window.NovelGenerator = {
    showToast: showToast,
    formatNumber: formatNumber,
    truncateText: truncateText,
    fetchStats: fetchStats
};