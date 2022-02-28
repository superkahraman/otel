from ast import operator
from django.shortcuts import render, redirect
from .models import Room  # models'deki Room modelini alıyoruz.
from .forms import RoomForm  # forms.py'dan gelen class

# Create your views here.

odalar = [
    {'id': 1, 'name': 'Room One'},
    {'id': 2, 'name': 'Room Two'},
    {'id': 3, 'name': 'Room Three'},
]


def home(request):
    odalar = Room.objects.all()

    icerik = {'rooms_list_in_view': odalar}
    # rooms_list_in_view home.html template'e gönderiliyor.
    return render(request, 'base/home.html', icerik)


def room(request, room_id_in_url):
    oda = Room.objects.get(id=room_id_in_url)
    # o id ile 'oda_in_view' adıyla template gönderiyoruz
    icerik = {'oda_in_view': oda}
    return render(request, 'base/room.html', icerik)


def empty_room(request):
    return render(request, 'base/empty_room.html')


def createRoom(request):
    form_data = RoomForm()  # forms.py'da tanımladık..

    # FORM KAYIT İŞLEMLERİ
    if request.method == 'POST':  # Formumuzda action olarak kendini göstermiştik. Yani Submit edildiğinde
        # buraya POST datası gönderiyor.
        form_gelen = RoomForm(request.POST)  # Gelen POST datamızı okuyalım..
        if form_gelen.is_valid():  # Eğer formumuzda bir sıkıntı yok ve 'valid' ise
            # Form bilgisini kaydedelim. Kayıttan sonra urls'de belirtilen sayfaya yönlendirelim..
            form_gelen.save()
            # return redirect('form_submitted_in_urls'), #Bu fonksiyon önce urls'e gönderip, orda bir URL tanımlatıp, sonra orda belirtilen view'a gelip, sonucu view'daki fonksiyonla render eder.
            # Burada belirttiğimiz HTML sayfayı direk render eder, ve URL değişmez.
            return render(request, 'base/form_submitted.html')

    icerik = {'form_template': form_data}
    return render(request, 'base/room_form.html', icerik)

# return redirect('form_submitted_in_urls'),
#
# Form submit edildikten sonra sayfayı redirect() ile urls'deki form_submitted_in_urls isimli path'e gönderiyoruz.
# O path'de aşağıdaki form_submitted() view fonksiyonunu tetikliyor.
# Bu fonksiyon da form_submitted.html dosyasını render ediyor..
# Sonuç olarak URL'de localhost/thank-you şeklinde sayfaya gitmiş oluyoruz.

# return render(request, 'base/form_submitted.html')
# Form http://localhost/create-room/ URL'inde doldurulup, yine aynı URL'de submit edilince
# bu sefer URL değiştirmeden sadece form_submitted.html 'i render ediyoruz.
# URL'de hala /create-room/ kalıyor ama bize Teşekkürler mesajı gösteriliyor (html'den gelen)
#
#


def form_submitted(request):
    return render(request, 'base/form_submitted.html')


def updateRoom(request, room_id_in_url):
    room_data = Room.objects.get(id=room_id_in_url)
    form_data = RoomForm(instance=room_data)

    # FORM GÜNCELLEME İŞLEMLERİ
    if request.method == 'POST':  # Formumuzda action olarak kendini göstermiştik. Yani Submit edildiğinde
        # buraya POST datası gönderiyor.
        # Gelen POST datamızı okuyalım..
        form_gelen = RoomForm(request.POST, instance=room_data)
        if form_gelen.is_valid():  # Eğer formumuzda bir sıkıntı yok ve 'valid' ise
            form_gelen.save()  # Form bilgisini kaydedelim.
            # kayıttan sonra urls'de belirtilen sayfaya yönlendirelim..
            return redirect('form_submitted_in_urls')

    icerik = {'form_template': form_data}
    return render(request, 'base/room_form.html', icerik)


# Acımasız deleteRoom fonksiyonumuz
# models'da tanımladığımız Room objesinin id'sini, url'deki id ile eşleyip o kaydı direk siliyor.
# Bam gümm!! Herhangi bir kontrol yok: URL'de delete-room/blabla desek bile işi yapıp
# yapmadığına bakmadan direk HTML'i render ediyor.
def deleteRoom(request, room_id_in_url):
    Room.objects.filter(id=room_id_in_url).delete()
    return render(request, 'base/room_deleted.html')
