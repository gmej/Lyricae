import React from 'react'

export default class Header extends React.Component {
    
    render() {
        return(
            <div>
                <header className="header">{this.props.text}</header>
            </div>
        )
    }

}