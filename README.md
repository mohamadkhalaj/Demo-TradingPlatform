# Demo Trading

Advanced cryptocurrencies demo trading platform.

[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![.github/workflows/production.yml](https://github.com/mohamadkhalaj/Demo-TradingPlatform/actions/workflows/production.yml/badge.svg)](https://github.com/mohamadkhalaj/Demo-TradingPlatform/actions/workflows/production.yml)

## Features✨

### Market:
- real-time price
- search any cryptocurrency!

### Trade:
- spot trading
- limit-order trading
- recent trades(Live)
- all trade histories
- all open orders
- cancel open orders

### Portfolio:
- account available margin
- account total margin
- PNL chart
- asset allocation chart

### Trade history
- all trade histories

### Open orders:
- all open orders
- cancel orders

### Profile:
- gravatar profile photo
- edit name and last name
- change password
- view email and username

## Tech

All used frameworks, technologies and libraries:

- [Django] - We use django for our backend
- [Redis] - Datebase memory caching and message broker
- [PostgreSql] - Sql datebase
- [JavaScript] - Our frontEnd made with pure js
- [jQuery] - FrontEnd
- [Twitter Bootstrap] - Great UI boilerplate for modern and responsive web apps
- [Heroku] - Deployment
- [Sentry] - Error tracking for both Django/JS
- [Google analytics] - For users analysis
- [Celery] - task schedule
- [Docker] - container
- [Django channels] - socket programming

## Docker

`$ docker-compose up --build`

## Setting Up Super User

-   To create a **superuser account**, use this command:

        $ python manage.py createsuperuser

## Local running
First you should change directory to web:</br>
```$ cd web```</br>
```$ cp .env-sample .env``` and paste variables with your own.</br>
```$ pip install -r requirements/local.txt```</br>
```$ chmod +x ./release.sh && ./release.sh```</br>
```$ python manage.py collectstatic```</br>
```$ python -m celery -A config worker -l info -c 4```</br>
in another console run:</br>
```$ python manage.py runserver```</br>

## Running in Production

Set this environment variables
| KEY | VALUE |
| ------ | ------ |
| DJANGO_SECRET_KEY | ```$(openssl rand -base64 64)``` |
| WEB_CONCURRENCY | 4 |
| DJANGO_DEBUG | False |
| DJANGO_SETTINGS_MODULE | config.settings.production |
| PYTHONHASHSEED | random |
| DJANGO_ALLOWED_HOSTS | YOUR_DOMAIN |
| DJANGO_ADMIN_URL | RANDOM_STRING/ |
| CRYPTO_COMPARE_API | [Get it from here](https://min-api.cryptocompare.com/) |
| EMAIL_HOST_USER | Email username|
| EMAIL_HOST_PASSWORD | Email password |
| SOCIAL_AUTH_GOOGLE_OAUTH2_KEY | [Get it from here](https://developers.google.com/identity/protocols/oauth2) |
| SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET | Secret from above |
| HCAPTCHA_SITEKEY | [Login and create new site](https://dashboard.hcaptcha.com/overview) |
| HCAPTCHA_SECRET | Copy secret from above url |
| SENTRY_DSN | [Follow this instruction](https://docs.sentry.io/platforms/python/guides/django/) |

```
$ cd web
$ pip install -r requirements.txt
$ chmod +x ./release.sh && ./release.sh
$ python manage.py collectstatic
$ python -m celery -A config worker -l info -c 4
$ daphne -b 0.0.0.0 -p $PORT config.routing:application
```

## Github workflows (CI/CD)

If you want to pass ci/cd and auto deploy after each commit, you should add below secrets to your github repo secret lists.

| KEY | VALUE |
| ------ | ------ |
| CRYPTO_COMPARE_API | [Get it from here](https://min-api.cryptocompare.com/) |
| EMAIL_HOST_USER | Email username|
| EMAIL_HOST_PASSWORD | Email password |
| SOCIAL_AUTH_GOOGLE_OAUTH2_KEY | [Get it from here](https://developers.google.com/identity/protocols/oauth2) |
| SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET | Secret from above |
| HCAPTCHA_SITEKEY | [Login and create new site](https://dashboard.hcaptcha.com/overview) |
| HCAPTCHA_SECRET | Copy secret from above url |
| SENTRY_DSN | [Follow this instruction](https://docs.sentry.io/platforms/python/guides/django/) |
| HEROKU_API_KEY | Your API key |
| HEROKU_APP_NAME | Your app name to be deployed here |
| HEROKU_EMAIL | Your email address related to your heroku account |

## Celery
```
$ cd web
$ python3 -m celery -A config worker -l info -c 4
```

## License

GPL-3.0 license

## Screenshots
![Screenshot 2022-09-05 at 15-26-03 Exchange Wallet](https://user-images.githubusercontent.com/62938359/188433585-8ab502a4-94f9-48a6-871c-6c42f848e612.png)
![Screenshot 2022-09-05 at 15-21-11 Exchange Settings](https://user-images.githubusercontent.com/62938359/188433609-c297c02b-aefa-4bcb-aa79-3e0e6f8e3658.png)
![Screenshot 2022-09-05 at 15-20-21 Exchange Trade BTC](https://user-images.githubusercontent.com/62938359/188433615-863f84b1-c8ac-491d-9bea-94b43bc94058.png)
![Screenshot 2022-09-05 at 15-19-38 Exchange Trade BTC](https://user-images.githubusercontent.com/62938359/188433624-d67e728f-4496-4ad1-bf7a-c6802389ea61.png)
![Screenshot 2022-09-05 at 15-18-40 Exchange Settings](https://user-images.githubusercontent.com/62938359/188433635-ee435b93-0113-40b8-af66-450dc6ae96cf.png)
![Screenshot 2022-09-05 at 15-18-08 Exchange profile](https://user-images.githubusercontent.com/62938359/188433646-daaeb262-20cb-4280-ba07-c3378750c183.png)
![Screenshot 2022-09-05 at 15-17-23 Exchange Home](https://user-images.githubusercontent.com/62938359/188433651-6833302d-36e6-438d-a7ef-a4d98298e2e7.png)
![Screenshot 2022-09-05 at 15-16-32 Exchange Reset Password](https://user-images.githubusercontent.com/62938359/188433671-9d6a0fb2-649c-4882-a78a-77355d7765be.png)
![Screenshot 2022-09-05 at 15-16-23 Exchange Sign up](https://user-images.githubusercontent.com/62938359/188433676-aad84479-6689-4fdb-9ce9-208c7b764ce4.png)
![Screenshot 2022-09-05 at 15-15-48 Exchange Login](https://user-images.githubusercontent.com/62938359/188433681-3310b522-02ad-4eee-a17a-a5025073407d.png)
![Screenshot 2022-09-05 at 15-15-28 Exchange Markets Info](https://user-images.githubusercontent.com/62938359/188433687-fe7ea394-921e-43e9-b226-b95bf089e797.png)
![Screenshot 2022-09-05 at 15-14-38 Exchange Markets Info](https://user-images.githubusercontent.com/62938359/188433707-d39949f0-af1c-48f3-9f54-6f391f120c4c.png)
![Screenshot 2022-09-05 at 15-14-05 Exchange Home](https://user-images.githubusercontent.com/62938359/188433717-d9ccf572-cbaf-4640-988a-6c6df087faa2.png)

