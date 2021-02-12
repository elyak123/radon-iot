from django.urls import path, include

app_name = 'api'

urlpatterns = [

    ####################################################
    # ####    U R L S   A P I   P U B L I C A      #####
    ####################################################


    ####################
    #  URLS PARA IOT #
    ####################
    path('iot/', include('radon.api.urls.ioturls')),

    ####################
    #  URLS PARA USERS #
    ####################
    path('users/', include('radon.api.urls.usersurls')),

    #####################
    #  URLS PARA MARKET #
    #####################
    path('market/', include('radon.api.urls.marketurls')),

    ####################
    #  URLS PARA RUTAS #
    ####################
    path('rutas/', include('radon.api.urls.rutasurls')),

    ###########################
    #  URLS PARA GEORADON API #
    ###########################
    path('geo/', include('radon.api.urls.georadonurls')),

    ################################
    #  URLS PARA AUTENTICACION API #
    ################################
    path('auth/', include('radon.api.urls.authurls')),


    ####################################################
    # ####    U R L S   A P I   P R I V A D A      #####
    ####################################################

    #############################
    #  URLS PARA APP CONSUMIDOR #
    #############################
    path('app/', include('radon.app.apiurls')),

    ###########################
    #  URLS PARA CRM CLIENTES #
    ###########################
    path('crm/', include('radon.crm.apiurls')),
]
