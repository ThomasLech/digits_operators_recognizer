## Installation
1. Install Python 3.5.0 (for tensorflow/tensorflow-gpu windows compatibility):
 <br/>[Windows x86-64 web-based installer](https://www.python.org/ftp/python/3.5.0/python-3.5.0-amd64-webinstall.exe) or [Select & download other installer](https://www.python.org/downloads/release/python-350/).
 <br/><br/>While installing Python please make sure that option 'Add Pytohn 3.5 to PATH' is checked.

2. Install virtuenv package:  
`pip install virtualenv`

3. Create new directory and enter it:  
`mkdir digits_operators_recognizer`

4. Enter newly created directory:  
`cd digits_operators_recognizer`

5. Clone **this repository** into current directory:  
`git clone https://github.com/ThomasLech/digits_operators_recognizer .`

6. Create isolated working copy of Python:  
`virtualenv env`

7. Acivate virtual enviroment:  
`source env/Scripts/activate` (on Windows: `env\Scripts\activate`)



8. Download missing packages (those that **cannot** be installed via pip):
 <br/>_scipy‑0.19.0‑cp35‑cp35m‑win_amd64.whl:_ [SciPy Download Page](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy),
 <br/>_scikit_image-0.13.0-cp35-cp35m-win_amd64.whl:_ [Scikit-image Download Page](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scikit-image),
 <br/>_numpy-1.12.1+mkl-cp35-cp35m-win_amd64.whl:_ [NumPy Download Page](http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy).

9. Upgrade pip (Python Package Manager) and install three downloaded packages with the following shell command:
```
python -m pip install --upgrade pip

pip install "scikit_image-0.13.0-cp35-cp35m-win_amd64.whl"
pip install "scipy-0.19.1-cp35-cp35m-win_amd64.whl"
pip install "numpy-1.13.1+mkl-cp35-cp35m-win_amd64.whl"
```

10. Install specified dependencies with pip (Python Package Manager) with the following shell command:
```
pip install -U -r requirements.txt
```


## Usage
Navigate to folder with **_run.py_** & run OCR algorithm with following command:
```
python run.py <files/folders>
```
