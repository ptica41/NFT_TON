## Для запуска selenium на сервере ubuntu или debian без графического интерфейса, скачиваем последнею версию браузера Chrome
`
wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
`
## устанавливаем браузер
`
sudo apt install -f ./google-chrome-stable_current_amd64.deb
`
## устанавливаем selenium и webdriver-manager
`
python3.11 -m pip install selenium webdriver-manager
`
## устанавливаем зависимости
`
python3.11 -m pip install -r requirements.txt
`
## запускаем проект
`
python3.11 main.py
`
