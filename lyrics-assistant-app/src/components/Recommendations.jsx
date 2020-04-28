import React from 'react'
import SentimentRecommendations from './SentimentRecommendations'
import UserInputRecommendations from './UserInputRecommendations'
import '../assets/styles/Recommendations.css'

export default class Recommendations extends React.Component {
    constructor(props){
        super(props)

        this.selectNSimilarWords = this.selectNSimilarWords.bind(this)
        this.selectNBigramsRecommendations = this.selectNBigramsRecommendations.bind(this)
    }


    selectNSimilarWords(n) {
        this.props.selectNSimilarWords(n)
    }

    selectNBigramsRecommendations(n) {
        this.props.selectNBigramsRecommendations(n)
    }


    render() {
        return(
            
            <div>
                <SentimentRecommendations 
                    sentiment={this.props.sentiment}
                    mostCommonWords={this.props.mostCommonWords}
                    mostCommonBigrams={this.props.mostCommonBigrams}
                />

                <UserInputRecommendations 
                    mostSimilarWords={this.props.mostSimilarWords}
                    nextNBigrams={this.props.nextNBigrams}
                    selectNSimilarWords={this.selectNSimilarWords}
                    selectNBigramsRecommendations={this.selectNBigramsRecommendations}
                />
            </div>
        )
    }
}