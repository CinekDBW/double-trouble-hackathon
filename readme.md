# Hello it's us, Double Trouble 😎🔥

In this repo you can find our implementations of the tasks on BEST Hackathon 2022

## Contributors
Our team consists of 3 people:
* @[Ciniaq](https://github.com/Ciniaq)
* @[Percival33](https://github.com/Percival33)
* @[CinekDBW](https://github.com/CinekDBW)



# Task 2


### Installation
1. Run `pip install -r zad2/requirements.txt` to install necessary packages
2. Download tesseract.exe from this [link](https://github.com/UB-Mannheim/tesseract/wiki)
3. Install this exe, make sure it has installed itself in `C:\Program Files\Tesseract- OCR`
4. Copy and paste `pol.traineddata` to `C:\Program Files\Tesseract-OCR\tessdata\`
5. Everything should work now!


### running task 2
1. Simply clone the whole repo
2. Run `pip install -r zad2/requirements.txt` to install necessary packages
3. Paste input pictures in the `/input` directory
4. In the main.py file change the filename in `line 71` and run `main.py`
5. Voilà! Answers are placed in the `/outputs` directory


### Usage

```python
#before running main.py, make sure to change path in line 71
#71 path = 'input/' + your_file_name
python3 main.py

```

## License
[MIT](https://choosealicense.com/licenses/mit/)
