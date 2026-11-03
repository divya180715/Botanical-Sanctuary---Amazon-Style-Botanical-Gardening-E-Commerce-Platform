/**
 * VERDANT BOTANICS - AMAZON-STYLE CLIENT CONTROLLER
 * Handles:
 * - Live product rendering from API
 * - Real-time client & server filtering by category, search query, and sorting
 * - Persistent Cart state via LocalStorage
 * - Quick-view product modal with thumbnail switching & plant care specs
 * - Amazon-style fly-in Cart Drawer with item adjustments
 * - Frictionless 1-click & modal Checkout flow (No login needed)
 * - Auto-sliding botanical hero banners
 * - Visual feedback / Toast alerts
 */

let allProducts = [];
let currentCategory = 'all';
let currentSort = 'featured';
let searchQuery = '';
let cart = JSON.parse(localStorage.getItem('verdant_cart')) || [];
let activeHeroSlide = 0;
let heroInterval;

// HERO SLIDES DATA (High resolution botanical Unsplash free images)
const HERO_SLIDES = [
    {
        title: "Breathe Fresh. Live Green.",
        subtitle: "Handpicked Indoor Plants, Exotic Succulents & NASA-Approved Air Purifiers delivered safe to your doorstep.",
        badge: "Spring Planting Festival",
        image: "https://images.unsplash.com/photo-1545241047-6083a3684587?auto=format&fit=crop&w=1600&q=80",
        ctaText: "Shop Live Plants",
        category: "plants"
    },
    {
        title: "Heirloom Seeds & Flower Gardens",
        subtitle: "High-germination pollinator seed mixes, organic culinary herbs, and rare Japanese Bonsai starter kits.",
        badge: "Gardener's Choice 2026",
        image: "https://images.unsplash.com/photo-1490750967868-88aa4486c946?auto=format&fit=crop&w=1600&q=80",
        ctaText: "Explore Seeds",
        category: "seeds"
    },
    {
        title: "Nordic Pots & Living Room Botanical Art",
        subtitle: "Glazed ceramic planters with bamboo saucers, geometric glass terrariums & wall living moss frames.",
        badge: "New Home Decor Arrivals",
        image: "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=1600&q=80",
        ctaText: "Discover Pots & Decor",
        category: "pots"
    }
];

// INITIALIZATION
document.addEventListener('DOMContentLoaded', () => {
    initHeroCarousel();
    updateCartBadge();
    fetchProducts();
    setupEventListeners();
});

// HERO CAROUSEL LOGIC
function initHeroCarousel() {
    const container = document.getElementById('heroSlides');
    if (!container) return;

    container.innerHTML = HERO_SLIDES.map((slide, idx) => `
        <div class="hero-slide ${idx === 0 ? 'active' : ''}" style="background-image: url('${slide.image}');">
            <div class="hero-overlay">
                <div class="hero-content">
                    <span class="hero-badge"><i class="fas fa-leaf"></i> ${slide.badge}</span>
                    <h1 class="hero-title">${slide.title}</h1>
                    <p class="hero-description">${slide.subtitle}</p>
                    <a href="#products-section" class="hero-cta" onclick="filterByCategory('${slide.category}')">
                        ${slide.ctaText} <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            </div>
        </div>
    `).join('');

    heroInterval = setInterval(nextHeroSlide, 6000);
}

function nextHeroSlide() {
    const slides = document.querySelectorAll('.hero-slide');
    if (!slides.length) return;
    slides[activeHeroSlide].classList.remove('active');
    activeHeroSlide = (activeHeroSlide + 1) % slides.length;
    slides[activeHeroSlide].classList.add('active');
}

function prevHeroSlide() {
    const slides = document.querySelectorAll('.hero-slide');
    if (!slides.length) return;
    slides[activeHeroSlide].classList.remove('active');
    activeHeroSlide = (activeHeroSlide - 1 + slides.length) % slides.length;
    slides[activeHeroSlide].classList.add('active');
}

