# Lyricae

Lyricae is an assistant tool for composing lyrics by making recommendations based on sentiment selected and the verses written by the user. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. The project consists in two fundamental parts: first lyrics scraping and processing to create the dataframes for the recommendation system, and the application itself.

See deployment for notes on how to deploy the project on a live system.

### Prerequisites

For the live application it is required Python 3.7 or higher, and nodeJS v12.18.0

In order to create the database, you will only need Python 3.7.

#### Linux prerequisites

Run this commands to install python 3 and nodeJS:

```
$ sudo apt-get update
$ sudo apt-get install python3.7
$ sudo apt-get install nodejs
$ sudo apt-get install npm
```

The project was developed in the specified versions , and it has not been tested with previous versions in which it might work as well.

### Installing

First of all, install python requirements and npm packages:

```
pip install -r requirements.txt
cd app
npm install
```

#### Application

NOTE: See deployment to k.now how to get the application deployed with docker. This application runs currently on a development server.

1. Run the API:

```
cd app
export FLASK_APP=api.py
npm run start-api
```

2. Run the web server:

```
cd app
npm start
```

If ypu get the error "System limit for number of file watchers reached", run the next command before starting the web server:

```
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
```

#### Database creation

NOTE: These scripts take some minutes to finish.


1. DOWNLOAD LYRICS: Run "donwload_lyrics.py" to automatically donwload all the songs of the .csv file in the folder "/lyrics_dataset". This lyrics will be downloaded to "/lyrics_lyricwikia":

```
python donwload_lyrics.py
```

2. PROCESS LYRICS: Run "process_lyrics.py" to process the lyrics and create the dataset for the recommendation engine:

```
python process_lyrics.py
```

3. POSTPROCESS LYRICS: Run "postprocess.py" to filter words in other languages other than English, as some of them are in Spanish:

```
python postprocess.py
```

3. WORD SIMILARITIES: You need to donwload the Word2Vec model to "Word2Vec" directory to be able to run either "KeyedVectors.py" or the notebook "KeyedVectors.ipynb". This script calculates similarities between words in the dataframes created previously:

```
python KeyedVectors.py
```




<!-- 

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc

-->