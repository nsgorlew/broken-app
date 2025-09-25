Bu uygulama şu yığını kullanır: Nginx, Gunicorn, FastAPI

-Uygulama bir Docker konteynerinde çalışır.
-Nginx, ters proxy görevi görür ve istekleri Gunicorn çalışanlarına dağıtır.
-Her Gunicorn çalışanı, FastAPI uygulamasını çalıştıran bir işlemdir.

Senaryo:

-Banka A'nın, müşterilerine kredi faiz oranlarını vermek için kullandığı bir XYZ uygulaması vardır.
-Bir müşteri kredi başvurusunda bulunur ve başvuru XYZ uygulamasına gönderilir.
-Uygulama, en iyi faiz oranını tahmin eden bir Makine Öğrenimi modeli kullanır.
-Bu faiz oranı, istek göndericisine döndürülür.

Sorun:

XYZ uygulaması amaçlandığı gibi çalışıyor. Ancak 18.00-19.30 saatleri arasında aynı anda gönderilen kredi başvurularının sayısı önemli ölçüde artıyor.
Bu süre zarfında performans hızla düşüyor. Trafikte artış olduğunda performansı iyileştirmenin yollarını bulmamız gerekiyor.

--------------------------------------------------------

This app uses the following stack: Nginx, Gunicorn, FastAPI

-The application runs in a Docker container
-Nginx acts as a reverse proxy and distributes requests to Gunicorn workers
-Each Gunicorn worker is a process running the FastAPI application


Scenario:

-Bank A has an app XYZ that it uses to give loan interest rates for customers.
-A customer applies for a loan and the application is sent to app XYZ.
-The app uses a Machine Learning model that predicts the best interest rate.
-That interest rate is returned to the request sender.



Problem:

App XYZ works as intended. But from 18.00-19.30, the amount of loan applications sent at the same time increases a lot.
Performance quickly degrades during this time. We need to find ways to improve the performance when there is an increase in traffic.
