import React from 'react'
import { TagCloud } from 'react-tagcloud'

import "../assets/styles/Cloud.css"


export default class Cloud extends React.Component {



colorOptions = {
    luminosity: 'bright',
    hue: '#ffcad4',
    /* count: 15 */
}

constructor(props){
    super(props)

    this.onWordClick = this.onWordClick.bind(this)
}

onWordClick(word){
    this.props.onWordClick(word)
}

render(){
    return(
        <div className="cloud">
            <div className="cloudTitle">Most common {this.props.type} for sentiment: {this.props.sentiment}</div>
            <TagCloud
            minSize={18}
            maxSize={60}
            shuffle={true}
            tags={this.props.data}
            className="simple-cloud"
            onClick={tag => this.onWordClick(tag.value)}
            colorOptions={this.colorOptions}
            />
        </div>
        )
        
    } 
    }