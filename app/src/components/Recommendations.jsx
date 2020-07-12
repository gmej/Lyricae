import React from 'react'
import SentimentRecommendations from './SentimentRecommendations'
import UserInputRecommendations from './UserInputRecommendations'
//import '../assets/styles/Recommendations.css'

export default class Recommendations extends React.Component {
    constructor(props){
        super(props)

        this.selectNSimilarWords = this.selectNSimilarWords.bind(this)
        this.selectNBigramsRecommendations = this.selectNBigramsRecommendations.bind(this)
        this.onWordClick = this.onWordClick.bind(this)
    }


    selectNSimilarWords(n) {
        this.props.selectNSimilarWords(n)
    }

    selectNBigramsRecommendations(n) {
        this.props.selectNBigramsRecommendations(n)
    }

    onClick(word){
        this.props.onClick(word)
    }

    onWordClick(word){
        this.props.onWordClick(word)
    }

    render() {
        return( 
            <div className="recommendations">
                <SentimentRecommendations 
                    sentiment={this.props.sentiment}
                    mostCommonWords={this.props.mostCommonWords}
                    mostCommonBigrams={this.props.mostCommonBigrams}
                    onWordClick={this.onWordClick}
                />
                <UserInputRecommendations 
                    mostSimilarWords={this.props.mostSimilarWords}
                    nextNBigrams={this.props.nextNBigrams}
                    selectNSimilarWords={this.selectNSimilarWords}
                    selectNBigramsRecommendations={this.selectNBigramsRecommendations}
                    onWordClick={this.onWordClick}
                />
            </div>
        )
    }
}