<a href="http://www.djangoproject.com/"><img src="https://www.djangoproject.com/m/img/badges/djangopowered126x54.gif" border="0" alt="Powered by Django." title="Powered by Django." /></a>
 [![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/license-mit.svg)](https://forthebadge.com)

# TimeTracker
Manage your time by tracking your **working sessions** manually and by **label**, for personal improvement.

Only in Django admin's page.
## Features

- Create a working **day** with a time target (7h by default).
- Create **labels** for your **work sessions** like : "Dev", "Prospecting", "Support" or simply "project 1", "project 2" ...
- Create a **working session** with the **day**, **start time** and **label**, complete **end time** at finished session.
- Each **week's goal** is automatically calculated on the basis of the sum of the **daily goals** in the week.
- Each **week's working time** is automatically calculated on the basis of the sum of all the **working sessions** in the week.
- Each **week** displays the time **surplus** or **deficit**, based on the **week's goal** compared with the **week's working time**. 
- Each **week** displays the proportional distribution of **time** by **label**.

---

## Local Install

### Pre-requisites
**Linux** OS with **Python 3.11** installed

<br/>

### Local
Execute these commands in a **bash** terminal to install the project
```bash
git clone git@github.com:Jeremie-Silva/TimeTracker.git
cd TimeTracker
```

```bash
virtualenv -p3.11 .venv
source .venv/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt
```

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

You may need this command :
```bash
python manage.py collectstatic
```