// FETCH PRODUCTS FROM FLASK API
async function fetchProducts() {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;

    grid.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 60px 0; color: #565959;">
            <i class="fas fa-spinner fa-spin fa-2x" style="color: #2e7d32; margin-bottom: 12px;"></i>
            <p>Loading fresh botanical collections...</p>
        </div>
    `;

    try {
        const queryParams = new URLSearchParams({
            category: currentCategory,
            q: searchQuery,
            sort: currentSort
        });

        const response = await fetch(`/api/products?${queryParams.toString()}`);
        const data = await response.json();

        if (data.status === 'success') {
            allProducts = data.products;
            renderProducts(allProducts);
            document.getElementById('resultsCount').innerText = `${data.total} botanical items available`;
        } else {
            grid.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 40px;">Failed to load products.</div>`;
        }
    } catch (err) {
        console.error('API Fetch Error:', err);
        grid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: #b12704;">
                <p>Could not connect to product database. Refreshing...</p>
            </div>
        `;
    }
}

// INDIAN RUPEE FORMATTER
function formatINR(val) {
    if (val === undefined || val === null) return '0';
    return Number(val).toLocaleString('en-IN');
}

// RENDER PRODUCTS IN AMAZON STYLE CARD
function renderProducts(products) {
    const grid = document.getElementById('productsGrid');
    if (!grid) return;

    if (!products.length) {
        grid.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 60px 20px; background: #fff; border-radius: 8px;">
                <i class="fas fa-seedling" style="font-size: 3rem; color: #86efac; margin-bottom: 12px;"></i>
                <h3 style="font-size: 1.2rem; color: #0f1111; margin-bottom: 6px;">No botanical items match your query</h3>
                <p style="color: #565959; font-size: 0.9rem; margin-bottom: 16px;">Try searching for "flower pot", "monstera", "seeds", "pruner", or click below to view all items.</p>
                <button class="filter-pill" style="margin: 0 auto;" onclick="resetFilters()">Reset All Filters</button>
            </div>
        `;
        return;
    }

    grid.innerHTML = products.map(product => {
        const badgeClass = getBadgeClass(product.badge);

        return `
            <div class="product-card" data-id="${product.id}">
                ${product.badge ? `<span class="badge-flag ${badgeClass}">${product.badge === "Amazon's Choice" ? 'Verdant\'s <span>Choice</span>' : product.badge}</span>` : ''}
                
                <div class="product-img-wrapper" onclick="openQuickView('${product.id}')">
                    <img src="${product.image}?v=2" alt="${product.name}" class="product-img" loading="lazy" onerror="this.onerror=null; this.src='https://images.unsplash.com/photo-1614594975525-e45190c55d0b?auto=format&fit=crop&w=800&q=80';">
                    <button class="product-quick-view-btn" onclick="event.stopPropagation(); openQuickView('${product.id}')">
                        <i class="fas fa-eye"></i> Quick Details
                    </button>
                </div>

                <div class="product-meta-category">${product.category_label}</div>
                
                <h3 class="product-name" onclick="openQuickView('${product.id}')" title="${product.name}">
                    ${product.name}
                </h3>

                <div class="product-rating">
                    <div class="stars">${renderStars(product.rating)}</div>
                    <span class="rating-score">${product.rating}</span>
                    <span class="reviews-count">(${product.reviews_count.toLocaleString()})</span>
                </div>

                <div class="product-pricing">
                    <span class="price-currency">₹</span>
                    <span class="price-amount">${formatINR(product.price)}</span>
                    ${product.original_price ? `<span class="original-price">₹${formatINR(product.original_price)}</span>` : ''}
                    ${product.original_price ? `<span class="discount-tag">Save ${Math.round(((product.original_price - product.price)/product.original_price)*100)}%</span>` : ''}
                </div>

                <div class="prime-delivery-badge">
                    <span class="prime-pill"><i class="fas fa-check" style="color: #4ade80;"></i> VerdantExpress</span>
                    <span>FREE Delivery across India</span>
                </div>

                <div class="stock-status">
                    <i class="fas fa-check-circle"></i> In Stock. Ships in plant-safe boxes.
                </div>

                <div class="card-btn-group">
                    <button class="btn-add-cart" onclick="addToCart('${product.id}')">
                        <i class="fas fa-cart-plus"></i> Add to Cart
                    </button>
                    <button class="btn-buy-now" onclick="quickBuyNow('${product.id}')">
                        Buy Now
                    </button>
                </div>
            </div>
        `;
    }).join('');
}

