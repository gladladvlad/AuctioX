from views import *

# Aici mapam expresii regulate view-urilor. Cand se primeste un request, dispatcherul verifica toate expresiile regulate in ordine si apeleaza view-ul corespunzator

map = [
    {'regex': '^/public/*', 'view': publicFileResponse},
    {'regex': '^/signin/?', 'view': publicFileResponse},
    {'regex': '^/',         'view': homepage}
]