from view import *
from testViews import *
from generalViews import *
from userViews import *

# Aici mapam expresii regulate view-urilor. Cand se primeste un request, dispatcherul verifica toate expresiile regulate in ordine si apeleaza view-ul corespunzator

map = [
    ('^/public/*', publicFileView),
    ('^/jinjatest', jinjatest),

    # User Registration START

    ('^/registration', userRegistrationPage),

    # User Registration END

    ('^/userlistings', userListingView),

    ('^/', homepageView),
    ('*', view)
]
