import React from 'react'
import Selector from './Selector'

export default class UserInputRecommendations extends React.Component {

    constructor(props){
        super(props)

        this.selectNSimilarWords = this.selectNSimilarWords.bind(this)
        this.selectNBigramsRecommendations = this.selectNBigramsRecommendations.bind(this)
        this.createMostSimilarWordsTable = this.createMostSimilarWordsTable.bind(this)
        this.onWordClick = this.onWordClick.bind(this)
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
            table.push(<div key={"recom_" + recom}>{recom}</div>)
        })
        return table
    }


    onWordClick(word){
        console.log('AAAAAAAAAAAAAAa')
        console.log('AAAAAAAAAAAAAAa')
        console.log('AAAAAAAAAAAAAAa')
        console.log('AAAAAAAAAAAAAAa')
        console.log('AAAAAAAAAAAAAAa')
        console.log(word)
        this.props.onWordClick(word.target)
    }

    createMostSimilarWordsTable(content){
        let words = []
        for(let word in content){
            words.push(word)
        }
        return words.map((word, index) =>{
            let words2 = []
            let recoms = content[word]
            let i=1
            for(let el in recoms){
                let newWord = ""
                if(i < recoms.length){
                    newWord = recoms[el] + ", "
                } else {
                    newWord = recoms[el]
                }
                words2.push(<span>{newWord}</span>)
                i++
            }
                return(
                    <div key={"word_"+word}>
                    {/* {word}: {newWord} */}
                    {word}: {words2}
                </div>
            )
        })
    }


    render() {
        return(
            <div>

                <div className="box">
                Recommendations based on written words:
                    <Selector selectNumber={this.selectNSimilarWords} />
                    <br/>
                    <div>
                        {this.props.mostSimilarWords != null ? 
                            this.createMostSimilarWordsTable(this.props.mostSimilarWords) :
                            null}
                    </div>
                </div>


                <div className="box">
                Recommendations to continue the verse:

                <Selector min={2} max={5} initial={3} selectNumber={this.selectNBigramsRecommendations} />
                <br/>
                <ul>
                    {this.props.nextNBigrams != null ? 
                        <div>{this.createList(this.props.nextNBigrams)} </div> :
                        null}
                </ul>
                </div>
            </div>
        )
    }
}
