from django.shortcuts import render, redirect
from .models import Room, Topic  # models'deki Room modelini alıyoruz.
from .forms import RoomForm  # forms.py'dan gelen class
from django.db.models import Q  # Objects.filter'da  and/or vs kullanmak için
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.


def home(request):

    if request.GET.get('ara') != None:
        aranan_sey = request.GET.get('ara')
    else:
        aranan_sey = ''

    print(aranan_sey)

    # Bu şekilde bir filte kullanınca hem Room modelinin topic.name'inde hem de Room.name'de arama yaptırabiliyoruz.
    # Bunu Q yapıyor. ( | bu işaret OR anlamına geliyor. Tabii ki & AND'de kullanabiliriz..)
    odalar = Room.objects.filter(
        Q(topic__name__icontains=aranan_sey) | Q(name__icontains=aranan_sey) | Q(description__icontains=aranan_sey))

    topics = Topic.objects.all()  # Home'da sidebar'da Topic'leri listelemek için

    oda_sayisi = odalar.count()

    icerik = {'rooms_list_in_view': odalar,
              'topics': topics, 'aranan_sey': aranan_sey, 'oda_sayisi': oda_sayisi}
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


# Buraya bir "id" ile geliyoruz.
# O id'nin içeriği Room.objects.get ile alıyoruz ve delete_confirm templatini döndürüyoruz
# O template'de bir form var. methodu da POST
# eğer bu view'a POST datası gelirse, ilgili odayı siliyoruz.
# Ve room_deleted templatini döndürüyoruz..
def deleteRoom(request, room_id_in_url):
    # Room.objects.filter(id=room_id_in_url).delete()
    room = Room.objects.get(id=room_id_in_url)
    if request.method == 'POST':
        room.delete()
        return render(request, 'base/room_deleted.html')
    return render(request, 'base/delete_confirm.html', {'obj': room})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exists")
    icerik = {}
    return render(request, "base/login_register.html", icerik)
