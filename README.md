# Text-chat
	
	src/ChatServer.py [addres port] - сервер, в качестве необязательных параметров принимает адрес и порт.
	По умолчанию "localhost" и 9090. На других параметрах адреса не тестировалось, но думаю работать должно.
	К серверу могут подключаться до 15 пользователей, сервер работает с данными длинной до 1024 символов (при получении
	данных большей длины обрезает их до 1024). Протокол обмена UDP
	
	src/ChatClient.py [addres port] - клиент, в параметрах принимает адрес и порт сервера, значения по умолчанию
	идентичны параметрам сервера
	
	Комманды чата:
		:exit - Выход из чата. Серверу посылается сообщение о выходе
		:members - вывод всех онлайн пользователей в чате.
	
	src/other/localchat - крайне сырая (но работающая) версия чата, реализованного без сервера, на основе широковещательной
	рассылки
	
	
	ТЗ:
	Live chat application. Please create a simple application "Text chat" using Python as primary development tool
	(without an additional packages, only common pack). Requirements: should work on Windows without an additional
	configuration; chat should have at least two active members; GUI not required. Input data: user name or ID. Output
	data: chat console. Desirable to provide your results (code base) using Git.