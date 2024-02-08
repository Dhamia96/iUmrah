# iUmrah chatbot

Welcome to the iUmrah project repository! This project aims to guide and assist Muslims during their Umrah pilgrimage.

## Setup Instructions

Before running the `chatbot.py` file, please follow these steps:

1. **Create a new OpenAI account** by clicking on the [Log in button: OpenAI](https://openai.com/).
2. On the left side, click on **API Key: API Key**.
3. Click on **Create a new secret key**, enter a name for the key, copy the generated key, and save it in a safe place. Note that you won't be able to display this key again once you leave this page.
4. **Install Python** on your machine from the official Python website: [Python Downloads](https://www.python.org/downloads/).
5. *(Optional)* Create a new **virtual environment** to install your packages. If you are using Windows, follow these steps:
   - Open the command prompt by pressing Win + R and typing `cmd`, then press Enter.
   - Navigate to the directory where you want to create your virtual environment.
   - Once inside the desired directory, run the following command to create a new virtual environment using `venv`:
     ```
     python -m venv myenv
     ```
     Replace `myenv` with the desired name for your virtual environment.
   - Activate the newly created virtual environment by running the following command:
     ```
     myenv\Scripts\activate
     ```
6. Install the packages listed in the `requirements.txt` file using the following command:
     ```
     pip install -r requirements.txt
     ```
7. Inside your code editor, create a new `.env` file and put your generated key inside it:
     ```
     OPENAI_API_KEY="put your key here"
     ```
8. Now you can run and render the app using Streamlit by typing the following command:
     ```
     streamlit run chatbot.py
     ```
Feel free to reach out if you have any further questions or issues!




