import React from 'react'
import Selector from './Selector'

export default class UserInputRecommendations extends React.Component {

    constructor(props){
        super(props)

        this.selectNSimilarWords = this.selectNSimilarWords.bind(this)
        this.selectNBigramsRecommendations = this.selectNBigramsRecommendations.bind(this)
        this.createMostSimilarWordsTable = this.createMostSimilarWordsTable.bind(this)
    }


    selectNSimilarWords(n){
        this.props.selectNSimilarWords(n)
    }

    selectNBigramsRecommendations(n){
        this.props.selectNBigramsRecommendations(n)
    }

    createList(content){
        let table = []
        content.map((recom, i) => {
            table.push(<tr key={"recom_" + recom}>{recom}</tr>)
        })
        return table
    }

    createMostSimilarWordsTable(content){
        let words = []
        for(let word in content){
            words.push(word)
        }
        return words.map((word, i) =>{
            return(
                <div key={"word_"+word}>
                    {word}: {content[word] + " , "}
                </div>
            )
        })
    }


    render() {
        return(
            <div>
                <br/>
                Most Similar Words: 
                <Selector selectNumber={this.selectNSimilarWords} />
                <br/>
                <div>
                    {this.props.mostSimilarWords != null ? 
                        this.createMostSimilarWordsTable(this.props.mostSimilarWords) :
                        null}
                </div>
                <br/>
                <br/>
            
                Recommendations:

                <Selector min={2} max={5} initial={3} selectNumber={this.selectNBigramsRecommendations} />
                <br/>
                <ul>
                    {this.props.nextNBigrams != null ? 
                        <table>{this.createList(this.props.nextNBigrams)} </table> :
                        null}
                </ul>
            </div>
        )
    }
}
