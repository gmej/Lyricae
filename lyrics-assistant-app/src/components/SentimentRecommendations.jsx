import React from 'react'
import Selector from './Selector'
import Cloud from './Cloud'

export default class SentimentRecommendations extends React.Component {


    constructor(props){
        super(props)

        this.createTableBigrams = this.createTableBigrams.bind(this)
    }

    createTable(content){
        return
        let words = []
        let weights = content.weights
        let words_list = content.words
        words_list.forEach(word => {
            words.push(<td key = {word}>{word}</td>)
        });
        return words
    }

    createTableBigrams(content){
        return
        let words = []
        content.forEach(word => {
            words.push(<td key = {word}>{word}</td>)
        });
        return words
    }

    render() {
        if(!this.props.mostCommonWords || !this.props.mostCommonBigrams) {
            return(<div></div>)
        }

        return(
            <div>
                <br/>

                Most Common Words: 

                <br/>
                {/* <Cloud type={"bigrams"} sentiment={this.props.sentiment} data={this.props.mostCommonBigrams}/> */}
                {/* <Cloud type={"words"} sentiment={this.props.sentiment} data={this.props.mostCommonWords}/> */}
                <table>
                    {this.props.mostCommonWords >0 ? 
                        this.createTable(this.props.mostCommonWords) :
                        null}
                </table>

                <br/>
                <br/>
                
                Most Common Bigrams:

                <br/>
                <table>
                    {this.props.mostCommonBigrams != null ? 
                        this.createTableBigrams(this.props.mostCommonBigrams) :
                        null}
                </table>
            </div>
        )
    }

}
