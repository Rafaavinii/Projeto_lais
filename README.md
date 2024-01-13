# Projeto_lais

### Arquitetura

* Linguagem: Python
* Framework: Django

### 📋 Pré-requisitos

Para instalação do software é necessário:
* Python 3.10
* Django 4.1.7
* requests 2.31.0


### 🔧 Instalação

1. Clone o repositório:
```
> git clone https://github.com/Rafaavinii/Projeto_lais.git
```
2. Instale a virtual env:
```
> python -m venv ven
```
3. Ative a venv:
3.1 Windows:
```
> venv\Scripts\activate
```
3.2 Linux:
```
source nome_da_sua_venv/bin/activate
```

4. Instale as dependências:
```
> pip install -r requirements.txt
```

5. Execute as migrações:
```
> python manage.py makemigrations
> python manage.py migrate
```

6. Execute o servidor:
```
> python manage.py runserver
```
