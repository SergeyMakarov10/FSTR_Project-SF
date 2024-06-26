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

______

 ***Метод:*** 

```
POST /pereval
```
*добавление записи (перевала).*

Принимает JSON в теле запроса с информацией о перевале. Ниже находится пример такого JSON-а:

```
{
    "beauty_title": "Перевал",
    "title": "Большой перевал",
    "other_title": "Малый перевал",
    "connect": "Соединяет долины",
    "status": "new",
    "user": {
        "surname": "Петров",
        "name": "Иван",
        "otc": "Сергеевич",
        "email": "test2@example.com",
        "phone": "1234567890"
    },
    "coord": {
        "latitude": 99.0,
        "longitude": 99.0,
        "height": 2700
    },
    "level": {
        "winter": "1a",
        "summer": "1b",
        "autumn": "2a",
        "spring": "2b"
    },
    "images": [
{
"title":"Виднаперевал",
"data":"http://example.com/image.jpg"
}
]
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
