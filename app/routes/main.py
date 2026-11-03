import os
import json
import random
from flask import Blueprint, render_template, jsonify, request

bp = Blueprint('main', __name__)

# Curated catalog of botanical products covering all requested categories:
# 1. Plants (Indoor, Outdoor, Succulents, Air-purifying)
# 2. Seeds (Flowers, Vegetables, Organic Herbs, Bonsai)
# 3. Flower Pots & Planters (Ceramic, Terracotta, Hanging, Geometric)
# 4. Home Decorative Things with Plants (Terrariums, Plant stands, Hydroponic vases, Wall frames)
# 5. Flower Gardening Things (Pruning tools, Watering cans, Organic fertilizers, Moisture meters)

PRODUCTS = [
    {
        "id": "p-101",
        "name": "Monstera Deliciosa (Swiss Cheese Plant)",
        "category": "plants",
        "category_label": "Live Plants",
        "price": 899,
        "original_price": 1299,
        "rating": 4.8,
        "reviews_count": 1420,
        "badge": "Best Seller",
        "in_stock": True,
        "description": "Iconic split-leaf tropical plant that brings lush green vibrancy to any living room or indoor sanctuary.",
        "features": [
            "Low to medium maintenance",
            "Purifies indoor air",
            "Includes 6-inch nursery pot",
            "Pet-safe alert: toxic if ingested"
        ],
        "care": {
            "light": "Bright, indirect light",
            "water": "Once every 1-2 weeks",
            "humidity": "High (60%+)"
        },
        "image": "/static/images/products/p-101.jpg",
        "secondary_images": [
            "/static/images/products/p-101.jpg"
        ]
    },
    {
        "id": "p-102",
        "name": "Snake Plant Sansevieria (Mother-in-Law's Tongue)",
        "category": "plants",
        "category_label": "Live Plants",
        "price": 499,
        "original_price": 749,
        "rating": 4.9,
        "reviews_count": 2180,
        "badge": "Amazon's Choice",
        "in_stock": True,
        "description": "Virtually indestructible architectural plant known for releasing oxygen at night and purifying airborne toxins.",
        "features": [
            "Thrives on neglect",
            "Tolerates low light and drought",
            "Deep green with golden yellow margins",
            "NASA-tested air purifier"
        ],
        "care": {
            "light": "Low to direct sunlight",
            "water": "Every 2-3 weeks",
            "humidity": "Any level"
        },
        "image": "/static/images/products/p-102.jpg",
        "secondary_images": [
            "/static/images/products/p-102.jpg"
        ]
    },
    {
        "id": "p-103",
        "name": "Fiddle Leaf Fig (Ficus Lyrata)",
        "category": "plants",
        "category_label": "Live Plants",
        "price": 1499,
        "original_price": 1999,
        "rating": 4.6,
        "reviews_count": 860,
        "badge": "Trending",
        "in_stock": True,
        "description": "Statement indoor tree featuring violin-shaped leathery leaves that elevate modern interior spaces.",
        "features": [
            "Stunning focal point",
            "Grows up to 6-10 ft indoors",
            "Potting mix enriched with bio-char",
            "Hand-selected by horticulturists"
        ],
        "care": {
            "light": "Generous indirect sunlight",
            "water": "When top 2 inches feel dry",
            "humidity": "Moderate to high"
        },
        "image": "/static/images/products/p-103.jpg",
        "secondary_images": [
            "/static/images/products/p-103.jpg"
        ]
    },
    {
        "id": "p-104",
        "name": "Peace Lily 'Sensation' (White Bloom Spathiphyllum)",
        "category": "plants",
        "category_label": "Live Plants",
        "price": 549,
        "original_price": 799,
        "rating": 4.7,
        "reviews_count": 940,
        "badge": "Eco Choice",
        "in_stock": True,
        "description": "Glossy emerald foliage crowned with graceful white blooms. Acts as a visual barometer drooping when thirsty.",
        "features": [
            "Elegant recurrent white flowers",
            "Excellent pollutant scrubber",
            "Pre-potted with slow-release fertilizer",
            "Easy to revive"
        ],
        "care": {
            "light": "Medium to low shade",
            "water": "Weekly or when soil feels dry",
            "humidity": "Medium"
        },
        "image": "/static/images/products/p-104.jpg",
        "secondary_images": [
            "/static/images/products/p-104.jpg"
        ]
    },
    {
        "id": "p-105",
        "name": "Assorted Rare Rosette Succulents (Pack of 6)",
        "category": "plants",
        "category_label": "Live Plants",
        "price": 699,
        "original_price": 999,
        "rating": 4.8,
        "reviews_count": 1650,
        "badge": "Deal of the Day",
        "in_stock": True,
        "description": "Hand-picked collection of 6 unique rosette succulents in starter pots ready for creative window arrangements.",
        "features": [
            "6 distinct species",
            "Drought resistant",
            "Ideal for desks and windowsill displays",
            "Comes with species identification card"
        ],
        "care": {
            "light": "Bright sunny window",
            "water": "Every 2 weeks sparingly",
            "humidity": "Low / Dry"
        },
        "image": "/static/images/products/p-105.jpg",
        "secondary_images": [
            "/static/images/products/p-105.jpg"
        ]
    },
    {
        "id": "p-106",
        "name": "Golden Pothos Money Vine (Epipremnum Aureum)",
        "category": "plants",
        "category_label": "Live Plants",
        "price": 349,
        "original_price": 499,
        "rating": 4.9,
        "reviews_count": 2890,
        "badge": "Best Seller",
        "in_stock": True,
        "description": "Lucky and air-cleansing vining plant with lush variegated green and yellow heart-shaped leaves that can trail or climb.",
        "features": [
            "Symbol of prosperity and positive energy",
            "Super resilient and fast growing",
            "Grows in water or soil",
            "Includes hanging nursery basket"
        ],
        "care": {
            "light": "Low to bright indirect light",
            "water": "Once every 7-10 days",
            "humidity": "Moderate"
        },
        "image": "/static/images/products/p-106.jpg",
        "secondary_images": [
            "/static/images/products/p-106.jpg"
        ]
    },
    {
        "id": "p-107",
        "name": "ZZ Plant (Zamioculcas Zamiifolia Emerald)",
        "category": "plants",
        "category_label": "Live Plants",
        "price": 649,
        "original_price": 899,
        "rating": 4.8,
        "reviews_count": 1340,
        "badge": "Amazon's Choice",
        "in_stock": True,
        "description": "Ultra-glossy feather-like compound leaves that thrive in dark interior corners and low-humidity office spaces.",
        "features": [
            "Water-storing rhizomes resist drought",
            "Tolerates fluorescent office lighting",
            "Sleek architectural look",
            "Pest resistant"
        ],
        "care": {
            "light": "Low to medium indirect light",
            "water": "Every 3 weeks",
            "humidity": "Low to average"
        },
        "image": "/static/images/products/p-107.jpg",
        "secondary_images": [
            "/static/images/products/p-107.jpg"
        ]
    },
    {
        "id": "p-108",
        "name": "Areca Palm Natural Air Purifier (Chrysalidocarpus)",
        "category": "plants",
        "category_label": "Live Plants",
        "price": 799,
        "original_price": 1199,
        "rating": 4.7,
        "reviews_count": 1120,
        "badge": "Popular",
        "in_stock": True,
        "description": "Graceful feathery fronds that bring a relaxing tropical resort atmosphere to living rooms and balconies.",
        "features": [
            "Natural room humidifier",
            "Removes airborne xylene and toluene",
            "Safe for pets and kids",
            "Height: 2.5 to 3 feet"
        ],
        "care": {
            "light": "Bright filtered sunlight",
            "water": "Twice weekly",
            "humidity": "High"
        },
        "image": "/static/images/products/p-108.jpg",
        "secondary_images": [
            "/static/images/products/p-108.jpg"
        ]
    },
    {
        "id": "s-201",
        "name": "English Cottage Wildflower Seed Mix (50,000 Seeds)",
        "category": "seeds",
        "category_label": "Seeds & Bulbs",
        "price": 399,
        "original_price": 599,
        "rating": 4.9,
        "reviews_count": 3120,
        "badge": "Best Seller",
        "in_stock": True,
        "description": "Non-GMO heirloom pollinator mix containing poppies, cornflowers, cosmos, and daisies designed to attract butterflies and bees.",
        "features": [
            "Coverage up to 1,000 sq ft",
            "100% pure seed with 0 fillers",
            "Germination rate 85%+",
            "Blooms spring through late autumn"
        ],
        "care": {
            "light": "Full Sun",
            "water": "Keep moist until germination",
            "humidity": "Outdoor normal"
        },
        "image": "/static/images/products/s-201.jpg",
        "secondary_images": [
            "/static/images/products/s-201.jpg"
        ]
    },
    {
        "id": "s-202",
        "name": "Japanese Red Maple Bonsai Starter Seed Kit",
        "category": "seeds",
        "category_label": "Seeds & Bulbs",
        "price": 599,
        "original_price": 849,
        "rating": 4.5,
        "reviews_count": 780,
        "badge": "Gift Favorite",
        "in_stock": True,
        "description": "Complete beginner germination kit with Acer Palmatum seeds, peat soil pellets, plant markers, and growing guide.",
        "features": [
            "Authentic Japanese Maple seeds",
            "Includes biodegradable pots",
            "Comprehensive bonsai training pamphlet",
            "High-viability batch"
        ],
        "care": {
            "light": "Partial morning sun",
            "water": "Mist daily",
            "humidity": "Covered mini-greenhouse"
        },
        "image": "/static/images/products/s-202.jpg",
        "secondary_images": [
            "/static/images/products/s-202.jpg"
        ]
    },
    {
        "id": "s-203",
        "name": "Organic Kitchen Herb Vault (12 Heirloom Varieties)",
        "category": "seeds",
        "category_label": "Seeds & Bulbs",
        "price": 449,
        "original_price": 699,
        "rating": 4.8,
        "reviews_count": 1890,
        "badge": "Amazon's Choice",
        "in_stock": True,
        "description": "Basil, Rosemary, Thyme, Oregano, Coriander, Mint, and Parsley in sealed moisture-proof packets for year-round fresh kitchen seasoning.",
        "features": [
            "USDA Certified Organic seeds",
            "Heirloom non-hybrid",
            "Long shelf life seed packets",
            "Suitable for indoor herbs windowsill garden"
        ],
        "care": {
            "light": "Sunny windowsill or grow light",
            "water": "Moist soil",
            "humidity": "Normal"
        },
        "image": "/static/images/products/s-203.jpg",
        "secondary_images": [
            "/static/images/products/s-203.jpg"
        ]
    },
    {
        "id": "s-204",
        "name": "French Lavender 'Vera' Fragrant Flower Seeds",
        "category": "seeds",
        "category_label": "Seeds & Bulbs",
        "price": 299,
        "original_price": 449,
        "rating": 4.7,
        "reviews_count": 640,
        "badge": "Popular",
        "in_stock": True,
        "description": "True English & French hybrid lavender seeds renowned for soothing perfume, insect repellent properties, and vibrant violet spikes.",
        "features": [
            "Perennial aroma plant",
            "Drought tolerant once established",
            "Perfect for tea and potpourri",
            "Attracts honeybees"
        ],
        "care": {
            "light": "Full direct sunlight",
            "water": "Dry out between waterings",
            "humidity": "Dry/Low"
        },
        "image": "/static/images/products/s-204.jpg",
        "secondary_images": [
            "/static/images/products/s-204.jpg"
        ]
    },
    {
        "id": "s-205",
        "name": "Giant Mammoth Golden Sunflower Seeds",
        "category": "seeds",
        "category_label": "Seeds & Bulbs",
        "price": 249,
        "original_price": 399,
        "rating": 4.8,
        "reviews_count": 920,
        "badge": "Trending",
        "in_stock": True,
        "description": "Stunning golden giant sunflowers that reach 10 to 12 feet tall with enormous 14-inch seed heads for pollinators and edible snacking.",
        "features": [
            "Fast 75-day maturity",
            "Produces thousands of edible sunflower seeds",
            "Easy for kids and beginner gardeners",
            "High pollinator magnet"
        ],
        "care": {
            "light": "Direct full sun (6+ hours)",
            "water": "Moderate deep watering",
            "humidity": "Outdoor"
        },
        "image": "/static/images/products/s-205.jpg",
        "secondary_images": [
            "/static/images/products/s-205.jpg"
        ]
    },
    {
        "id": "s-206",
        "name": "Exotic Thai Marigold Golden Blossom Seeds",
        "category": "seeds",
        "category_label": "Seeds & Bulbs",
        "price": 279,
        "original_price": 419,
        "rating": 4.6,
        "reviews_count": 510,
        "badge": "Deal of the Day",
        "in_stock": True,
        "description": "Vibrant festive garland marigold flowers with dense pom-pom blooms in rich orange and gold.",
        "features": [
            "Natural pest repellent for veggie patches",
            "Continuous blooms all season long",
            "90% germination rate batch tested",
            "Easy to grow from seed"
        ],
        "care": {
            "light": "Full sun",
            "water": "Regular morning watering",
            "humidity": "Moderate"
        },
        "image": "/static/images/products/s-206.jpg",
        "secondary_images": [
            "/static/images/products/s-206.jpg"
        ]
    },
    {
        "id": "s-207",
        "name": "Sweet Genovese Italian Basil Culinary Seeds",
        "category": "seeds",
        "category_label": "Seeds & Bulbs",
        "price": 199,
        "original_price": 320,
        "rating": 4.9,
        "reviews_count": 1420,
        "badge": "Top Rated",
        "in_stock": True,
        "description": "Tender fragrant culinary basil seeds ideal for authentic homemade pesto, pasta sauces, and fresh window harvests.",
        "features": [
            "High essential oil yield",
            "Ready to harvest in 4 weeks",
            "Compact container friendly",
            "High germination 92%"
        ],
        "care": {
            "light": "Full morning sun",
            "water": "Keep soil evenly damp",
            "humidity": "Moderate"
        },
        "image": "/static/images/products/s-207.jpg",
        "secondary_images": [
            "/static/images/products/s-207.jpg"
        ]
    },
    {
        "id": "s-208",
        "name": "Rainbow Zinnia Elegans Butterfly Garden Seeds",
        "category": "seeds",
        "category_label": "Seeds & Bulbs",
        "price": 259,
        "original_price": 399,
        "rating": 4.8,
        "reviews_count": 780,
        "badge": "Eco Choice",
        "in_stock": True,
        "description": "Showy multi-colored double-blooming zinnias in shades of magenta, scarlet, coral, and canary yellow.",
        "features": [
            "Heat and drought tolerant",
            "Attracts swallowtails and monarch butterflies",
            "Long vase life cut flower",
            "Bloom from summer to frost"
        ],
        "care": {
            "light": "Warm direct sun",
            "water": "Water base of plant",
            "humidity": "Low to medium"
        },
        "image": "/static/images/products/s-208.jpg",
        "secondary_images": [
            "/static/images/products/s-208.jpg"
        ]
    },
    {
        "id": "pot-301",
        "name": "Nordic Sage Ceramic Planter with Bamboo Saucer (8-inch)",
        "category": "pots",
        "category_label": "Flower Pots & Planters",
        "price": 799,
        "original_price": 1199,
        "rating": 4.9,
        "reviews_count": 2450,
        "badge": "Top Rated",
        "in_stock": True,
        "description": "Minimalist matte sage glazed ceramic pot engineered with drainage hole and organic bamboo water tray to prevent overwatering.",
        "features": [
            "Heavy ceramic pottery",
            "Integrated drainage hole & mesh plug",
            "Natural anti-mildew bamboo saucer",
            "UV-resistant finish"
        ],
        "care": {
            "light": "All environments",
            "water": "Drainage friendly",
            "humidity": "Moisture-sealed"
        },
        "image": "/static/images/products/pot-301.jpg",
        "secondary_images": [
            "/static/images/products/pot-301.jpg"
        ]
    },
    {
        "id": "pot-302",
        "name": "Modern Bohemian Macrame Woven Hanging Planter",
        "category": "pots",
        "category_label": "Flower Pots & Planters",
        "price": 649,
        "original_price": 899,
        "rating": 4.8,
        "reviews_count": 1740,
        "badge": "Amazon's Choice",
        "in_stock": True,
        "description": "Handwoven pure cotton macrame rope plant holder with stainless ceiling hooks, fitting pots 5 to 9 inches.",
        "features": [
            "100% natural cotton rope",
            "Adjustable cradle design",
            "Ceiling hooks & anchors included",
            "Space-saving vertical greening"
        ],
        "care": {
            "light": "Window hangings",
            "water": "Hand washable",
            "humidity": "Indoor use recommended"
        },
        "image": "/static/images/products/pot-302.jpg",
        "secondary_images": [
            "/static/images/products/pot-302.jpg"
        ]
    },
    {
        "id": "pot-303",
        "name": "Artisan Terracotta Ribbed Planter with Drainage",
        "category": "pots",
        "category_label": "Flower Pots & Planters",
        "price": 549,
        "original_price": 799,
        "rating": 4.6,
        "reviews_count": 620,
        "badge": "Handmade",
        "in_stock": True,
        "description": "Breathable porous clay pot promotes healthy root aeration and prevents root rot for aroid plants and succulents.",
        "features": [
            "Porous natural clay pottery",
            "Prevents root rot and soil fungus",
            "Ribbed texture for aesthetic grip",
            "Ages with natural patina"
        ],
        "care": {
            "light": "Indoor or outdoor",
            "water": "Breathes moisture easily",
            "humidity": "All conditions"
        },
        "image": "/static/images/products/pot-303.jpg",
        "secondary_images": [
            "/static/images/products/pot-303.jpg"
        ]
    },
    {
        "id": "pot-304",
        "name": "Self-Watering Reservoir Planter Box System",
        "category": "pots",
        "category_label": "Flower Pots & Planters",
        "price": 999,
        "original_price": 1499,
        "rating": 4.7,
        "reviews_count": 1390,
        "badge": "Smart Garden",
        "in_stock": True,
        "description": "Sub-irrigation system with water level indicator keeps plants perfectly hydrated for up to 14 days unattended.",
        "features": [
            "Deep reservoir wicks water upward",
            "Visual water gauge meter",
            "Food-grade BPA free resin",
            "Ideal for travelers and offices"
        ],
        "care": {
            "light": "All",
            "water": "Refill every 10-14 days",
            "humidity": "Consistent root hydration"
        },
        "image": "/static/images/products/pot-304.jpg",
        "secondary_images": [
            "/static/images/products/pot-304.jpg"
        ]
    },
    {
        "id": "pot-305",
        "name": "Minimalist Matte White Ceramic Pot with Wooden Legs",
        "category": "pots",
        "category_label": "Flower Pots & Planters",
        "price": 1199,
        "original_price": 1699,
        "rating": 4.9,
        "reviews_count": 870,
        "badge": "Trending",
        "in_stock": True,
        "description": "Architectural porcelain cylindrical pot resting on solid beech wood tripod feet for a clean Scandinavian look.",
        "features": [
            "High-fired dense ceramic",
            "Elevated tripod stand promotes air circulation",
            "Includes rubber floor protectors",
            "Fits 8-inch nursery liners"
        ],
        "care": {
            "light": "All",
            "water": "Wipe clean",
            "humidity": "Water-resistant glaze"
        },
        "image": "/static/images/products/pot-305.jpg",
        "secondary_images": [
            "/static/images/products/pot-305.jpg"
        ]
    },
    {
        "id": "pot-306",
        "name": "Heavy-Duty Metal Railing Balcony Flower Pots (Pack of 4)",
        "category": "pots",
        "category_label": "Flower Pots & Planters",
        "price": 849,
        "original_price": 1299,
        "rating": 4.7,
        "reviews_count": 1450,
        "badge": "Best Seller",
        "in_stock": True,
        "description": "Powder-coated rustproof wrought iron balcony railing hanging pots designed for compact apartment gardens.",
        "features": [
            "Detachable sturdy hanging hooks",
            "Weather-resistant electroplated coat",
            "Bottom drainage hole",
            "Holds up to 10 kg per pot"
        ],
        "care": {
            "light": "Balcony outdoor",
            "water": "Direct watering",
            "humidity": "Rust-proof"
        },
        "image": "/static/images/products/pot-306.jpg",
        "secondary_images": [
            "/static/images/products/pot-306.jpg"
        ]
    },
    {
        "id": "pot-307",
        "name": "Geometric Origami Faceted Planter with Brass Saucer",
        "category": "pots",
        "category_label": "Flower Pots & Planters",
        "price": 729,
        "original_price": 999,
        "rating": 4.8,
        "reviews_count": 560,
        "badge": "Popular",
        "in_stock": True,
        "description": "Faceted multi-angle decorative planter that catches natural light uniquely throughout the day.",
        "features": [
            "Faceted prism geometry",
            "Includes spun brass drip plate",
            "Engineered drainage hole",
            "Smooth matte glazed texture"
        ],
        "care": {
            "light": "Window or desk display",
            "water": "Drain excess water",
            "humidity": "All"
        },
        "image": "/static/images/products/pot-307.jpg",
        "secondary_images": [
            "/static/images/products/pot-307.jpg"
        ]
    },
    {
        "id": "pot-308",
        "name": "Handmade Clay Studio Terracotta Pot (Warm Earth Tone)",
        "category": "pots",
        "category_label": "Flower Pots & Planters",
        "price": 489,
        "original_price": 699,
        "rating": 4.7,
        "reviews_count": 430,
        "badge": "Handmade",
        "in_stock": True,
        "description": "Authentic potter-thrown raw clay pot featuring natural earth tones and tactile ribbed contour for cacti and jade plants.",
        "features": [
            "100% natural kiln-fired clay",
            "Aerates roots naturally",
            "Thermal insulation protects roots",
            "Includes matching clay saucer"
        ],
        "care": {
            "light": "Sunlight friendly",
            "water": "Porous fast drying",
            "humidity": "All"
        },
        "image": "/static/images/products/pot-308.jpg",
        "secondary_images": [
            "/static/images/products/pot-308.jpg"
        ]
    },
    {
        "id": "dec-401",
        "name": "Geometric Glass Octahedron Terrarium with Brass Edge",
        "category": "decor",
        "category_label": "Home Decor with Plants",
        "price": 1099,
        "original_price": 1599,
        "rating": 4.9,
        "reviews_count": 1580,
        "badge": "Best Seller",
        "in_stock": True,
        "description": "Hand-soldered brass geometric display case for air plants, ferns, fairy moss, and micro-succulent landscapes.",
        "features": [
            "Ultra-clear tempered glass",
            "Antique brass sealed seams",
            "Open side facet for ventilation",
            "Includes fairy moss sample"
        ],
        "care": {
            "light": "Bright indirect light",
            "water": "Mist weekly",
            "humidity": "Self-sustaining microclimate"
        },
        "image": "/static/images/products/dec-401.jpg",
        "secondary_images": [
            "/static/images/products/dec-401.jpg"
        ]
    },
    {
        "id": "dec-402",
        "name": "Mid-Century Walnut Adjustable Wood Plant Stand Riser",
        "category": "decor",
        "category_label": "Home Decor with Plants",
        "price": 899,
        "original_price": 1299,
        "rating": 4.8,
        "reviews_count": 2790,
        "badge": "Amazon's Choice",
        "in_stock": True,
        "description": "Expandable solid hardwood plant riser adjusting from 8 to 12 inches to highlight floor planters with elegance.",
        "features": [
            "Solid sustainably sourced beech wood",
            "Supports up to 70 kg",
            "Adjusts 8-12 inches wide",
            "Two height settings by flipping"
        ],
        "care": {
            "light": "Indoor furniture",
            "water": "Wipe with damp cloth",
            "humidity": "Stained wood seal"
        },
        "image": "/static/images/products/dec-402.jpg",
        "secondary_images": [
            "/static/images/products/dec-402.jpg"
        ]
    },
    {
        "id": "dec-403",
        "name": "Pyramid Glass Botanical Prism Terrarium",
        "category": "decor",
        "category_label": "Home Decor with Plants",
        "price": 749,
        "original_price": 1099,
        "rating": 4.7,
        "reviews_count": 890,
        "badge": "Trending",
        "in_stock": True,
        "description": "Sleek tabletop glass pyramid terrarium designed for air plants, pebbles, and tiny succulent gardens.",
        "features": [
            "Heavy clear float glass",
            "Lead-free solder seams",
            "Open triangular access door",
            "Compact coffee table centerpiece"
        ],
        "care": {
            "light": "Filtered daylight",
            "water": "Light misting",
            "humidity": "Moderate"
        },
        "image": "/static/images/products/dec-403.jpg",
        "secondary_images": [
            "/static/images/products/dec-403.jpg"
        ]
    },
    {
        "id": "dec-404",
        "name": "Preserved Reindeer Forest Moss Living Wall Frame",
        "category": "decor",
        "category_label": "Home Decor with Plants",
        "price": 1299,
        "original_price": 1899,
        "rating": 4.9,
        "reviews_count": 520,
        "badge": "No Maintenance",
        "in_stock": True,
        "description": "Zero-care real Scandinavian preserved moss artwork in natural wood frame. Stays vibrant and soft for years.",
        "features": [
            "100% natural preserved real moss",
            "Requires ZERO water or sunlight",
            "Acoustic sound dampening properties",
            "Ready to hang"
        ],
        "care": {
            "light": "Keep away from direct heat",
            "water": "NEVER WATER",
            "humidity": "Indoor ambient"
        },
        "image": "/static/images/products/dec-404.jpg",
        "secondary_images": [
            "/static/images/products/dec-404.jpg"
        ]
    },
    {
        "id": "dec-405",
        "name": "Desktop Hydroponic Glass Bulb Swivel Vase Stand",
        "category": "decor",
        "category_label": "Home Decor with Plants",
        "price": 599,
        "original_price": 849,
        "rating": 4.8,
        "reviews_count": 1240,
        "badge": "Popular",
        "in_stock": True,
        "description": "Charming vintage tabletop propagation bulb vase on a swivel metal rod and dark walnut finish wooden stand for study desks.",
        "features": [
            "Clear heat-resistant lab glass bulb",
            "Solid natural wooden swivel bracket",
            "Great for pothos cuttings, bamboo, and flowers",
            "Rubber washers keep glass secure"
        ],
        "care": {
            "light": "Ambient indoor light",
            "water": "Change water every 7 days",
            "humidity": "Normal"
        },
        "image": "/static/images/products/dec-405.jpg",
        "secondary_images": [
            "/static/images/products/dec-405.jpg"
        ]
    },
    {
        "id": "dec-406",
        "name": "Tiered Bamboo Plant Ladder Display Shelf (Multi-Level)",
        "category": "decor",
        "category_label": "Home Decor with Plants",
        "price": 1499,
        "original_price": 2299,
        "rating": 4.8,
        "reviews_count": 780,
        "badge": "Top Rated",
        "in_stock": True,
        "description": "Multi-tier carbonized bamboo display rack allowing multiple planters to receive optimal sunlight in living rooms and balconies.",
        "features": [
            "High temperature carbonized bamboo",
            "Holds up to 8 medium-large planters",
            "Open slat design for air circulation",
            "Includes assembly hardware & tools"
        ],
        "care": {
            "light": "Indoor or covered patio",
            "water": "Wipe with soft cloth",
            "humidity": "Waterproof lacquer"
        },
        "image": "/static/images/products/dec-406.jpg",
        "secondary_images": [
            "/static/images/products/dec-406.jpg"
        ]
    },
    {
        "id": "dec-407",
        "name": "Handwoven Natural Seagrass Belly Plant Basket",
        "category": "decor",
        "category_label": "Home Decor with Plants",
        "price": 699,
        "original_price": 999,
        "rating": 4.8,
        "reviews_count": 1350,
        "badge": "Best Seller",
        "in_stock": True,
        "description": "Artisan woven seagrass storage basket designed as an organic cover for fiddle leaf figs, monsteras, and palms.",
        "features": [
            "100% natural seagrass fibers",
            "Foldable top rim creates shallow bowl",
            "Double reinforced carrying handles",
            "Interior plastic liner included"
        ],
        "care": {
            "light": "Indoor living areas",
            "water": "Use inner plastic tray",
            "humidity": "Keep dry"
        },
        "image": "/static/images/products/dec-407.jpg",
        "secondary_images": [
            "/static/images/products/dec-407.jpg"
        ]
    },
    {
        "id": "dec-408",
        "name": "Botanical Fairy Light Climbing Plant Garland",
        "category": "decor",
        "category_label": "Home Decor with Plants",
        "price": 449,
        "original_price": 649,
        "rating": 4.7,
        "reviews_count": 910,
        "badge": "Gift Favorite",
        "in_stock": True,
        "description": "Warm-white micro LED wire lights interwoven with realistic silk ivy leaves for magical bedroom headboards and balcony canopies.",
        "features": [
            "10 meters with 100 warm LED bulbs",
            "Waterproof copper wire string",
            "USB powered with remote dimmer",
            "Creates cozy botanical glow"
        ],
        "care": {
            "light": "Indoor ambiance",
            "water": "Keep USB plug dry",
            "humidity": "Normal"
        },
        "image": "/static/images/products/dec-408.jpg",
        "secondary_images": [
            "/static/images/products/dec-408.jpg"
        ]
    },
    {
        "id": "tool-501",
        "name": "Heritage Gold & Emerald Floral Pruning Shears",
        "category": "tools",
        "category_label": "Gardening Tools",
        "price": 699,
        "original_price": 999,
        "rating": 4.9,
        "reviews_count": 3410,
        "badge": "Best Seller",
        "in_stock": True,
        "description": "Titanium coated SK5 high-carbon steel bypass clippers with ergonomic non-slip botanical grip and safety lock.",
        "features": [
            "SK-5 Japanese high carbon steel blade",
            "Cuts up to 3/4 inch diameter branches",
            "Sap groove prevents sticking",
            "Smooth spring action"
        ],
        "care": {
            "light": "Tool storage",
            "water": "Wipe blade with oil after use",
            "humidity": "Store dry"
        },
        "image": "/static/images/products/tool-501.jpg",
        "secondary_images": [
            "/static/images/products/tool-501.jpg"
        ]
    },
    {
        "id": "tool-502",
        "name": "Vintage Long-Spout Copper & Forest Green Watering Can",
        "category": "tools",
        "category_label": "Gardening Tools",
        "price": 849,
        "original_price": 1199,
        "rating": 4.8,
        "reviews_count": 1920,
        "badge": "Amazon's Choice",
        "in_stock": True,
        "description": "1.5L slender stainless spout delivers pinpoint water flow straight to roots without splashing delicate foliage.",
        "features": [
            "Precision targeted narrow spout",
            "Balanced ergonomic handle",
            "Heavy-gauge galvanised steel body",
            "Leak-tested weld joints"
        ],
        "care": {
            "light": "Display worthy",
            "water": "Holds 1.5 Liters",
            "humidity": "Rust proof finish"
        },
        "image": "/static/images/products/tool-502.jpg",
        "secondary_images": [
            "/static/images/products/tool-502.jpg"
        ]
    },
    {
        "id": "tool-503",
        "name": "3-in-1 Soil Moisture, pH & Sunlight Meter Probe",
        "category": "tools",
        "category_label": "Gardening Tools",
        "price": 499,
        "original_price": 749,
        "rating": 4.6,
        "reviews_count": 4890,
        "badge": "Must Have",
        "in_stock": True,
        "description": "Battery-free dual probe gives instant readings on root moisture levels, light exposure, and soil acidity.",
        "features": [
            "No batteries needed",
            "Dual probe technology",
            "Instant dial readout",
            "Protects against under & overwatering"
        ],
        "care": {
            "light": "Sensor tested",
            "water": "Do not submerge dial in water",
            "humidity": "Wipe probes after test"
        },
        "image": "/static/images/products/tool-503.jpg",
        "secondary_images": [
            "/static/images/products/tool-503.jpg"
        ]
    },
    {
        "id": "tool-504",
        "name": "Organic Cold-Pressed Atlantic Kelp Bio-Stimulant (500ml)",
        "category": "tools",
        "category_label": "Gardening Tools",
        "price": 399,
        "original_price": 599,
        "rating": 4.9,
        "reviews_count": 1130,
        "badge": "Organic Pro",
        "in_stock": True,
        "description": "Cold-pressed Atlantic kelp booster promotes vigorous flowering, lush foliage density, and transplant shock resistance.",
        "features": [
            "Contains 60+ micronutrients",
            "Encourages explosive root growth",
            "100% pet & child safe",
            "Concentrated: yields 100 gallons"
        ],
        "care": {
            "light": "Store in cool shade",
            "water": "Dilute 1 cap per gallon",
            "humidity": "Sealed cap"
        },
        "image": "/static/images/products/tool-504.jpg",
        "secondary_images": [
            "/static/images/products/tool-504.jpg"
        ]
    },
    {
        "id": "tool-505",
        "name": "Heavy-Duty Stainless Steel Hand Trowel with Measurement Scale",
        "category": "tools",
        "category_label": "Gardening Tools",
        "price": 549,
        "original_price": 799,
        "rating": 4.8,
        "reviews_count": 1620,
        "badge": "Trending",
        "in_stock": True,
        "description": "Cast stainless steel gardening trowel with etched centimeter and inch depth markings and non-slip rubberized comfort grip.",
        "features": [
            "Mirror polished rust-resistant head",
            "Engraved inch and centimeter depth gauges",
            "Hanging hole for easy storage",
            "Lifetime breakage warranty"
        ],
        "care": {
            "light": "Store dry",
            "water": "Wash and wipe dry after digging",
            "humidity": "Indoor shed"
        },
        "image": "/static/images/products/tool-505.jpg",
        "secondary_images": [
            "/static/images/products/tool-505.jpg"
        ]
    },
    {
        "id": "tool-506",
        "name": "Continuous Ultra-Fine Mist Spray Bottle for Plants (300ml)",
        "category": "tools",
        "category_label": "Gardening Tools",
        "price": 349,
        "original_price": 499,
        "rating": 4.7,
        "reviews_count": 2240,
        "badge": "Popular",
        "in_stock": True,
        "description": "Aerosol-free continuous fine mist sprayer that hydrates orchids, monsteras, and seedlings without soaking foliage.",
        "features": [
            "0.3mm nozzle delivers consistent aerosol-like mist",
            "360-degree spraying angle",
            "Reduces hand fatigue with pre-compression trigger",
            "BPA-free durable PET"
        ],
        "care": {
            "light": "Indoor",
            "water": "Fill with distilled or tap water",
            "humidity": "Ambient"
        },
        "image": "/static/images/products/tool-506.jpg",
        "secondary_images": [
            "/static/images/products/tool-506.jpg"
        ]
    },
    {
        "id": "tool-507",
        "name": "Solid Brass Heavy-Duty Adjustable Garden Hose Nozzle",
        "category": "tools",
        "category_label": "Gardening Tools",
        "price": 499,
        "original_price": 699,
        "rating": 4.8,
        "reviews_count": 890,
        "badge": "Top Rated",
        "in_stock": True,
        "description": "Machined solid brass twist nozzle delivering everything from a gentle fine spray for seedbeds to high-pressure patio blast.",
        "features": [
            "100% solid rustproof brass",
            "Internal O-ring leakproof seal",
            "Twist adjustment from mist to jet",
            "Fits standard garden hoses"
        ],
        "care": {
            "light": "Outdoor storage",
            "water": "Drain in freezing weather",
            "humidity": "Corrosion-resistant"
        },
        "image": "/static/images/products/tool-507.jpg",
        "secondary_images": [
            "/static/images/products/tool-507.jpg"
        ]
    },
    {
        "id": "tool-508",
        "name": "Heavy-Duty Ergonomic Garden Hand Cultivator Rake",
        "category": "tools",
        "category_label": "Gardening Tools",
        "price": 429,
        "original_price": 619,
        "rating": 4.7,
        "reviews_count": 640,
        "badge": "Eco Choice",
        "in_stock": True,
        "description": "3-prong steel hand cultivator engineered to loosen compacted soil, remove weeds, and mix compost around roots.",
        "features": [
            "Heat-treated carbon steel tines",
            "Comfort contoured ergonomic grip",
            "Perfect for flower beds and containers",
            "Durable rust-inhibiting coating"
        ],
        "care": {
            "light": "Store dry",
            "water": "Rinse clean after use",
            "humidity": "Shed dry"
        },
        "image": "/static/images/products/tool-508.jpg",
        "secondary_images": [
            "/static/images/products/tool-508.jpg"
        ]
    }
]

