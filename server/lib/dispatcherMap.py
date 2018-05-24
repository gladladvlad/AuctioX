from views import *

# Aici mapam expresii regulate view-urilor. Cand se primeste un request, dispatcherul verifica toate expresiile regulate in ordine si apeleaza view-ul corespunzator

map = [
    {'regex': '^/public/*', 'view': publicPageView},
    {'regex': '^/signin/?', 'view': view},
    {'regex': '^/',         'view': view}
]

pageMap = {
    'home': '/public/static/html/home.html',
    'search': '/public/static/html/search.html',
    'advancedSearch': '/public/static/html/advancedSearch.html',
    'product': '/public/static/html/product.html',
}