document.addEventListener('DOMContentLoaded', () => {

  // Mobile nav
  const hamburger = document.querySelector('.hamburger');
  const navLinks = document.querySelector('.nav-links');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      navLinks.classList.toggle('open');
    });
  }

  // Scroll to top
  const scrollBtn = document.getElementById('scrollTop');
  if (scrollBtn) {
    window.addEventListener('scroll', () => {
      scrollBtn.classList.toggle('visible', window.scrollY > 300);
    });
    scrollBtn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }

  // Auto-dismiss alerts
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      alert.style.transition = 'all 0.5s ease';
      setTimeout(() => alert.remove(), 500);
    }, 5000);
  });

  // Cart quantity update
  document.querySelectorAll('.cart-qty-input').forEach(input => {
    input.addEventListener('change', function() {
      const form = this.closest('form');
      if (form) form.submit();
    });
  });

  // Product image zoom
  const detailImg = document.querySelector('.detail-image img');
  if (detailImg) {
    detailImg.addEventListener('mouseenter', () => {
      detailImg.style.transform = 'scale(1.03)';
      detailImg.style.transition = 'transform 0.5s ease';
    });
    detailImg.addEventListener('mouseleave', () => {
      detailImg.style.transform = 'scale(1)';
    });
  }

  // Checkout payment toggle
  const cardDetails = document.getElementById('cardDetails');
  const upiDetails = document.getElementById('upiDetails');
  document.querySelectorAll('input[name="payment_method"]').forEach(radio => {
    radio.addEventListener('change', function() {
      if (cardDetails) cardDetails.style.display = this.value === 'card' ? 'block' : 'none';
      if (upiDetails) upiDetails.style.display = ['gpay','phonepe','upi'].includes(this.value) ? 'block' : 'none';
    });
  });

  // Form validation
  const checkoutForm = document.getElementById('checkoutForm');
  if (checkoutForm) {
    checkoutForm.addEventListener('submit', function(e) {
      const required = this.querySelectorAll('[required]');
      let valid = true;
      required.forEach(field => {
        if (!field.value.trim()) {
          field.style.borderColor = '#e74c3c';
          valid = false;
        } else {
          field.style.borderColor = '';
        }
      });
      if (!valid) {
        e.preventDefault();
        showToast('Please fill in all required fields.', 'error');
      }
    });
  }

  // Search autocomplete hint
  const searchInput = document.querySelector('.search-input');
  if (searchInput) {
    searchInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        this.closest('form').submit();
      }
    });
  }

  // Animate cards on scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.product-card, .category-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
  });

  // Toast notification
  window.showToast = function(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type === 'error' ? 'danger' : type}`;
    toast.style.cssText = 'position:fixed;top:20px;right:20px;z-index:9999;min-width:300px;animation:slideIn 0.3s ease';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  };

  // Active nav link
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });

});

// CSS animation for toast
const style = document.createElement('style');
style.textContent = '@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }';
document.head.appendChild(style);
