# Twitter-Sentiment-Analysis-Web-App

<br>

![App](imgs/demo.gif)

This is a web app which can be used to **analyze users' sentiments across Twitter hashtags/terms**. Its created using React and Django and uses an LSTM model trained on the [Kaggle Sentiment140 dataset](https://www.kaggle.com/kazanova/sentiment140) and served as a REST API to the ReactJS frontend.

The server pulls tweets using **tweepy** and performs inference using Keras. It also pulls data from the **Wikipedia API** based the hashtag chosen to display a short description. As part of the analysis, I also added few examples of the tweets and their predicted sentiments. A kernel for another sentiment classification using a CNN + 1D pooling can be found [here](https://www.kaggle.com/thatawkwardguy/twitter-sentiment-classification-using-cnns)

![Untitled Diagram (6)](https://user-images.githubusercontent.com/29514438/59569258-5f55b700-90a4-11e9-8167-60f53a765c02.jpg)

## How to Use

### Running the application

1. Download the [trained model](https://drive.google.com/file/d/1ckK5m4JysFKtBuC9yCnEaHe6cxOgXlG8/view?usp=sharing) and put into the `server/main` folder <br>(**Note:** _This is the CNN model. Also, don't forget to change the loaded model name in `server/main/init.py`_ )
2. Get your Twitter API **"Bearer Token"** through Keys and Tokens tab under the [Twitter Developer Portal Projects & Apps page](https://developer.twitter.com/en/portal/projects-and-apps) and add it to the `/server/main/config.py` file.
3. Run `docker-compose up --build` in the terminal from the root folder <br> (**Note:** _Ensure that you have Docker installed_)

4. Open `http://localhost:3000` in your browser to access the app

### Training the model

_(Note: If you have a GPU in your system, We suggest that you train the CNN model.

#### CNN Model

1. Copy and run the [Kaggle Notebook](https://www.kaggle.com/thatawkwardguy/twitter-sentiment-classification-using-cnns).

