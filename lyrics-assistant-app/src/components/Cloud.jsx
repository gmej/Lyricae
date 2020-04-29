import React from 'react'
import { TagCloud } from 'react-tagcloud'

import "../assets/styles/Cloud.css"

let divStyle = {
    "height": "200px",
    "width": "40%",
    "background-color": "powderblue",
    "float": "right",
  }

export default class Cloud extends React.Component {



constructor(props){
    super(props)

    this.onClick = this.onClick.bind(this)
}

onClick(word){
    this.props.onClick(word)
}

// minSize, maxSize - font size in px
// tags - array of objects with properties value and count
// shuffle - indicates if data should be shuffled (true by default)
// onClick event handler has `tag` and `event` parameter
render(){
    return(
        <div style={divStyle}>
            <h1>Most common {this.props.type} for sentiment: {this.props.sentiment}</h1>
            <TagCloud
            minSize={12}
            maxSize={55}
            shuffle={true}
            tags={this.props.data}
            className="simple-cloud"
            onClick={tag => this.onClick(tag.value)}
            />
        </div>
        )
        
    } 
    }