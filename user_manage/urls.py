from django.conf.urls import patterns, include, url
from django.contrib import admin
from user_manage import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ELive.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r"^get_first_page/$",views.get_first_page),
    url(r"^login/$",views.login,name='login'),
    url(r"^lucky_draw/$",views.lucky_draw,name='lucky_draw'),
    url(r"^routette/$",views.routette,name='routette'),
    url(r"^credit_exchange/$",views.credit_exchange,name='credit_exchange'),
    url(r"^sign_in/$",views.sign_in,name='sign_in'),
    url(r"^get_credit_exchange_goods/$",views.get_credit_exchange_goods,name='get_credit_exchange_goods'),
    url(r"^get_lucky_draw_goods/$",views.get_lucky_draw_goods,name='get_lucky_draw_goods'),
    url(r"^get_records/$",views.get_records,name='get_records'),
    url(r"^get_user_information/$",views.get_user_information,name='get_user_information'),
    url(r"^logout/$",views.logout,name='logout'),
    url(r"^get_like_goods/$",views.get_like_goods,name='get_like_goods'),
    url(r"^get_new_goods/$",views.get_new_goods,name='get_new_goods'),
    url(r"^friends_invitation/$",views.friends_invitation,name='friends_invitation'),
    url(r"^add_oil/$",views.add_oil,name='add_oil'),
    
)
