Clone the repository 

Navigate into the project directory

navigate into the frontend folder:

```bash
cd frontend
```

install required dependencies:

```bash
npm install
```
build the static files

```bash
npm run build
```

navigate to backend folder:

```bash
cd ..
cd backend
```

install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

start the flask server by running the command:

```bash
python app.py
```

After running the command, head to the `frontend` folder to run the frontend:

```bash
cd ..
cd frontend
npm run dev

[…]
  ➜  Local:   http://localhost:5173/
  ➜  Network: http://10.255.255.254:5173/
  ➜  Network: http://172.19.113.104:5173/
[…]
```

You are now ready to explore the conjugator on http://localhost:5173/.