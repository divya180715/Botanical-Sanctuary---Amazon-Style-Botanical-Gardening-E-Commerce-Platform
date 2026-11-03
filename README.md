# Botanical Sanctuary — E-Commerce Store

Amazon-style botanical marketplace featuring curated live plants, flower seeds, designer ceramic planters, decorative botanical home pieces, and gardening tools.

## Structure
```
e:\pythonprj\
├── run.py                          # Flask entrypoint script
├── requirements.txt                # Python dependencies
│
└── app\
    ├── __init__.py                 # App factory & blueprint registration
    ├── config.py                   # App configuration
    │
    ├── routes\
    │   ├── __init__.py
    │   └── main.py                 # REST APIs (/api/products, /api/checkout) & store route
    │
    ├── static\
    │   ├── css\
    │   │   └── style.css           # Amazon-style botanical theme & responsive CSS
    │   │
    │   └── js\
    │       └── main.js             # Cart logic, catalog fetching, filter, search, modals
    │
    └── templates\
        ├── base.html               # Amazon navbar, category ribbon, cart drawer, modals
        └── index.html              # Hero carousel, department cards, product grid
```

## Running the Project
```bash
python run.py
```
Visit `http://127.0.0.1:5000` in your web browser.
