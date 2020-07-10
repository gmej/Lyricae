import React from 'react'


import '../assets/styles/Input.css'

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
            <div className="verse">
                <input /* className="input" */
                    className={this.props.selected ? "selectedInput" : "unselectedInput"}
                    autoFocus={this.props.selected ? "autofocus" : null}
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