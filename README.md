To install:
1. Clone this repository
2. Download the [models](https://drive.google.com/drive/folders/1-oGWdh5Zbl9bF_BpyXd__beJRAiyg-Ug?usp=sharing) and put them on the resources directory
3. `gunicorn -b 0.0.0.0:5000 --limit-request-line 0 app:app --daemon`