function getBadgeClass(badge) {
    if (!badge) return '';
    const b = badge.toLowerCase();
    if (b.includes('seller')) return 'best-seller';
    if (b.includes('choice')) return 'amazon-choice';
    if (b.includes('deal')) return 'deal';
    return 'eco';
}

function renderStars(rating) {
    let html = '';
    const full = Math.floor(rating);
    const half = rating % 1 >= 0.4;
    for (let i = 0; i < full; i++) html += '<i class="fas fa-star"></i>';
    if (half) html += '<i class="fas fa-star-half-alt"></i>';
    const empty = 5 - full - (half ? 1 : 0);
    for (let i = 0; i < empty; i++) html += '<i class="far fa-star"></i>';
    return html;
}

// FILTER & SEARCH HANDLERS
function filterByCategory(catId) {
    currentCategory = catId;
    document.querySelectorAll('.filter-pill').forEach(pill => {
        pill.classList.toggle('active', pill.dataset.category === catId);
    });

    const categorySelect = document.getElementById('searchCategorySelect');
    if (categorySelect) categorySelect.value = catId;

    fetchProducts();
}

function handleSearch(e) {
    if (e) e.preventDefault();
    const input = document.getElementById('searchInput');
    searchQuery = input ? input.value.trim() : '';

    const categorySelect = document.getElementById('searchCategorySelect');
    if (categorySelect) {
        currentCategory = categorySelect.value;
        document.querySelectorAll('.filter-pill').forEach(pill => {
            pill.classList.toggle('active', pill.dataset.category === currentCategory);
        });
    }

    // Scroll smoothly to products section if searching from header
    const section = document.getElementById('products-section');
    if (section && window.scrollY < section.offsetTop - 120) {
        section.scrollIntoView({ behavior: 'smooth' });
    }

    fetchProducts();
}

function handleSortChange(sortVal) {
    currentSort = sortVal;
    fetchProducts();
}

function resetFilters() {
    currentCategory = 'all';
    searchQuery = '';
    currentSort = 'featured';
    const input = document.getElementById('searchInput');
    if (input) input.value = '';
    const categorySelect = document.getElementById('searchCategorySelect');
    if (categorySelect) categorySelect.value = 'all';
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) sortSelect.value = 'featured';
    filterByCategory('all');
}

