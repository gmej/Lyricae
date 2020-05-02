import React from 'react'
import WritingSpace from './WritingSpace'
import Header from './Header'
import SentimentSelector from './SentimentSelector'
import Recommendations from './Recommendations'

import '../assets/styles/App.css'


export default class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            timeoutTime: 0.5*1000,
            writing: false,
            timeout: null,
            selectedVerse: 0,
            sentiment: "happy",
            verses: [""],
            mostCommonWords: null,
            mostCommonBigrams: null,
            mostSimilarWords: null,
            nextNBigrams: null,
            nSimilarWords: 7,
            nNextBigrams: 3,
        }
        this.write = this.write.bind(this)
        this.newVerse = this.newVerse.bind(this)
        this.selectSentiment = this.selectSentiment.bind(this)
        this.selectVerse = this.selectVerse.bind(this)
        this.call_api_sentiment = this.callApiSelectSentiment.bind(this)
        this.selectNSimilarWords = this.selectNSimilarWords.bind(this)
        this.selectNBigramsRecommendations = this.selectNBigramsRecommendations.bind(this)
        this.onWordClick = this.onWordClick.bind(this)
    }

    componentDidUpdate(){/* 
        console.log('-------------------------------------')
        console.log("mostCommonWords: ", this.state.mostCommonWords)
        console.log("mostCommonBigrams: ", this.state.mostCommonBigrams)
        console.log("mostSimilarWords: ", this.state.mostSimilarWords)
        console.log("nextNBigrams: ", this.state.nextNBigrams)
        console.log('-------------------------------------')
        console.log("sentiment: ", this.state.sentiment)
        console.log("nSimilarWords: ", this.state.nSimilarWords)
        console.log("nNextBigrams: ", this.state.nNextBigrams)
        console.log("nextBigrams: ", this.state.nextBigrams) */
    }

    async callApi() {
        clearTimeout(this.timeout)

        this.timeout = setTimeout(async () => {
            this.callApiSelectSentiment(this.state.sentiment)
            this.callApiRecommendFromText(this.state.verses[this.state.selectedVerse], this.state.nSimilarWords, this.state.nextNBigrams)
        },this.state.timeoutTime)


    }

    async callApiSelectSentiment(sentiment) {
        if(sentiment == undefined) {
            sentiment=this.state.sentiment
        }

            const response = await fetch("/select_sentiment", {
                method: "POST",
                headers: {
                "Content_Type": "application/json"
                },
                body:
                JSON.stringify({
                    sentiment: sentiment,
                })
            })
            if(response.ok) {
                response.json().then(data => {
                    this.setState({
                        mostCommonWords: data.most_common_words,
                        mostCommonBigrams: data.most_common_bigrams
                    })
                })
            }
    }

    async callApiRecommendFromText(text, nSimilarWords, nNextBigrams){
        if(text == undefined) {
            text=this.state.text
        }
        if(nSimilarWords == undefined) {
            nSimilarWords=this.state.nSimilarWords
        }
        if(nNextBigrams == undefined) {
            nNextBigrams=this.state.nNextBigrams
        }

            const response = await fetch("/recommend_from_text", {
                method: "POST",
                headers: {
                "Content_Type": "application/json"
                },
                body:
                JSON.stringify({
                    sentiment: this.state.sentiment,
                    user_input: this.state.verses[this.state.selectedVerse],
                    n_similar_words: this.state.nSimilarWords,
                    n_next_bigrams: this.state.nNextBigrams,
                })
                })
            if(response.ok) {
                response.json().then(data => {
                    this.setState({
                        mostSimilarWords: data.most_similar_words,
                        nextNBigrams: data.next_bigrams
                    })
                })
            }
    }

    write(text) {
        let copyVerses = this.state.verses
        copyVerses[this.state.selectedVerse] = text
        this.setState({
            verses: copyVerses
        })
        this.callApi()
    }

    selectSentiment(sentiment){
        this.setState({
            sentiment: sentiment
        })
        this.callApi()
    }

    selectVerse(number) {
        this.setState({
            selectedVerse: number
        })
        this.callApi()
    }


    selectNSimilarWords(n) {
        this.setState({
            nSimilarWords:n
        })
        this.callApi()
    }

    selectNBigramsRecommendations(n) {
        this.setState({
            nNextBigrams:n
        })
        this.callApi()
    }

    newVerse(){
        let copyVerses = this.state.verses
        copyVerses.push("")
        let selected = copyVerses.length-1
        this.setState({
            verses: copyVerses,
            selectedVerse: copyVerses.length-1
        })
        this.callApi()
    }


    onWordClick(word){
        let copyVerses = this.state.verses
        let currentVerse = copyVerses[this.state.selectedVerse].trim()
        let newVerse = ""
        if(currentVerse.length == 0){
            newVerse = word
        } else {
            newVerse = currentVerse + " " + word
        }
        copyVerses[this.state.selectedVerse] = newVerse
        this.setState({
            verses: copyVerses
        })
        this.callApi()
    }
    //TODO renders twice
    render() {
        return(
            <div className="general">
                <Header/>
                <div className="myApp">
                    <div className="input">
                        <SentimentSelector selectSentiment={this.selectSentiment} />
                        <WritingSpace
                            verses={this.state.verses} 
                            selected={this.state.selectedVerse}
                            write={this.write}
                            selectVerse = {this.selectVerse}
                            newVerse={this.newVerse}
                            />
                    </div>
                        <Recommendations 
                            sentiment={this.state.sentiment}
                            mostCommonWords={this.state.mostCommonWords}
                            mostCommonBigrams={this.state.mostCommonBigrams}
                            mostSimilarWords={this.state.mostSimilarWords}
                            nextNBigrams={this.state.nextNBigrams}
                            selectNSimilarWords={this.selectNSimilarWords}
                            selectNBigramsRecommendations={this.selectNBigramsRecommendations}
                            onWordClick={this.onWordClick}
                            />
                    </div>
                </div>
        )
    }
}