from views import *

# Aici mapam expresii regulate view-urilor. Cand se primeste un request, dispatcherul verifica toate expresiile regulate in ordine si apeleaza view-ul corespunzator

map = [
    ('^/public/*', publicFileView),
    ('^/jinjatest', jinjatest),
    ('^/', view)
]