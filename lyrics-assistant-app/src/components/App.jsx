import React, { useState, useEffect } from 'react'
import WritingSpace from './WritingSpace'
import Header from './Header'
import SentimentSelector from './SentimentSelector'
import Recommendations from './Recommendations'


export default class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            writing: false,
            timeout: null,
            sentiment: null,
            selectedVerse: 0,
            verses: [""],
            mostCommonWords: null,
            mostCommonBigrams: null,
            mostSimilarWords: null,
            nextBigrams: null,
        }
        this.write = this.write.bind(this)
        this.newVerse = this.newVerse.bind(this)
        this.selectSentiment = this.selectSentiment.bind(this)
        this.selectVerse = this.selectVerse.bind(this)
        this.call_api_sentiment = this.call_api_select_sentiment.bind(this)
    }

    componentDidMount(){
    }

    componentDidUpdate(){
        console.log('-------------------------------------')
        console.log('-------------------------------------')
        console.log("Current verse: ", this.state.selectedVerse)
        console.log("Current sentiment: ", this.state.sentiment)
        console.log("Verses: ", this.state.verses)
        console.log("mostCommonWords: ", this.state.mostCommonWords)
        console.log("mostCommonBigrams: ", this.state.mostCommonBigrams)
        console.log("mostSimilarWords: ", this.state.mostSimilarWords)
        console.log("nextBigrams: ", this.state.nextBigrams)
    }
    
    componentWillUpdate(){

        

    }

    async call_api_select_sentiment(sentiment) {
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

    async call_api_recommend_from_text(text){
        const response = await fetch("/recommend_from_text", {
            method: "POST",
            headers: {
              "Content_Type": "application/json"
            },
            body:
              JSON.stringify({
                sentiment: this.state.sentiment,
                user_input: this.state.verses[this.state.selectedVerse]
              })
            })
        if(response.ok) {
            response.json().then(data => {
                this.setState({
                    mostSimilarWords: data.most_similar_words,
                    nextBigrams: data.next_bigrams
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

        clearTimeout(this.timeout)

        this.timeout = setTimeout(async () => {
            this.call_api_recommend_from_text(text)
        },2000)

        //this.timeout = t
    }

    selectSentiment(sentiment){
        this.setState({
            sentiment: sentiment
        })
        this.call_api_select_sentiment(sentiment).then()
    }

    selectVerse(number) {
        this.setState({
            selectedVerse: number
        })

    }

    newVerse(){
        let copyVerses = this.state.verses
        copyVerses.push("")
        this.setState({
            verses: copyVerses
        })
    }

    //TODO renders twice
    render() {
        let text = "Welcome to the lyrics assistant app!"
        return(
            <div>
                <Header text = {text} />
                <SentimentSelector selectSentiment={this.selectSentiment} />
                <WritingSpace
                    verses={this.state.verses} 
                    selected={this.state.selectedVerse}
                    write={this.write}
                    selectVerse = {this.selectVerse}
                    newVerse={this.newVerse}
                />
                <Recommendations 
                    mostCommonWords={this.state.mostCommonWords}
                    mostCommonBigrams={this.state.mostCommonBigrams}
                    mostSimilarWords={this.state.mostSimilarWords}
                    nextBigrams={this.state.nextBigrams}
                />
            </div>
        )
    }
}