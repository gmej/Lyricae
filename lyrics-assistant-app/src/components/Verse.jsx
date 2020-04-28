import React from 'react'

export default class Verse extends React.Component {

    constructor(props) {
        super(props)
        this.handleChange = this.handleChange.bind(this)
        this.select = this.select.bind(this)
    }

    
    handleChange(event) {
        this.props.write(event.target.value)
    }

    select() {
        this.props.selectVerse(this.props.id)
    }
    
    render() {
        return(
            <div id={this.props.id}>
                <input 
                    autofocus={this.props.selected ? "autofocus" : null}
                    className={this.props.selected ? "selected" : "unselected"}
                    type="text"
                    id={this.props.key}
                    name={this.props.key}
                    value={this.props.text}
                    onChange={this.handleChange}
                    onClick={this.select}
                    >
                    </input>
            </div>
        )
    }

}