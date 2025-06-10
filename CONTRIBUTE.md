# Contribute

First things first, make sure you follow the `README.md` file’s instructions.

## Installing backend dependencies

**Note: this guide is only valuable for Linux. A guide for Windows contributors shall be written in the near future.**

For now (this might change in the future) we are told to install dependencies
without creating a python virtual environment.

Creating a virtual environment let us install dependencies without overriding
the ones set up on our system.

To quickly set up a virtual environment, navigate to the `laz_verb_conjugator/backend`
folder and execute this command:

```bash
python -m virtualenv venv
```

This will create a `venv` folder, storing our files for the python’s virtual environment.
If you are not familiar with it, think of it to be the equivalent to the `node_modules` folder for the frontend project (or any Javascript project, actually). You don’t want to track this folder. The same rules apply to the `venv` folder.

There is one extra command to run, though. Everytime you work on the backend, make sure you
execute (while you are in):

```bash
laz_verb_conjugator/backend$
source venv/bin/activate
```

You should then see a `(venv)` label at the beginning of your command prompt: congratulations! You’ve enabled your virtualenv.

You can then install the dependencies as stated in the `README.md` file:

```python
pip install -r requirements.txt
```