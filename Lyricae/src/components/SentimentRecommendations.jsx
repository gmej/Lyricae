import React from 'react'
import Cloud from './Cloud'

export default class SentimentRecommendations extends React.Component {

    constructor(props){
        super(props)

        this.onWordClick = this.onWordClick.bind(this)
    }

    onWordClick(word){
        this.props.onWordClick(word)
    }

    render() {
        if(!this.props.mostCommonWords || !this.props.mostCommonBigrams) {
            return(<div></div>)
        }

        return(
            <div>
                <div className="box">
                    {this.props.mostCommonBigrams  ? 
                        <Cloud 
                        type={"bigrams"}
                        sentiment={this.props.sentiment}
                        data={this.props.mostCommonBigrams}
                        onWordClick={this.onWordClick}/> :
                        null
                    }
                </div>
                <div className="box">
                    {this.props.mostCommonWords  ? 
                        <Cloud 
                            type={"words"}
                            sentiment={this.props.sentiment}
                            data={this.props.mostCommonWords}
                            onWordClick={this.onWordClick}/> :
                        null
                    }
                </div>
            </div>
        )
    }

}
