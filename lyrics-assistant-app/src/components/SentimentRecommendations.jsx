import React from 'react'
import Selector from './Selector'
import Cloud from './Cloud'

export default class SentimentRecommendations extends React.Component {

    constructor(props){
        super(props)

        this.onCloudClick = this.onCloudClick.bind(this)
    }

    onCloudClick(word){
        this.props.onCloudClick(word)
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

                {this.props.mostCommonBigrams  ? 
                        <Cloud 
                            type={"bigrams"}
                            sentiment={this.props.sentiment}
                            data={this.props.mostCommonBigrams}
                            onClick={this.onCloudClick}/> :
                        null}

<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>
                <br/>
                
                Most Common Bigrams:


                {this.props.mostCommonWords  ? 
                        <Cloud 
                            type={"words"}
                            sentiment={this.props.sentiment}
                            data={this.props.mostCommonWords}
                            onClick={this.onCloudClick}/> :
                        null}
                
            </div>
        )
    }

}