// QUICK VIEW MODAL
async function openQuickView(productId) {
    const modal = document.getElementById('productModal');
    const content = document.getElementById('modalContent');
    if (!modal || !content) return;

    modal.classList.add('open');
    content.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 40px;">
            <i class="fas fa-spinner fa-spin fa-2x" style="color: #2e7d32;"></i>
        </div>
    `;

    try {
        const response = await fetch(`/api/products/${productId}`);
        const data = await response.json();

        if (data.status === 'success') {
            const p = data.product;
            const images = [p.image, ...(p.secondary_images || [])];

            content.innerHTML = `
                <div>
                    <img id="quickViewMainImg" src="${p.image}" alt="${p.name}" class="modal-gallery-main">
                    <div class="modal-thumbnails">
                        ${images.map((img, i) => `
                            <img src="${img}" class="modal-thumb ${i === 0 ? 'active' : ''}" onclick="switchModalThumb(this, '${img}')" alt="preview">
                        `).join('')}
                    </div>
                </div>

                <div class="modal-details">
                    <div class="product-meta-category">${p.category_label}</div>
                    <h2 style="font-size: 1.35rem; font-weight: 700; color: #0f1111; margin-bottom: 8px;">${p.name}</h2>
                    
                    <div class="product-rating" style="margin-bottom: 12px;">
                        <div class="stars">${renderStars(p.rating)}</div>
                        <span class="rating-score">${p.rating} / 5</span>
                        <span class="reviews-count">(${p.reviews_count} customer reviews)</span>
                    </div>

                    <div class="product-pricing" style="margin-bottom: 12px;">
                        <span class="price-currency">₹</span>
                        <span class="price-amount">${formatINR(p.price)}</span>
                        ${p.original_price ? `<span class="original-price">₹${formatINR(p.original_price)}</span>` : ''}
                        ${p.original_price ? `<span class="discount-tag" style="margin-left: 8px;">Save ${Math.round(((p.original_price - p.price)/p.original_price)*100)}%</span>` : ''}
                    </div>

                    <p style="font-size: 0.88rem; color: #333; line-height: 1.5; margin-bottom: 14px;">${p.description}</p>

                    ${p.care ? `
                        <div class="modal-plant-care">
                            <strong style="display: block; margin-bottom: 6px; color: #1b5e20;">
                                <i class="fas fa-heartbeat"></i> Botanical Care Guidelines:
                            </strong>
                            <div class="care-row"><i class="fas fa-sun"></i> <span><strong>Sunlight:</strong> ${p.care.light}</span></div>
                            <div class="care-row"><i class="fas fa-tint"></i> <span><strong>Water:</strong> ${p.care.water}</span></div>
                            <div class="care-row"><i class="fas fa-wind"></i> <span><strong>Humidity:</strong> ${p.care.humidity}</span></div>
                        </div>
                    ` : ''}

                    <ul style="font-size: 0.83rem; color: #555; margin-bottom: 18px; padding-left: 18px;">
                        ${p.features.map(f => `<li style="margin-bottom: 4px;">${f}</li>`).join('')}
                    </ul>

                    <div style="margin-top: auto; display: flex; gap: 10px;">
                        <button class="btn-add-cart" style="flex: 1;" onclick="addToCart('${p.id}'); closeModal();">
                            <i class="fas fa-cart-plus"></i> Add to Cart
                        </button>
                        <button class="btn-buy-now" style="flex: 1;" onclick="quickBuyNow('${p.id}'); closeModal();">
                            Proceed to Buy
                        </button>
                    </div>
                </div>
            `;
        }
    } catch (err) {
        console.error(err);
        closeModal();
    }
}

function switchModalThumb(el, src) {
    document.querySelectorAll('.modal-thumb').forEach(t => t.classList.remove('active'));
    el.classList.add('active');
    document.getElementById('quickViewMainImg').src = src;
}

function closeModal() {
    const modal = document.getElementById('productModal');
    if (modal) modal.classList.remove('open');
}

// CART MANAGEMENT
function addToCart(productId) {
    const product = allProducts.find(p => p.id === productId);
    if (!product) return;

    const existing = cart.find(item => item.id === productId);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            image: product.image,
            category_label: product.category_label,
            quantity: 1
        });
    }

    saveCart();
    updateCartBadge();
    showToast(`Added "${product.name}" to your cart!`);
    openCartDrawer();
}

function updateCartQuantity(productId, delta) {
    const item = cart.find(i => i.id === productId);
    if (!item) return;

    item.quantity += delta;
    if (item.quantity <= 0) {
        cart = cart.filter(i => i.id !== productId);
    }

    saveCart();
    updateCartBadge();
    renderCartDrawer();
}

function removeFromCart(productId) {
    cart = cart.filter(i => i.id !== productId);
    saveCart();
    updateCartBadge();
    renderCartDrawer();
    showToast("Item removed from cart");
}

function saveCart() {
    localStorage.setItem('verdant_cart', JSON.stringify(cart));
}

function updateCartBadge() {
    const totalQty = cart.reduce((sum, item) => sum + item.quantity, 0);
    const badge = document.getElementById('cartCount');
    if (badge) badge.innerText = totalQty;
}

// CART DRAWER (SIDEBAR)
function openCartDrawer() {
    const drawer = document.getElementById('cartDrawer');
    const overlay = document.getElementById('cartDrawerOverlay');
    if (drawer && overlay) {
        renderCartDrawer();
        drawer.classList.add('open');
        overlay.classList.add('open');
    }
}

function closeCartDrawer() {
    const drawer = document.getElementById('cartDrawer');
    const overlay = document.getElementById('cartDrawerOverlay');
    if (drawer && overlay) {
        drawer.classList.remove('open');
        overlay.classList.remove('open');
    }
}

function renderCartDrawer() {
    const container = document.getElementById('cartItemsList');
    const subtotalEl = document.getElementById('cartSubtotalAmount');
    if (!container) return;

    if (!cart.length) {
        container.innerHTML = `
            <div class="cart-empty-state">
                <i class="fas fa-shopping-basket"></i>
                <h4 style="font-size: 1.1rem; color: #111; margin-bottom: 6px;">Your Botanical Cart is Empty</h4>
                <p style="font-size: 0.85rem;">Discover live plants, seeds, terracotta pots, and gardening tools ready to ship.</p>
            </div>
        `;
        if (subtotalEl) subtotalEl.innerText = '₹0';
        return;
    }

    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    if (subtotalEl) subtotalEl.innerText = `₹${formatINR(subtotal)}`;

    container.innerHTML = cart.map(item => `
        <div class="cart-item">
            <img src="${item.image}" alt="${item.name}" class="cart-item-img">
            <div class="cart-item-info">
                <div class="cart-item-title">${item.name}</div>
                <div class="cart-item-price">₹${formatINR(item.price * item.quantity)}</div>
                <div class="cart-item-qty-row">
                    <div class="qty-control">
                        <button class="qty-btn" onclick="updateCartQuantity('${item.id}', -1)">-</button>
                        <span class="qty-value">${item.quantity}</span>
                        <button class="qty-btn" onclick="updateCartQuantity('${item.id}', 1)">+</button>
                    </div>
                    <button class="remove-item-btn" onclick="removeFromCart('${item.id}')">Delete</button>
                </div>
            </div>
        </div>
    `).join('');
}

// CHECKOUT (INSTANT WITHOUT AUTHENTICATION REQUIRED)
function openCheckoutModal() {
    if (!cart.length) {
        showToast("Your cart is empty! Add botanical items first.");
        return;
    }

    closeCartDrawer();
    const modal = document.getElementById('checkoutModal');
    const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const tax = Math.round(subtotal * 0.05);
    const grandTotal = subtotal + tax;

    const summaryEl = document.getElementById('checkoutOrderSummary');
    if (summaryEl) {
        summaryEl.innerHTML = `
            <div style="background: #f8faf8; border: 1px solid #d5d9d9; border-radius: 6px; padding: 12px; margin-bottom: 14px; font-size: 0.85rem;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span>Items (${cart.reduce((s,i)=>s+i.quantity,0)}):</span>
                    <span>₹${formatINR(subtotal)}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px; color: #007600;">
                    <span>Green Botanical Packaging:</span>
                    <span>FREE</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                    <span>Estimated GST (5%):</span>
                    <span>₹${formatINR(tax)}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-weight: 700; font-size: 1rem; border-top: 1px solid #ddd; padding-top: 6px; color: #b12704;">
                    <span>Order Total:</span>
                    <span>₹${formatINR(grandTotal)}</span>
                </div>
            </div>
        `;
    }

    if (modal) modal.classList.add('open');
}

function closeCheckoutModal() {
    const modal = document.getElementById('checkoutModal');
    if (modal) modal.classList.remove('open');
}

async function handleCheckoutSubmit(e) {
    e.preventDefault();
    const btn = document.getElementById('placeOrderBtn');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Processing Eco Delivery...`;
    }

    const name = document.getElementById('shipName').value;
    const address = document.getElementById('shipAddress').value;
    const city = document.getElementById('shipCity').value;
    const state = document.getElementById('shipState') ? document.getElementById('shipState').value : '';
    const postal = document.getElementById('shipPostal').value;
    const phone = document.getElementById('shipPhone').value;

    const fullAddress = state 
        ? `${address}, ${city}, ${state} - ${postal}`
        : `${address}, ${city} - ${postal}`;

    const payload = {
        items: cart,
        shipping: {
            name,
            address: fullAddress,
            city,
            state,
            postal,
            phone
        }
    };

    try {
        const response = await fetch('/api/checkout', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (data.status === 'success') {
            const bodyEl = document.getElementById('checkoutModalBody');
            bodyEl.innerHTML = `
                <div class="order-success-screen">
                    <div class="success-badge"><i class="fas fa-check"></i></div>
                    <h2 style="font-size: 1.4rem; color: #1b5e20; margin-bottom: 8px;">Order Confirmed!</h2>
                    <p style="font-size: 0.9rem; color: #555; margin-bottom: 12px;">Order ID: <strong>${data.order_id}</strong></p>
                    <div style="background: #f1f8f4; border: 1px solid #c8e6c9; border-radius: 8px; padding: 14px; text-align: left; font-size: 0.85rem; margin-bottom: 20px;">
                        <p><i class="fas fa-truck" style="color: #2e7d32; margin-right: 6px;"></i> <strong>Estimated Arrival:</strong> ${data.delivery_estimate}</p>
                        <p><i class="fas fa-map-marker-alt" style="color: #2e7d32; margin-right: 6px;"></i> <strong>Delivering to:</strong> ${name}, ${data.shipping_address}</p>
                        <p><i class="fas fa-leaf" style="color: #2e7d32; margin-right: 6px;"></i> <strong>Packed in:</strong> 100% Biodegradable & Plant-Safe insulation boxes.</p>
                    </div>
                    <button class="btn-proceed-checkout" onclick="finishCheckout();">
                        Continue Shopping Botanical
                    </button>
                </div>
            `;

            // Reset cart
            cart = [];
            saveCart();
            updateCartBadge();
        }
    } catch (err) {
        console.error(err);
        showToast("Error processing order. Please try again.");
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = `Place Your Botanical Order`;
        }
    }
}

