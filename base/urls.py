from django.urls import path
# from django.views.static import serve #Debug=FALSE durumunda static dosyaların erişimi için...
from . import views

# static klasöründeki öğelere erişim için.. örnek : favicon.ico
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView


urlpatterns = [
    path('', views.home, name="home_page_name_in_urls"),
    #path(url, vievs.function, name)

    # buradaki name değişkeni templatelerin içindekıi {% url bla_bla_bla %} kısmında kullanılıyor.
    # URL'deki 'oda_link' i değiştirdiğimizde,
    # template'in  içindeki linkler {% url %} name'e baktığı için olumsuz etkilenmiyor.
    # hem de templatedeki <a> linklerde esneklik kazanıyoruz.

    path('oda_link/<str:room_id_in_url>/',
         views.room, name="room_page_name_in_urls"),
    path('create-room/', views.createRoom, name="create-room_in_urls"),
    path('update-room/<str:room_id_in_url>/',
         views.updateRoom, name="update-room_in_urls"),
    path('delete-room/<str:room_id_in_url>/',
         views.deleteRoom, name="delete-room_in_urls"),

    # Oda numarası verilmezse boş oda fonksiyonuna gidilsin..
    path('oda_link/', views.empty_room, name="empty_room_page_name_in_urls"),


    # Teşekkürler sayfası (Room oluşturulduktan sonra)
    path('thank-you/', views.form_submitted, name="form_submitted_in_urls"),

    # static dosyalar ve favicon
    path("favicon.ico", RedirectView.as_view(
        url=staticfiles_storage.url("favicon.ico")),),
]
