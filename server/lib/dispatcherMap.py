from view import *
from testViews import *
from generalViews import *
from userViews import *
from productViews import *

# Aici mapam expresii regulate view-urilor. Cand se primeste un request, dispatcherul verifica toate expresiile regulate in ordine si apeleaza view-ul corespunzator

map = [

    #test views
    ('^/addprod', addProductView),
    ('^/adduser', addUserView),
    #
    ('^/public/*', publicFileView),
    ('^/jinjatest', jinjatest),

    # User Views START

    ('^/registration/?$', userRegistrationPageView),
    ('^/registrationrequest/?$', userRegistrationRequestView),
    ('^/userlistings/?$', userListingView),
    ('^/userSignIn/?$', userSignInView),

    # User Views END

    # Product Views START

    ('^/search_page', searchPageView),
    ('^/search', searchView),
    ('^/getproductids', searchProductIDsView),
    ('^/product', productView),
    ('^/bid', bidView),
    ('^/createlistingrequest/?$', createListingRequestView),
    ('^/createlisting/?$', createListingView),

    # Product Views END


    ('^/', homepageView),
    ('*', view)
]
