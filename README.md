<h1>Сервис на FastAPI для конвертации файлов</h1>

<p>Данный проект представляет собой сервис на базе FastAPI, предоставляющий API для регистрации пользователей, управления файлами и конвертации данных.</p>

<h2>Установка и запуск</h2>

<ol>
    <li>Клонируйте репозиторий:
        <pre><code>git clone https://github.com/KLYMENKORUS/Convert_to_pdf.git</code></pre>
    </li>
    <li>Запустите команду:
        <pre><code>docker-compose up -d --build</code></pre>
    </li>
</ol>

<h2>Методы API</h2>

<h3>Регистрация пользователя</h3>

<pre><code>POST user/register</code></pre>

<p>Регистрация нового пользователя. Отправьте POST запрос с JSON данными:</p>

<pre><code>{
  "username": "string",
  "email": "user@example.com",
  "password": "string"
}</code></pre>

<h3>Получение токена для входа</h3>

<pre><code>POST user/login</code></pre>

<p>Авторизация пользователя. Отправьте POST запрос с query параметрами:</p>

<pre><code>{
  "username": "your_username",
  "password": "your_password"
}</code></pre>

<h3>Добавление нового файла для конвертации</h3>

<pre><code>POST file/add?format_file{format_file}</code></pre>

<p>Загрузка нового файла на сервер для конвертации без регистрации. Передайте файл в формате <code>multipart/form-data</code>.</p>

<pre><code>POST file/add?format_file{format_file}&username={username}</code></pre>

<p>Загрузка нового файла на сервер для конвертации для зарегистрированных пользователей. Передайте файл в формате <code>multipart/form-data</code>.</p>

<h3>Получение файла</h3>

<pre><code>GET file/get?filename={filename}</code></pre>

<p>Получение конвертированного файла по его названию без формата.
Данный GET запрос будет выдавать конвертированный файл для не зарегистрированных пользователей</p>

<pre><code>GET file/get?filename{filename}&username{username}</code></pre>

<p>Получение конвертированного файла по его названию без формата.
Данный GET запрос будет выдавать конвертированный файл для зарегистрированных пользователей</p>

<h3>Получение всех файлов текущего пользователя</h3>

<pre><code>GET file/all</code></pre>

<p>Получение списка всех файлов, загруженных текущим пользователем.</p>

<h3>Удаление файла</h3>

<pre><code>DELETE file/delete?{filename}</code></pre>

<p>Удаление файла по его названию</p>

<h2>Примеры использования</h2>

<p>Примеры использования методов API можно найти в файле <a href="examples.md">examples.md</a>.</p>

<h2>Автор</h2>

<p>Ruslan</p>
