import React from 'react'

import "../assets/styles/Header.css"

import icon from "../assets/icon.svg"

export default class Header extends React.Component {
    
    render() {
        let title = "Lyrics assistant app"
        let lema = "\"Music is the language of the soul\""
        let lines = [
            "Instructions: ", 
            "1. Select the sentiment you are feeling in the lyrics you want to write and start witing the first verse.", 
            "2. Start writing on the left side!",
            "",
            "You can see the recommendations on the right side of this app based on the selected sentiment",
            "You will see more recommendations based on your verse once you start writing!"
        ]
        let renderlines = lines.map((line, index) => {
            return(
                <div className="line">
                    {line} <br/>
                </div>
            )
        })
        return(
            <div className="header">
                <div className="izquierda">
                    <div className="title">{title}</div>
                    <header>{renderlines}</header>
                </div>
                <div className="derecha">
                    <img className="icon" src={icon} alt="React Logo" />
                    <div className="lema">{lema}</div>

                </div>
            <div>

            </div>
            </div>
        )
    }

}