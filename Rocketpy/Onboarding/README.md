<!-- Ctrl + Shift + V to read -->
# RocketPy Onboarding

## Set up

1. Create a folder (e.g. C:\UTAT)

2. Download the files into the folder:
    - `drag.csv`
    - `airfoil.csv`
    - `thrust.csv`
    - `Onboarding.ipynb`

3. Download [Python 3.10+](https://www.python.org/downloads/) and [Visual Studio Code](https://code.visualstudio.com/download)

4. Open Visual Studio Code, go to File > Open Folder... , and select the folder created previously

5. Create a virtual environment
    - Recommended way:

        - Press Ctrl + Shift + P and select `Python: Create Environment...`

        - Select Venv and your Python executable

        - Go to Terminal > New Terminal (or Ctrl + Shift + P and select `Terminal: Create New Terminal`)

        - Check the new venv with:

            ```
            pip list
            ```

            You should only see something like

            ```
            Package Version
            ------- -------
            pip     version
            ```

            If not, try running:

            ```
            .venv/Scripts/Activate.ps1
            ```

            If it returns an error saying running scripts is disabled on this system. Open PowwerShell as administrator and run:

            ```
            Get-ExecutionPolicy
            ```

            If it returns `Restricted`, run the following code and try activating the virtual environment again:

            ```
            Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
            ```

6. Install RocketPy:

    ```
    pip install rocketpy
    ```

7. Open `Onboarding.ipynb` and have fun!


