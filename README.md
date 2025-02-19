# Whisper demo

## Get started

### Docker

Build container:

```bash
docker build -t whisper-demo .
```

Run container:

```bash
docker run --rm -v "$(pwd)/assets:/assets" -v "$(pwd)/models:/models" -p 3000:80 whisper-demo
```

**The whisper model will be loaded on first bootup**

The API will be available on http://localhost:3000/docs

### Local env

Create python env:

```bash
python3 -m venv env
```

Activate env:

```bash
source env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Jupyter extension:
https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter 

Select venv as Python kernel:
![alt text](docs/image.png)

Run notebook!