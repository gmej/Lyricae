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
            selectedVerse: 0,
            verses: [""],
            mostCommonWords: null,
            mostCommonBigrams: null,
            mostSimilarWords: null,
            nextNBigrams: null,
            sentiment: "happy",
            nBigrams: 7,
            nWords: 7,
            nSimilarWords: 7,
            nNextBigrams: 3,
        }
        this.write = this.write.bind(this)
        this.newVerse = this.newVerse.bind(this)
        this.selectSentiment = this.selectSentiment.bind(this)
        this.selectVerse = this.selectVerse.bind(this)
        this.call_api_sentiment = this.call_api_select_sentiment.bind(this)
        this.selectNBigrams = this.selectNBigrams.bind(this)
        this.selectNWords = this.selectNWords.bind(this)
        this.selectNSimilarWords = this.selectNSimilarWords.bind(this)
        this.selectNBigramsRecommendations = this.selectNBigramsRecommendations.bind(this)
    }

    componentDidMount(){
    }

    componentDidUpdate(){
        console.log('-------------------------------------')
        console.log('-------------------------------------')
        console.log("nBigrams: ", this.state.nBigrams)
        console.log("nWords: ", this.state.nWords)
        console.log("nSimilarWords: ", this.state.nSimilarWords)
        console.log("nNextBigrams: ", this.state.nNextBigrams)
        console.log("mostSimilarWords: ", this.state.mostSimilarWords)
        console.log("nextBigrams: ", this.state.nextBigrams)
    }
    
    componentWillUpdate(){

        

    }

    async call_api_select_sentiment(sentiment, nWords, nBigrams) {
        if(sentiment == undefined) {
            sentiment=this.state.sentiment
        }
        if(nWords == undefined) {
            nWords=this.state.nWords
        }
        if(nBigrams == undefined) {
            nBigrams=this.state.nBigrams
        }

        const response = await fetch("/select_sentiment", {
            method: "POST",
            headers: {
              "Content_Type": "application/json"
            },
            body:
              JSON.stringify({
                  sentiment: sentiment,
                  n_words: nWords,
                  n_bigrams: nBigrams,
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

    async call_api_recommend_from_text(text, nSimilarWords, nNextBigrams){
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
                console.log(data)
                this.setState({
                    mostSimilarWords: data.most_similar_words,
                    nextNBigrams: data.next_bigrams
                })
            })
        }

    }

    write(text) {
        clearTimeout(this.timeout)

        let copyVerses = this.state.verses
        copyVerses[this.state.selectedVerse] = text
        this.setState({
            verses: copyVerses
        })

        this.timeout = setTimeout(async () => {
            this.call_api_recommend_from_text(text)
        },2000)
    }

    selectSentiment(sentiment){
        this.setState({
            sentiment: sentiment
        })
        this.call_api_select_sentiment(sentiment, undefined, undefined).then()
    }

    selectVerse(number) {
        this.setState({
            selectedVerse: number
        })

    }

    selectNWords(n){
        this.setState({
            nWords:n
        })
        this.call_api_select_sentiment(undefined, n, undefined).then()
    }
    
    selectNBigrams(n){
        this.setState({
            nBigrams:n
        })
        this.call_api_select_sentiment(undefined, undefined, n).then()
    }

    selectNSimilarWords(n) {
        this.setState({
            nSimilarWords:n
        })
        this.call_api_recommend_from_text(undefined, n, undefined)
    }

    selectNBigramsRecommendations(n) {
        this.setState({
            nNextBigrams:n
        })
        this.call_api_recommend_from_text(undefined, undefined, n)
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
                    nextNBigrams={this.state.nextNBigrams}
                    selectNBigrams={this.selectNBigrams}
                    selectNWords={this.selectNWords}
                    selectNSimilarWords={this.selectNSimilarWords}
                    selectNBigramsRecommendations={this.selectNBigramsRecommendations}
                />
            </div>
        )
    }
}