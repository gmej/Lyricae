import React from 'react'

import '../assets/styles/Recommendations.css'

export default class Recommendations extends React.Component {
    constructor(props){
        super(props)

        this.createTable = this.createTable.bind(this)
    }

    createTable(content){
        let table = []
    
        content.forEach(word => {
            table.push(<td key = {word}>{word}</td>)
        });
        return table
    }

    createMostSimilarWordsTable(content){
        let tables = []
        let table = []
        // Outer loop to create parent
        let words = []
        for(let word in content){
            words.push(word)
        }
        /* tables.push(<th>{words}</th>) */
        for(let word in content){
            let children = []
            for(let recom in content[word]){
                children.push(<tr>{content[word][recom]}</tr>)
                
            }
            table.push(<td>{children}</td>)
        }
        return table
      }

    render() {
        console.log('AAAAAAAAAAa')
        console.log(this.props.mostSimilarWords)
        return(
            
            <div>

                Most Common Words: 
                <table>
                    <p>{this.props.mostCommonWords != null ? 
                    this.createTable(this.props.mostCommonWords) :
                     null}</p>
                </table>

                
                Most Common Bigrams:
                <table>
                     <p>{this.props.mostCommonBigrams != null ? 
                    this.createTable(this.props.mostCommonBigrams) :
                     null}</p>
                </table>

                Most Similar Words: 
                <table>
                    {this.props.mostSimilarWords != null ? 
                    this.createMostSimilarWordsTable(this.props.mostSimilarWords) :
                     null}
                </table>
                {/* <p>{this.props.nextBigrams}</p> */}
            </div>
        )
    }
}