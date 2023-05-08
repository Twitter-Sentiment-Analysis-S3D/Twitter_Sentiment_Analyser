# Twitter_Sentiment_Analyser
This is a web app which can be used to analyze users' sentiments across Twitter hashtags/terms. It is created using React and Django and uses an CNN model trained on the Kaggle Sentiment140 dataset and served as a REST API to the ReactJS frontend.
The server pulls tweets using tweepy and performs inference using Keras. It also pulls data from the Wikipedia API based the hashtag chosen to display a short description.
As for now tweets are retrieved from twitter user datasets and text emotion datasets for the working of our app.
