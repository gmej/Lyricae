import React from 'react'
import Selector from './Selector'

export default class SentimentRecommendations extends React.Component {


    constructor(props){
        super(props)

        this.createTable = this.createTable.bind(this)
        this.selectNWords = this.selectNWords.bind(this)
        this.selectNBigrams = this.selectNBigrams.bind(this)
    }

    createTable(content){
        let table = []
    
        content.forEach(word => {
            table.push(<td key = {word}>{word}</td>)
        });
        return table
    }

    selectNWords(n){
        this.props.selectNWords(n)
    }


    selectNBigrams(n){
        this.props.selectNBigrams(n)
    }

    render() {
        return(
            <div>
                <br/>

                Most Common Words: 

                <Selector selectNumber={this.selectNWords} />
                <br/>
                <table>
                    {this.props.mostCommonWords != null ? 
                        this.createTable(this.props.mostCommonWords) :
                        null}
                </table>

                <br/>
                <br/>
                
                Most Common Bigrams:

                <Selector selectNumber={this.selectNBigrams} />
                <br/>
                <table>
                    {this.props.mostCommonBigrams != null ? 
                        this.createTable(this.props.mostCommonBigrams) :
                        null}
                </table>
            </div>
        )
    }


}
