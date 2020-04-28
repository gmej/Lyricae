import React from 'react'

export default class Header extends React.Component {
    
    render() {
        let lines = this.props.lines
        let renderlines = lines.map((line, index) => {
            return(
                <div>
                    {line} <br/>
                </div>
            )
        })
        return(
            <div>
                <header className="header">{renderlines}</header>
            </div>
        )
    }

}