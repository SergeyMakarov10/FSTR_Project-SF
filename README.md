# FSTR-Project---Skillfactory
**Как заказчик хочет решить эту проблему**
________________________________________
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