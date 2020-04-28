import React from 'react'
import TagCloud from "react-tag-cloud";
import randomColor from "randomcolor";
import '../assets/styles/Cloud.css'

const styles = {
    large: {
      fontSize: 60,
      fontWeight: "bold"
    },
    small: {
      opacity: 0.7,
      fontSize: 16
    }
  };

export default class Cloud extends React.Component {

    constructor(props){
        super(props)

        this.getElements = this.getElements.bind(this)
        this.onClick = this.onClick.bind(this)
    }

    componentDidMount()  {
        /*
      setInterval(() => {
        this.forceUpdate();
      }, 10*1000); */
    }

    onClick(w){
        console.log(w)
    }
    

    getElements(data){
        let elements = []
        for(let word in data){
            let weight = data[word]
            elements.push(<div id={word} className="tag-item-wrapper"
                /* onClick={this.onClick(w)} */
                style={{
                fontFamily: "serif",
                fontSize: weight,
                fontStyle: "italic",
                fontWeight: "bold",
                color: randomColor()
                }} >
                <div>
                    { word }
                </div>
            </div>)
        };
        return elements
    }

    render() {
        return (
            <div className="app-outer">
            <div className="app-inner">
                <h1>Most common {this.props.type} for sentiment: {this.props.sentiment}</h1>
                <TagCloud
                className="tag-cloud"
                style={{
                    fontFamily: "sans-serif",
                    // fontSize: () => Math.round(Math.random() * 50) + 16,
                    fontSize: 30,
                    color: () =>
                    randomColor({
                        hue: "blue"
                    }),
                    padding: 5
                }}
                >
                {this.getElements(this.props.data)}
                </TagCloud>
            </div>
            </div>
        );
    }
}