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
    ('^/mytransactions', userTransactionsView),
    ('^/conftrans', confirmTransactionView),
    ('^/canctrans', cancelTransactionView),
    ('^/cancprod', cancelProductView),
    ('^/cancbid', cancelBidView),
    ('^/cancrep', cancelReportView),
    ('^/reportdashboard', reportDashboardView),
    ('^/myaccount', myAccountView),

    # User Views END

    # Product Views START

    ('^/searchpage', searchPageView),
    ('^/search', searchView),
    ('^/getproductids', searchProductIDsView),
    ('^/product', productView),
    ('^/bid', bidView),
    ('^/buy', buyView),
    ('^/createlistingrequest/?$', createListingRequestView),
    ('^/createlisting/?$', createListingView),

    # QA

    ('^/postquestionrequest/?$', postQuestionRequestView),
    ('^/postanswerrequest/?$', postAnswerRequestView),

    # Product Views END

    # API / Export START

    ('^/api/json/?', jsonExportView),
    ('^/feed/?$', feedView),
    ('^/api/xml', xmlView),
    ('^/api/pdf', pdfView),


    # API / Export END

    ('^/favicon.ico$', globalFavicon),
    ('^/public/*', publicFileView),
    ('^/home', homepageView),
    ('^/$', homepageView),
    ('*', view)
]

