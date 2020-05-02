import React from 'react'
import Verse from './Verse'
export default class WritingSpace extends React.Component {

    constructor(props) {
        super(props)
        this.write = this.write.bind(this)
        this.newVerse = this.newVerse.bind(this)
        this.selectVerse = this.selectVerse.bind(this)
    }

    
    write(text) {
        this.props.write(text)
    }

    newVerse(){
        this.props.newVerse()
    }

    selectVerse(id){
        this.props.selectVerse(id)
    }

    render() {
        let verses = this.props.verses
        //verses.push(" ")
        let renderVerses = verses.map((verse, index) => {
            let key = "verse" + index
            return(
                <Verse
                    id={index}
                    text={verse}
                    write={this.write}
                    selectVerse = {this.selectVerse}
                    selected={this.props.selected === index ?
                        true : false}
                    />
            )
        })

        
        return(
            <div className="box">
                <div>Write here:</div>
                {renderVerses}
                <input 
                    type="button"
                    value="New verse"
                    onClick={this.newVerse}
                ></input>
            </div>
        )

    }

}