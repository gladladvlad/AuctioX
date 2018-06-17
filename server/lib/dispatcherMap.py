from view import *
from testViews import *
from generalViews import *
from userViews import *
from productViews import *
from apiViews import *

# Aici mapam expresii regulate view-urilor. Cand se primeste un request, dispatcherul verifica toate expresiile regulate in ordine si apeleaza view-ul corespunzator

map = [

    #test views
    ('^/addprod', addProductView),
    ('^/adduser', addUserView),
    #
    ('^/setcookie', setCookieView),
    ('^/sessiontest', sessionValidation),
    #
    ('^/jinjatest', jinjatest),

    # User Views START

    ('^/registration/?$', userRegistrationPageView),
    ('^/registrationrequest/?$', userRegistrationRequestView),
    ('^/signin/?$', userSignInView),
    ('^/signinrequest/?$', userSignInRequestView),
    ('^/signout/?$', userSignOutRequestView),

    ('^/userlistings/?$', userListingView),
    ('^/mylistings/?$', userMyListingsView),
    ('^/mybids/?$', userMyBidsView),

    # User Views END

    # Product Views START

    ('^/searchpage', searchPageView),
    ('^/search', searchView),
    ('^/getproductids', searchProductIDsView),
    ('^/product', productView),
    ('^/bid', bidView),
    ('^/createlistingrequest/?$', createListingRequestView),
    ('^/createlisting/?$', createListingView),

    # Product Views END

    # API / Export START

    ('^/api/json/?', jsonExportView),

    # API / Export END

    ('^/public/*', publicFileView),
    ('^/', homepageView),
    ('*', view)
]