function quickBuyNow(productId) {
    const existing = cart.find(i => i.id === productId);
    if (!existing) {
        addToCart(productId);
    }
    openCheckoutModal();
}

function finishCheckout() {
    closeCheckoutModal();
    window.location.reload();
}

// TOAST NOTIFICATIONS
function showToast(msg) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<i class="fas fa-check-circle"></i> <span>${msg}</span>`;

    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(10px)';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// EVENT LISTENERS
function setupEventListeners() {
    // Search form & input
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', handleSearch);
    }

    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let debounceTimer;
        searchInput.addEventListener('input', (e) => {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {
                handleSearch(e);
            }, 300);
        });
    }

    // Category drop selector
    const catSelect = document.getElementById('searchCategorySelect');
    if (catSelect) {
        catSelect.addEventListener('change', (e) => {
            filterByCategory(e.target.value);
        });
    }

    // Sort selector
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            handleSortChange(e.target.value);
        });
    }

    // Backdrop click close
    window.addEventListener('click', (e) => {
        const modal = document.getElementById('productModal');
        if (e.target === modal) closeModal();

        const checkoutModal = document.getElementById('checkoutModal');
        if (e.target === checkoutModal) closeCheckoutModal();
    });

    // Close on Escape key
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeModal();
            closeCheckoutModal();
            closeCartDrawer();
        }
    });
}
