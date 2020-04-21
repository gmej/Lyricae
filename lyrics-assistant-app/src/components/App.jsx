import React from 'react'
import WritingSpace from './WritingSpace'
import Header from './Header'


const SENTIMENTS = {
    happy: "happy",
    angry: "angry",
    relaxed: "relaxed",
    sad: "sad",
}
export default class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            writing: false,
            timeout: null,
            sentiment: SENTIMENTS.happy,
            selectedVerse: 0,
            verses: [""]
        }
        this.write = this.write.bind(this)
        this.newVerse = this.newVerse.bind(this)
        this.selectSentiment = this.selectSentiment.bind(this)
        this.selectVerse = this.selectVerse.bind(this)
    }

    componentDidUpdate(){

        console.log("Current verse: ", this.state.selectedVerse)
        console.log("Current sentiment: ", this.state.sentiment)
        console.log("Verses: ", this.state.verses)
    }
    
    componentWillUpdate(){

        clearTimeout(this.timeout)

        let t = setTimeout(() => {
            console.log("TIMEOUT")
        },2000)

        this.timeout = t

    }

    write(text) {
        let copyVerses = this.state.verses
        copyVerses[this.state.selectedVerse] = text
        this.setState({
            verses: copyVerses
        })
    }

    selectSentiment(sentiment){

    }

    selectVerse(number) {
        this.setState({
            selectedVerse: number
        })

    }

    newVerse(){
        let copyVerses = this.state.verses
        copyVerses.push("")
        this.setState({
            verses: copyVerses
        })
    }
    
    //TODO renders twice
    render() {
        let text = "Welcome to the lyrics assistant app!"
        return(
            <div>
                <Header text = {text} />
                <WritingSpace
                    selectVerse={this.state.selectedVerse}  
                    verses={this.state.verses} 
                    write={this.write}
                    selectVerse = {this.selectVerse}
                    selected={this.state.selectedVerse}
                    newVerse={this.newVerse}
                />
                
            </div>
        )
    }
}