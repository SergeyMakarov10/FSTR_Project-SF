# FSTR-Project---Skillfactory
ФСТР заказала студентам SkillFactory разработать мобильное приложение для Android и IOS, которое упростило бы туристам задачу по отправке данных о перевале и сократило время обработки запроса до трёх дней.

Пользоваться мобильным приложением будут туристы. В горах они будут вносить данные о перевале в приложение и отправлять их в ФСТР, как только появится доступ в Интернет.

Модератор из федерации будет верифицировать и вносить в базу данных информацию, полученную от пользователей, а те в свою очередь смогут увидеть в мобильном приложении статус модерации и просматривать базу с объектами, внесёнными другими.

**Требования к мобильному приложению и Rest API**
________________________________________
Для пользователя в мобильном приложении будут доступны следующие действия:
*	Внесение информации о новом объекте (перевале) в карточку объекта.
*	Редактирование в приложении неотправленных на сервер ФСТР данных об объектах. На перевале не всегда работает Интернет.
*	Заполнение ФИО и контактных данных (телефон и электронная почта) с последующим их автозаполнением при внесении данных о новых объектах.
*	Отправка данных на сервер ФСТР.
*	Получение уведомления о статусе отправки (успешно/неуспешно).
*	Согласие пользователя с политикой обработки персональных данных в случае нажатия на кнопку «Отправить» при отправке данных на сервер.

Пользователь с помощью мобильного приложения будет передавать в ФСТР следующие данные о перевале:
*	координаты перевала и его высота;
*	имя пользователя;
*	почта и телефон пользователя;
*	название перевала;
*	несколько фотографий перевала.

**Требования к Rest API**
________________________________________

**Метод POST submitData**
Когда турист поднимется на перевал, он сфотографирует его и внесёт нужную информацию с помощью мобильного приложения:

* координаты объекта и его высоту;
* название объекта;
* несколько фотографий;
* информацию о пользователе, который передал данные о перевале:
  + имя пользователя (ФИО строкой);
  + почта;
  + телефон.

После этого турист нажмёт кнопку «Отправить» в мобильном приложении. Мобильное приложение вызовет метод submitData твоего REST API.

Метод submitData принимает JSON в теле запроса с информацией о перевале. Ниже находится пример такого JSON-а:

```
{
  "beauty_title": "пер. ",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "", // что соединяет, текстовое поле
 
  "add_time": "2021-09-22 13:18:13",
  "user": {"email": "qwerty@mail.ru", 		
        "fam": "Пупкин",
		 "name": "Василий",
		 "otc": "Иванович",
        "phone": "+7 555 55 55"}, 
 
   "coords":{
  "latitude": "45.3842",
  "longitude": "7.1525",
  "height": "1200"}
 
 
  level:{"winter": "", //Категория трудности. В разное время года перевал может иметь разную категорию трудности
  "summer": "1А",
  "autumn": "1А",
  "spring": ""},
 
   images: [{data:"<картинка1>", title:"Седловина"}, {data:"<картинка>", title:"Подъём"}]
}
```

Результат метода: JSON

* status — код HTTP, целое число:
  + 500 — ошибка при выполнении операции;
  + 400 — Bad Request (при нехватке полей);
  + 200 — успех.
* message — строка:
  + Причина ошибки (если она была);
  + Отправлено успешно;
  + Если отправка успешна, дополнительно возвращается id вставленной записи.
* id — идентификатор, который был присвоен объекту при добавлении в базу данных.

Примеры:
```
{ "status": 500, "message": "Ошибка подключения к базе данных","id": null}
{ "status": 200, "message": null, "id": 42 }
```
*После того, как турист добавит в базу данных информацию о новом перевале, сотрудники ФСТР проведут модерацию для каждого нового объекта и поменяют поле status.*

***Допустимые значения поля status:***

+ *'new';*
+ *'pending' — модератор взял в работу;*
+ *'accepted'  — модерация прошла успешно;*
+ *'rejected' — модерация прошла, информация не принята.*
______

 ***Метод:*** 

```
POST /pereval
```
*добавление записи (перевала).*

______

 ***Метод:*** 

```
GET /pereval/<id>
```
*получает одну запись (перевал) по её id с выведением всей информацию об перевале, в том числе статус модерации.*

____
***Метод:***

```
PATCH /pereval/<id>
```

*позволяет отредактировать существующую запись (замена), при условии что она в статусе "new". При этом редактировать можно все поля, кроме тех, что содержат ФИО, адрес почты и номер телефона. В качестве результата изменения приходит ответ содержащий следующие данные:*

 *state:*
     *1 — если успешно удалось отредактировать запись в базе данных.*
     *0 — отредактировать запись не удалось.*
    
 *message: сообщение о причине неудачного обновления записи.*

_____
***Метод:***
   
```
GET /pereval/?user__email=<email>
```

*позволяет получить данные всех объектов, отправленных на сервер пользователем с почтой.* 

В качестве реализации использована фильтрация по адресу электронной почты пользователя с помощью пакета **django-filter**

______


***Документация сгенерирована с помощью пакета `drf-yasg`*** 

*Документация **swagger**: http://127.0.0.1:8000/swagger/*<br/>
*Документация **redoc**: http://127.0.0.1:8000/redoc/*

______


***Отчет о покрытии тестами:***
```
Name                                                                  Stmts   Miss  Cover
-----------------------------------------------------------------------------------------
fstr_project\__init__.py                                                  0      0   100%
fstr_project\asgi.py                                                      4      4     0%
fstr_project\settings.py                                                 28      0   100%
fstr_project\urls.py                                                      5      0   100%
fstr_project\wsgi.py                                                      4      4     0%
manage.py                                                                11      2    82%
pereval\__init__.py                                                       0      0   100%
pereval\admin.py                                                          7      0   100%
pereval\apps.py                                                           4      0   100%
pereval\migrations\0001_initial.py                                        6      0   100%
pereval\migrations\0002_remove_perevaluser_unique_email_and_more.py       4      0   100%
pereval\migrations\__init__.py                                            0      0   100%
pereval\models.py                                                        62      9    85%
pereval\resources.py                                                      3      0   100%
pereval\serializers.py                                                   77      0   100%
pereval\tests.py                                                         89      0   100%
pereval\urls.py                                                          10      0   100%
pereval\views.py                                                         64     11    83%
pereval\yasg.py                                                           6      0   100%
-----------------------------------------------------------------------------------------
TOTAL                                                                   384     30    92%
```