CATEGORIES = [
    {"id": "all", "name": "All Botanical", "icon": "fa-th-large", "count": len(PRODUCTS)},
    {"id": "plants", "name": "Live Plants", "icon": "fa-seedling", "count": 8},
    {"id": "seeds", "name": "Seeds & Bulbs", "icon": "fa-spa", "count": 8},
    {"id": "pots", "name": "Flower Pots & Planters", "icon": "fa-archive", "count": 8},
    {"id": "decor", "name": "Home Decor with Plants", "icon": "fa-couch", "count": 8},
    {"id": "tools", "name": "Gardening Supplies", "icon": "fa-tools", "count": 8}
]

@bp.route('/')
def index():
    return render_template('index.html', categories=CATEGORIES)

@bp.route('/api/products', methods=['GET'])
def get_products():
    category = request.args.get('category', 'all').lower()
    search = request.args.get('q', '').strip().lower()
    sort = request.args.get('sort', 'featured')
    badge = request.args.get('badge', '').lower()
    
    filtered = PRODUCTS
    if category and category != 'all':
        filtered = [p for p in filtered if p['category'] == category]
        
    if search:
        search_terms = [t for t in search.split() if t]
        def matches_product(p):
            p_text = f"{p['name']} {p['description']} {p['category_label']} {p['category']} {' '.join(p.get('features', []))}".lower()
            # If all search words appear anywhere in product info
            return all(term in p_text for term in search_terms)
        
        filtered_by_cat = [p for p in filtered if matches_product(p)]
        # If user searched within a specific department but got 0 results, also check all departments so they aren't stuck with empty search
        if not filtered_by_cat and category != 'all':
            filtered_by_cat = [p for p in PRODUCTS if matches_product(p)]
        filtered = filtered_by_cat

    if badge:
        filtered = [p for p in filtered if p.get('badge', '').lower() == badge]

    if sort == 'price-low':
        filtered = sorted(filtered, key=lambda x: x['price'])
    elif sort == 'price-high':
        filtered = sorted(filtered, key=lambda x: x['price'], reverse=True)
    elif sort == 'rating':
        filtered = sorted(filtered, key=lambda x: x['rating'], reverse=True)
    elif sort == 'reviews':
        filtered = sorted(filtered, key=lambda x: x['reviews_count'], reverse=True)
        
    return jsonify({
        "status": "success",
        "total": len(filtered),
        "products": filtered
    })

@bp.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404
        
    # Related products
    related = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != product_id][:4]
    return jsonify({
        "status": "success",
        "product": product,
        "related": related
    })

@bp.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify({
        "status": "success",
        "categories": CATEGORIES
    })

@bp.route('/api/checkout', methods=['POST'])
def checkout():
    data = request.get_json() or {}
    items = data.get('items', [])
    shipping = data.get('shipping', {})
    
    order_id = f"PLANT-{random.randint(100000, 999999)}"
    total = sum(item.get('price', 0) * item.get('quantity', 1) for item in items)
    
    return jsonify({
        "status": "success",
        "order_id": order_id,
        "total": round(total, 2),
        "items_count": len(items),
        "delivery_estimate": "2-4 Business Days",
        "shipping_address": shipping.get('address', 'Customer Address'),
        "message": "Order placed successfully! Eco-friendly packaging prepared."
    })
